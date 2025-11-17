"""
TrustedSource model for managing credible health information sources.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from app.database import Base


class TrustedSource(Base):
    """
    Model for tracking trusted health information sources.

    Used to whitelist/verify sources before summarizing them.
    """
    __tablename__ = "trusted_sources"

    id = Column(Integer, primary_key=True, index=True)

    # Source identification
    domain = Column(String(255), unique=True, nullable=False, index=True)  # e.g., "cdc.gov"
    name = Column(String(500), nullable=False)  # e.g., "Centers for Disease Control and Prevention"
    description = Column(Text, nullable=True)

    # Trust metadata
    category = Column(String(100), nullable=True)  # e.g., "government", "academic", "medical_institution"
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        """Convert to dictionary for API responses."""
        return {
            "id": self.id,
            "domain": self.domain,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "is_active": self.is_active,
        }
