"""
Duplicate checker to prevent publishing similar articles within a time window.
"""
from datetime import datetime, timedelta
from typing import List, Set
from sqlalchemy.orm import Session
from app.models.briefing import Briefing


class DuplicateChecker:
    """
    Checks if a new briefing is too similar to recently published ones.
    """

    def __init__(self, db: Session, days_lookback: int = 30):
        """
        Initialize duplicate checker.

        Args:
            db: Database session
            days_lookback: Number of days to check for duplicates (default 30)
        """
        self.db = db
        self.days_lookback = days_lookback

    def is_duplicate(
        self,
        new_title: str,
        new_tags: List[str],
        source_type: str = "article_summary",
        similarity_threshold: float = 0.6
    ) -> bool:
        """
        Check if a briefing is too similar to recent ones.

        Args:
            new_title: Title of the new briefing
            new_tags: Tags/keywords of the new briefing
            source_type: Type of briefing (article_summary or data_analysis)
            similarity_threshold: Minimum similarity to consider duplicate (0-1)

        Returns:
            True if duplicate found, False otherwise
        """
        # Get recent briefings from the last N days
        cutoff_date = datetime.utcnow() - timedelta(days=self.days_lookback)

        recent_briefings = (
            self.db.query(Briefing)
            .filter(Briefing.source_type == source_type)
            .filter(Briefing.created_at >= cutoff_date)
            .all()
        )

        if not recent_briefings:
            return False

        # Normalize new tags
        new_tags_set = self._normalize_tags(new_tags)
        new_title_words = self._extract_keywords(new_title)

        # Check each recent briefing
        for briefing in recent_briefings:
            # Compare tags
            existing_tags = self._normalize_tags(briefing.tags or [])
            tag_similarity = self._calculate_similarity(new_tags_set, existing_tags)

            # Compare title keywords
            existing_title_words = self._extract_keywords(briefing.title)
            title_similarity = self._calculate_similarity(
                new_title_words, existing_title_words
            )

            # Calculate overall similarity (weighted average)
            overall_similarity = (tag_similarity * 0.7) + (title_similarity * 0.3)

            if overall_similarity >= similarity_threshold:
                print(
                    f"Duplicate detected! New briefing similar to '{briefing.title}' "
                    f"(similarity: {overall_similarity:.2f})"
                )
                return True

        return False

    def _normalize_tags(self, tags: List[str]) -> Set[str]:
        """Normalize tags to lowercase set."""
        return {tag.lower().strip() for tag in tags if tag}

    def _extract_keywords(self, text: str) -> Set[str]:
        """Extract important keywords from text."""
        # Remove common stop words
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "up", "about", "into", "through", "during",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
            "do", "does", "did", "will", "would", "should", "could", "may", "might",
            "health", "update", "news", "briefing", "recent", "weekly", "new"
        }

        # Extract words, lowercase, remove punctuation
        import re
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = {w for w in words if w not in stop_words and len(w) > 3}

        return keywords

    def _calculate_similarity(self, set1: Set[str], set2: Set[str]) -> float:
        """Calculate Jaccard similarity between two sets."""
        if not set1 or not set2:
            return 0.0

        intersection = len(set1 & set2)
        union = len(set1 | set2)

        return intersection / union if union > 0 else 0.0


def check_for_duplicates(
    db: Session,
    title: str,
    tags: List[str],
    source_type: str = "article_summary",
    days_lookback: int = 30,
    similarity_threshold: float = 0.6
) -> bool:
    """
    Convenience function to check for duplicates.

    Returns:
        True if duplicate found, False otherwise
    """
    checker = DuplicateChecker(db, days_lookback)
    return checker.is_duplicate(title, tags, source_type, similarity_threshold)
