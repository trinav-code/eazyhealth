"""
Source Finder service for discovering relevant, trustworthy health information sources.
Integrates with web search APIs to find articles that answer user queries.
"""
import requests
from typing import List, Dict, Any, Optional
from app.config import settings, get_trusted_domains


class SourceFinder:
    """
    Finds relevant, trustworthy sources for health queries.
    Supports multiple search providers with fallback to mock data.
    """

    def __init__(self):
        self.provider = settings.search_provider
        self.trusted_domains = get_trusted_domains()

    def search(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant sources based on a health query.

        Args:
            query: The health-related search query
            max_results: Maximum number of results to return

        Returns:
            List of search results with url, title, and snippet
        """
        if self.provider == "brave":
            return self._search_brave(query, max_results)
        elif self.provider == "serper":
            return self._search_serper(query, max_results)
        else:
            # Mock mode for development
            return self._search_mock(query, max_results)

    def _search_brave(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using Brave Search API."""
        if not settings.brave_api_key:
            print("Warning: Brave API key not configured, falling back to mock search")
            return self._search_mock(query, max_results)

        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {
                "X-Subscription-Token": settings.brave_api_key,
                "Accept": "application/json",
            }
            params = {
                "q": f"{query} site:({' OR site:'.join(self.trusted_domains)})",
                "count": max_results,
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            for item in data.get("web", {}).get("results", [])[:max_results]:
                results.append({
                    "url": item.get("url"),
                    "title": item.get("title"),
                    "snippet": item.get("description", ""),
                })

            return results

        except Exception as e:
            print(f"Brave search error: {e}, falling back to mock")
            return self._search_mock(query, max_results)

    def _search_serper(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search using Serper API."""
        if not settings.serper_api_key:
            print("Warning: Serper API key not configured, falling back to mock search")
            return self._search_mock(query, max_results)

        try:
            url = "https://google.serper.dev/search"
            headers = {
                "X-API-KEY": settings.serper_api_key,
                "Content-Type": "application/json",
            }
            payload = {
                "q": f"{query} site:({' OR '.join(self.trusted_domains)})",
                "num": max_results,
            }

            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            results = []

            for item in data.get("organic", [])[:max_results]:
                results.append({
                    "url": item.get("link"),
                    "title": item.get("title"),
                    "snippet": item.get("snippet", ""),
                })

            return results

        except Exception as e:
            print(f"Serper search error: {e}, falling back to mock")
            return self._search_mock(query, max_results)

    def _search_mock(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """
        Mock search for development/testing.
        Returns curated results based on common health topics.
        """
        # Mock database of common health topics
        mock_database = {
            "atrial fibrillation": [
                {
                    "url": "https://www.cdc.gov/heartdisease/atrial_fibrillation.htm",
                    "title": "Atrial Fibrillation - CDC",
                    "snippet": "Atrial fibrillation (AFib) is the most common type of irregular heartbeat. Learn about symptoms, causes, and treatment options.",
                },
                {
                    "url": "https://www.mayoclinic.org/diseases-conditions/atrial-fibrillation/symptoms-causes/syc-20350624",
                    "title": "Atrial Fibrillation - Symptoms and Causes - Mayo Clinic",
                    "snippet": "Atrial fibrillation is an irregular and often very rapid heart rhythm that can lead to blood clots in the heart.",
                },
            ],
            "diabetes": [
                {
                    "url": "https://www.cdc.gov/diabetes/basics/diabetes.html",
                    "title": "What is Diabetes? - CDC",
                    "snippet": "Diabetes is a chronic disease that affects how your body turns food into energy. Learn about type 1, type 2, and gestational diabetes.",
                },
                {
                    "url": "https://www.nih.gov/diabetes",
                    "title": "Diabetes - National Institutes of Health",
                    "snippet": "Information about diabetes research, treatment, and prevention from the NIH.",
                },
            ],
            "covid": [
                {
                    "url": "https://www.cdc.gov/coronavirus/2019-ncov/index.html",
                    "title": "COVID-19 - CDC",
                    "snippet": "Latest information about COVID-19 symptoms, testing, vaccines, and prevention.",
                },
            ],
            "flu": [
                {
                    "url": "https://www.cdc.gov/flu/index.htm",
                    "title": "Influenza (Flu) - CDC",
                    "snippet": "Information about seasonal flu, including symptoms, prevention, and vaccination.",
                },
            ],
        }

        # Find best matching topic
        query_lower = query.lower()
        results = []

        for topic, topic_results in mock_database.items():
            if topic in query_lower or query_lower in topic:
                results.extend(topic_results)

        # Default fallback if no match
        if not results:
            results = [
                {
                    "url": "https://www.cdc.gov/",
                    "title": "CDC - Centers for Disease Control and Prevention",
                    "snippet": f"Reliable health information about {query}. Visit CDC.gov for more details.",
                },
                {
                    "url": "https://www.nih.gov/",
                    "title": "NIH - National Institutes of Health",
                    "snippet": f"Research and health information about {query} from the National Institutes of Health.",
                },
                {
                    "url": "https://www.mayoclinic.org/",
                    "title": "Mayo Clinic",
                    "snippet": f"Expert information about {query} from Mayo Clinic's trusted health resources.",
                },
            ]

        return results[:max_results]

    def is_trusted_source(self, url: str) -> bool:
        """
        Check if a URL is from a trusted domain.

        Args:
            url: The URL to verify

        Returns:
            True if the URL is from a trusted domain
        """
        from urllib.parse import urlparse

        try:
            domain = urlparse(url).netloc.lower()
            # Remove www. prefix
            domain = domain.replace("www.", "")

            # Check if domain or parent domain is trusted
            for trusted_domain in self.trusted_domains:
                if domain == trusted_domain or domain.endswith(f".{trusted_domain}"):
                    return True

            return False

        except Exception:
            return False


# Global source finder instance
source_finder = SourceFinder()
