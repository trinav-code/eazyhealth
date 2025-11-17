"""
Configuration management for EazyHealth AI.
Loads environment variables and provides app-wide settings.
"""
import os
from enum import Enum
from typing import Optional
from pydantic_settings import BaseSettings


class ReadingLevel(str, Enum):
    """Supported reading comprehension levels."""
    GRADE_3 = "grade3"
    GRADE_6 = "grade6"
    GRADE_8 = "grade8"
    HIGH_SCHOOL = "high_school"
    COLLEGE = "college"


class BriefingSourceType(str, Enum):
    """Types of briefing sources."""
    DATA_ANALYSIS = "data_analysis"
    ARTICLE_SUMMARY = "article_summary"


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # App settings
    app_name: str = "EazyHealth AI"
    app_version: str = "0.1.0"
    debug: bool = False

    # Database
    database_url: str = "sqlite:///./eazyhealth.db"

    # LLM Provider Settings
    llm_provider: str = "anthropic"  # "anthropic" or "openai"
    anthropic_api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    llm_model: str = "claude-3-5-sonnet-20241022"  # or gpt-4, etc.
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.7

    # Search API Settings (for source discovery)
    search_provider: str = "brave"  # "brave", "serper", or "mock"
    brave_api_key: Optional[str] = None
    serper_api_key: Optional[str] = None

    # Trusted Sources (comma-separated domains)
    trusted_domains: str = "cdc.gov,nih.gov,who.int,mayoclinic.org,hopkinsmedicine.org,health.harvard.edu,webmd.com,medlineplus.gov"

    # Rate Limiting
    rate_limit_per_minute: int = 10

    # CORS
    cors_origins: str = "http://localhost:5173,http://localhost:3000"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Global settings instance
settings = Settings()


def get_trusted_domains() -> list[str]:
    """Parse trusted domains from settings."""
    return [domain.strip() for domain in settings.trusted_domains.split(",") if domain.strip()]


# Reading level descriptions for prompts
READING_LEVEL_PROMPTS = {
    ReadingLevel.GRADE_3: "Use very simple words (3-4 letters), short sentences (5-8 words), and explain every term. Write as if explaining to an 8-year-old.",
    ReadingLevel.GRADE_6: "Use simple language, short sentences (8-12 words), and avoid jargon. Explain medical terms when used. Write at a middle school level.",
    ReadingLevel.GRADE_8: "Use clear, straightforward language with sentences of moderate length. Define technical terms but can use more health vocabulary. Write at an 8th-grade level.",
    ReadingLevel.HIGH_SCHOOL: "Use standard vocabulary including common medical terminology. Sentences can be longer and more complex. Assume basic health literacy.",
    ReadingLevel.COLLEGE: "Use advanced vocabulary and medical terminology freely. Complex sentence structures are acceptable. Assume college-level health knowledge.",
}
