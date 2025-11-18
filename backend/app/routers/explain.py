"""
Explainer API router for on-demand health explanations.
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session

from app.config import ReadingLevel
from app.database import get_db
from app.models.explainer_log import ExplainerLog
from app.services.llm_client import llm_client
from app.services.source_finder import source_finder
from app.services.article_extractor import article_extractor
from app.services.token_counter import token_counter

router = APIRouter(prefix="/api", tags=["Explainer"])


class ExplainRequest(BaseModel):
    """Request model for explain endpoint."""
    query: Optional[str] = Field(None, description="Health-related question")
    url: Optional[str] = Field(None, description="URL to a health article")
    raw_text: Optional[str] = Field(None, description="Raw text to explain")
    reading_level: ReadingLevel = Field(
        ReadingLevel.GRADE_6,
        description="Target reading comprehension level"
    )


class ExplainerSection(BaseModel):
    """A section in the explainer response."""
    heading: str
    content: str


class ExplainResponse(BaseModel):
    """Response model for explain endpoint."""
    title: str
    sections: List[ExplainerSection]
    sources: List[Dict[str, str]] = Field(default_factory=list, description="Sources used")
    disclaimer: str


@router.post("/explain", response_model=ExplainResponse)
async def explain(
    request: ExplainRequest,
    db: Session = Depends(get_db)
) -> ExplainResponse:
    """
    Generate a patient-friendly health explainer.

    At least one of query, url, or raw_text must be provided.
    The system will:
    1. Find relevant trustworthy sources (if query provided)
    2. Extract article content (if url provided)
    3. Generate a structured, easy-to-read explanation
    """
    # Validate input
    if not any([request.query, request.url, request.raw_text]):
        raise HTTPException(
            status_code=400,
            detail="At least one of 'query', 'url', or 'raw_text' must be provided"
        )

    input_text = ""
    sources_found = []
    source_url = request.url
    input_excerpt = None

    try:
        # Case 1: URL provided - extract article content
        if request.url:
            extracted = article_extractor.extract(request.url)

            if not extracted or not extracted.get("text"):
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to extract content from URL: {request.url}"
                )

            input_text = extracted["text"]

            # Check token count and truncate if necessary
            text_tokens = token_counter.count_tokens(input_text)
            base_prompt_tokens = 500  # Estimated tokens for system prompt

            if text_tokens + base_prompt_tokens > token_counter.max_input_tokens:
                print(f"⚠️  Article too long ({text_tokens} tokens). Truncating to fit within limit...")
                # Truncate to fit: calculate max chars we can use
                max_tokens_for_text = token_counter.max_input_tokens - base_prompt_tokens
                # Rough estimate: 1 token ≈ 4 characters
                max_chars = max_tokens_for_text * 4
                input_text = input_text[:max_chars]
                truncated_tokens = token_counter.count_tokens(input_text)
                print(f"✓ Truncated to {truncated_tokens} tokens")

            input_excerpt = article_extractor.extract_excerpt(input_text)
            sources_found.append({
                "url": request.url,
                "title": extracted.get("title", "Article"),
                "excerpt": input_excerpt,
            })

        # Case 2: Raw text provided
        elif request.raw_text:
            input_text = request.raw_text

            # Check token count and truncate if necessary
            text_tokens = token_counter.count_tokens(input_text)
            base_prompt_tokens = 500  # Estimated tokens for system prompt

            if text_tokens + base_prompt_tokens > token_counter.max_input_tokens:
                print(f"⚠️  Raw text too long ({text_tokens} tokens). Truncating to fit within limit...")
                max_tokens_for_text = token_counter.max_input_tokens - base_prompt_tokens
                max_chars = max_tokens_for_text * 4
                input_text = input_text[:max_chars]
                truncated_tokens = token_counter.count_tokens(input_text)
                print(f"✓ Truncated to {truncated_tokens} tokens")

            input_excerpt = article_extractor.extract_excerpt(input_text)

        # Case 3: Query provided - search for sources
        elif request.query:
            # Search for relevant sources
            search_results = source_finder.search(request.query, max_results=3)

            if not search_results:
                raise HTTPException(
                    status_code=404,
                    detail=f"No trusted sources found for query: {request.query}"
                )

            # Extract content from multiple sources and select based on token limits
            articles = []
            for result in search_results:
                url = result.get("url")
                if not url:
                    continue

                extracted = article_extractor.extract(url)
                if extracted and extracted.get("text"):
                    articles.append({
                        "url": url,
                        "title": extracted.get("title", result.get("title", "Article")),
                        "text": extracted.get("text", ""),
                    })

            if articles:
                # Use token counter to select articles that fit within limits
                print(f"Found {len(articles)} articles for query. Selecting based on token limit...")
                selected_articles = token_counter.select_articles_within_limit(
                    articles, base_prompt_tokens=500
                )

                if selected_articles:
                    # Combine selected article(s) into input_text
                    input_text = "\n\n---\n\n".join([
                        f"Source: {article['title']}\n\n{article['text']}"
                        for article in selected_articles
                    ])

                    # Add to sources_found
                    for article in selected_articles:
                        excerpt = article_extractor.extract_excerpt(article['text'])
                        sources_found.append({
                            "url": article["url"],
                            "title": article["title"],
                            "excerpt": excerpt,
                        })

                    input_excerpt = article_extractor.extract_excerpt(input_text)
                    print(f"✓ Selected {len(selected_articles)} article(s) that fit within token limit")
                else:
                    # No articles fit - find the shortest one and truncate it
                    print("⚠️  All articles too long. Finding shortest article to truncate...")

                    # Sort articles by token count (ascending)
                    articles_with_tokens = [
                        {
                            **article,
                            "token_count": token_counter.count_tokens(article["text"])
                        }
                        for article in articles
                    ]
                    articles_with_tokens.sort(key=lambda x: x["token_count"])

                    shortest_article = articles_with_tokens[0]
                    print(f"Shortest article: {shortest_article['token_count']} tokens. Truncating to fit...")

                    # Truncate to fit within limit
                    max_tokens_for_text = token_counter.max_input_tokens - 500
                    max_chars = max_tokens_for_text * 4
                    truncated_text = shortest_article["text"][:max_chars]

                    input_text = f"Source: {shortest_article['title']}\n\n{truncated_text}"
                    input_excerpt = article_extractor.extract_excerpt(truncated_text)

                    sources_found.append({
                        "url": shortest_article["url"],
                        "title": shortest_article["title"],
                        "excerpt": input_excerpt,
                    })

                    truncated_tokens = token_counter.count_tokens(truncated_text)
                    print(f"✓ Truncated shortest article to {truncated_tokens} tokens")
            else:
                # Fallback: use search snippets if extraction failed for all
                print("⚠️  Failed to extract content from articles. Using search snippets as fallback.")
                input_text = "\n\n".join([
                    f"{r['title']}\n{r.get('snippet', '')}"
                    for r in search_results
                ])
                input_excerpt = article_extractor.extract_excerpt(input_text)

                for result in search_results:
                    sources_found.append({
                        "url": result["url"],
                        "title": result["title"],
                        "excerpt": result.get("snippet", ""),
                    })

        # Generate explainer using LLM
        topic_hint = request.query or "health information"
        explainer_output = llm_client.generate_explainer(
            input_text=input_text,
            topic_hint=topic_hint,
            reading_level=request.reading_level,
        )

        # Log the request for analytics
        log_entry = ExplainerLog(
            query=request.query,
            source_url=source_url,
            input_excerpt=input_excerpt,
            sources_found=sources_found,
            reading_level=request.reading_level.value,
            output_json=explainer_output,
        )
        db.add(log_entry)
        db.commit()

        # Format response
        # Handle case where LLM returns content as list instead of string
        sections = []
        for section in explainer_output.get("sections", []):
            content = section.get("content", "")
            # If content is a list, join it into a single string
            if isinstance(content, list):
                content = "\n\n".join(str(item) for item in content)
            sections.append(
                ExplainerSection(
                    heading=section.get("heading", ""),
                    content=content
                )
            )

        return ExplainResponse(
            title=explainer_output.get("title", topic_hint),
            sections=sections,
            sources=sources_found,
            disclaimer=explainer_output.get(
                "disclaimer",
                "This information is for general educational purposes only and is not medical advice."
            ),
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in explain endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate explainer: {str(e)}"
        )
