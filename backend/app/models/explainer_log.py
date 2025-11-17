"""
ExplainerLog model for tracking on-demand explainer queries.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base


class ExplainerLog(Base):
    """
    Model for logging on-demand explainer requests.

    Helps track usage, popular queries, and improves future responses.
    """
    __tablename__ = "explainer_logs"

    id = Column(Integer, primary_key=True, index=True)

    # User input
    query = Column(Text, nullable=True)  # Free-form question
    source_url = Column(String(2000), nullable=True)  # URL provided by user
    input_excerpt = Column(Text, nullable=True)  # First 500 chars of raw text or extracted article

    # Sources found by the system
    sources_found = Column(JSON, nullable=True)  # List of {url, title, excerpt} dicts

    # Reading level requested
    reading_level = Column(String(20), nullable=False, default="grade6")

    # Generated output
    output_json = Column(JSON, nullable=False)  # Full explainer response with sections

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "query": self.query,
            "source_url": self.source_url,
            "sources_found": self.sources_found or [],
            "reading_level": self.reading_level,
            "output_json": self.output_json,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
