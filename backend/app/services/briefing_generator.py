"""
Briefing Generator service for creating auto-generated health briefings.
Handles both data analysis and article summary briefings.
"""
from datetime import datetime
from typing import Dict, Any, List
import re
from app.config import ReadingLevel, BriefingSourceType
from app.services.llm_client import llm_client
from app.services.source_finder import source_finder
from app.services.article_extractor import article_extractor


class BriefingGenerator:
    """
    Generates auto-briefings from either data analysis or article summaries.
    """

    def generate_data_analysis_briefing(
        self,
        disease_stats: Dict[str, Any],
        reading_level: ReadingLevel = ReadingLevel.GRADE_8,
    ) -> Dict[str, Any]:
        """
        Generate a briefing from disease surveillance data.

        Args:
            disease_stats: Dictionary with disease statistics (cases, trends, etc.)
            reading_level: Target reading level

        Returns:
            Dictionary with briefing data ready for database insertion
        """
        # Use LLM to generate briefing content
        llm_response = llm_client.generate_briefing(
            source_type="data_analysis",
            data=disease_stats,
            reading_level=reading_level,
        )

        # Generate slug from title
        slug = self._generate_slug(llm_response.get("title", "briefing"))

        # Add timestamp to slug to ensure uniqueness
        date_suffix = datetime.utcnow().strftime("%Y-%m-%d")
        slug = f"{slug}-{date_suffix}"

        return {
            "title": llm_response.get("title", "Weekly Health Briefing"),
            "slug": slug,
            "summary": llm_response.get("summary", ""),
            "body": llm_response.get("body_markdown", ""),
            "source_type": BriefingSourceType.DATA_ANALYSIS.value,
            "source_urls": None,
            "source_metadata": disease_stats,
            "tags": llm_response.get("tags", []),
            "reading_level": reading_level.value,
            "disclaimer": llm_response.get(
                "disclaimer",
                "This information is for general educational purposes only and is not medical advice."
            ),
        }

    def generate_article_summary_briefing(
        self,
        topic: str,
        reading_level: ReadingLevel = ReadingLevel.GRADE_8,
        max_articles: int = 3,
    ) -> Dict[str, Any]:
        """
        Generate a briefing by finding and summarizing recent health articles.

        Args:
            topic: Health topic to search for (e.g., "diabetes research updates")
            reading_level: Target reading level
            max_articles: Maximum number of articles to summarize

        Returns:
            Dictionary with briefing data ready for database insertion
        """
        # Step 1: Find relevant articles
        search_results = source_finder.search(topic, max_results=max_articles)

        if not search_results:
            raise ValueError(f"No trusted sources found for topic: {topic}")

        # Step 2: Extract full article content
        articles = []
        source_urls = []

        for result in search_results:
            url = result.get("url")
            if not url:
                continue

            # Extract article content
            extracted = article_extractor.extract(url)

            if extracted and extracted.get("text"):
                articles.append({
                    "url": url,
                    "title": extracted.get("title", result.get("title", "Article")),
                    "content": extracted.get("text", ""),
                })
                source_urls.append(url)
            else:
                # Fallback: use snippet from search results
                articles.append({
                    "url": url,
                    "title": result.get("title", "Article"),
                    "content": result.get("snippet", ""),
                })
                source_urls.append(url)

        if not articles:
            raise ValueError(f"Failed to extract content from articles for topic: {topic}")

        # Step 3: Use LLM to generate summary briefing
        llm_response = llm_client.generate_briefing(
            source_type="article_summary",
            data={"articles": articles, "topic": topic},
            reading_level=reading_level,
        )

        # Generate slug from title
        slug = self._generate_slug(llm_response.get("title", topic))

        # Add timestamp to ensure uniqueness
        date_suffix = datetime.utcnow().strftime("%Y-%m-%d")
        slug = f"{slug}-{date_suffix}"

        return {
            "title": llm_response.get("title", f"Health News: {topic}"),
            "slug": slug,
            "summary": llm_response.get("summary", ""),
            "body": llm_response.get("body_markdown", ""),
            "source_type": BriefingSourceType.ARTICLE_SUMMARY.value,
            "source_urls": source_urls,
            "source_metadata": {"topic": topic, "article_count": len(articles)},
            "tags": llm_response.get("tags", []),
            "reading_level": reading_level.value,
            "disclaimer": llm_response.get(
                "disclaimer",
                "This information is for general educational purposes only and is not medical advice."
            ),
        }

    def generate_mock_data_briefing(
        self,
        reading_level: ReadingLevel = ReadingLevel.GRADE_8,
    ) -> Dict[str, Any]:
        """
        Generate a briefing with mock disease data for demonstration.
        Useful for initial testing and demo purposes.

        Returns:
            Dictionary with briefing data
        """
        mock_stats = {
            "period": "Week of November 17, 2025",
            "diseases": [
                {
                    "name": "COVID-19",
                    "cases_this_week": 12500,
                    "change_from_last_week": "+8%",
                    "trend": "increasing",
                },
                {
                    "name": "Influenza",
                    "cases_this_week": 8200,
                    "change_from_last_week": "-3%",
                    "trend": "stable",
                },
                {
                    "name": "RSV",
                    "cases_this_week": 3400,
                    "change_from_last_week": "+15%",
                    "trend": "increasing",
                },
            ],
            "notes": "Data is from public health surveillance systems. Case counts may be underreported.",
        }

        return self.generate_data_analysis_briefing(mock_stats, reading_level)

    def _generate_slug(self, title: str) -> str:
        """
        Generate a URL-safe slug from a title.

        Args:
            title: The title to convert

        Returns:
            URL-safe slug
        """
        # Convert to lowercase
        slug = title.lower()

        # Replace spaces and special chars with hyphens
        slug = re.sub(r"[^a-z0-9]+", "-", slug)

        # Remove leading/trailing hyphens
        slug = slug.strip("-")

        # Limit length
        slug = slug[:100]

        return slug


# Global briefing generator instance
briefing_generator = BriefingGenerator()
