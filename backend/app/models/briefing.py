"""
Briefing model for auto-generated health briefings.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base


class Briefing(Base):
    """
    Model for auto-generated health briefings.

    Briefings can be either:
    - Data analysis posts (analyzing disease trends)
    - Article summaries (summarizing recent health news)
    """
    __tablename__ = "briefings"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False)
    slug = Column(String(500), unique=True, nullable=False, index=True)
    summary = Column(Text, nullable=False)  # Short summary for preview
    body = Column(Text, nullable=False)  # Full content (markdown or HTML)

    # Source tracking
    source_type = Column(String(50), nullable=False)  # "data_analysis" or "article_summary"
    source_urls = Column(JSON, nullable=True)  # List of source URLs if article_summary
    source_metadata = Column(JSON, nullable=True)  # Additional metadata (disease codes, locations, etc.)

    # Organization
    tags = Column(JSON, nullable=True)  # List of tags like ["covid", "flu", "respiratory"]

    # Charts and visualizations (optional, for future)
    charts = Column(JSON, nullable=True)  # List of chart metadata

    # Reading level used to generate this briefing
    reading_level = Column(String(20), nullable=False, default="grade8")

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Disclaimer (always included)
    disclaimer = Column(Text, nullable=False, default="This information is for general educational purposes only and is not medical advice. Please consult a healthcare professional for personalized medical guidance.")

    def to_dict(self, include_body: bool = False):
        """Convert to dictionary for API responses."""
        result = {
            "id": self.id,
            "title": self.title,
            "slug": self.slug,
            "summary": self.summary,
            "source_type": self.source_type,
            "tags": self.tags or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "reading_level": self.reading_level,
        }

        if include_body:
            result.update({
                "body": self.body,
                "source_urls": self.source_urls or [],
                "source_metadata": self.source_metadata or {},
                "charts": self.charts or [],
                "disclaimer": self.disclaimer,
            })

        return result
