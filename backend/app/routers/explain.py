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
            input_excerpt = article_extractor.extract_excerpt(input_text)
            sources_found.append({
                "url": request.url,
                "title": extracted.get("title", "Article"),
                "excerpt": input_excerpt,
            })

        # Case 2: Raw text provided
        elif request.raw_text:
            input_text = request.raw_text
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

            # Extract content from top result
            top_result = search_results[0]
            extracted = article_extractor.extract(top_result["url"])

            if extracted and extracted.get("text"):
                input_text = extracted["text"]
                input_excerpt = article_extractor.extract_excerpt(input_text)

                for result in search_results:
                    sources_found.append({
                        "url": result["url"],
                        "title": result["title"],
                        "excerpt": result.get("snippet", ""),
                    })
            else:
                # Fallback: use search snippets
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
        return ExplainResponse(
            title=explainer_output.get("title", topic_hint),
            sections=[
                ExplainerSection(
                    heading=section["heading"],
                    content=section["content"]
                )
                for section in explainer_output.get("sections", [])
            ],
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
