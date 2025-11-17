"""
Article Extractor service for extracting main content from web articles.
Uses trafilatura for robust article text extraction.
"""
import requests
from typing import Optional, Dict, Any


class ArticleExtractor:
    """
    Extracts main article content from URLs.
    Handles various article formats and cleans HTML.
    """

    def __init__(self):
        self.timeout = 10
        self.user_agent = "EazyHealthAI/0.1.0 (Health Information Bot)"

    def extract(self, url: str) -> Optional[Dict[str, Any]]:
        """
        Extract article content from a URL.

        Args:
            url: The URL to extract content from

        Returns:
            Dictionary with title, text, and metadata, or None if extraction fails
        """
        try:
            # Fetch the web page
            headers = {"User-Agent": self.user_agent}
            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            html_content = response.text

            # Try using trafilatura first (best for articles)
            try:
                import trafilatura

                # Extract with metadata
                text = trafilatura.extract(
                    html_content,
                    include_comments=False,
                    include_tables=False,
                )

                metadata = trafilatura.extract_metadata(html_content)

                if text:
                    return {
                        "url": url,
                        "title": metadata.title if metadata and metadata.title else "Article",
                        "text": text,
                        "author": metadata.author if metadata and metadata.author else None,
                        "date": metadata.date if metadata and metadata.date else None,
                        "word_count": len(text.split()),
                    }

            except ImportError:
                print("Warning: trafilatura not installed, using fallback extractor")

            # Fallback to simpler extraction
            return self._extract_fallback(url, html_content)

        except Exception as e:
            print(f"Article extraction error for {url}: {e}")
            return None

    def _extract_fallback(self, url: str, html_content: str) -> Optional[Dict[str, Any]]:
        """
        Fallback extraction method using BeautifulSoup.
        Simpler but less accurate than trafilatura.
        """
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html_content, "html.parser")

            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "aside"]):
                script.decompose()

            # Get title
            title = soup.find("title")
            title_text = title.get_text().strip() if title else "Article"

            # Try to find main content
            main_content = None
            for tag in ["article", "main", "div[role='main']"]:
                main_content = soup.find(tag)
                if main_content:
                    break

            # Fallback to body if no main content found
            if not main_content:
                main_content = soup.find("body")

            if not main_content:
                return None

            # Extract text
            text = main_content.get_text(separator="\n", strip=True)

            # Basic cleanup
            lines = [line.strip() for line in text.split("\n") if line.strip()]
            text = "\n\n".join(lines)

            return {
                "url": url,
                "title": title_text,
                "text": text,
                "author": None,
                "date": None,
                "word_count": len(text.split()),
            }

        except ImportError:
            print("Warning: BeautifulSoup not installed")
            return None
        except Exception as e:
            print(f"Fallback extraction error: {e}")
            return None

    def extract_excerpt(self, text: str, max_chars: int = 500) -> str:
        """
        Extract a short excerpt from article text.

        Args:
            text: The full article text
            max_chars: Maximum characters for excerpt

        Returns:
            Excerpt string
        """
        if len(text) <= max_chars:
            return text

        # Try to cut at sentence boundary
        excerpt = text[:max_chars]
        last_period = excerpt.rfind(".")
        last_question = excerpt.rfind("?")
        last_exclamation = excerpt.rfind("!")

        last_sentence_end = max(last_period, last_question, last_exclamation)

        if last_sentence_end > max_chars * 0.7:  # If we can keep at least 70% of excerpt
            return excerpt[:last_sentence_end + 1]

        return excerpt + "..."


# Global article extractor instance
article_extractor = ArticleExtractor()
