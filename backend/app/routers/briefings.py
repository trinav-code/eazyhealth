"""
Briefings API router for auto-generated health briefings.
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.config import ReadingLevel, BriefingSourceType
from app.database import get_db
from app.models.briefing import Briefing
from app.services.briefing_generator import briefing_generator

router = APIRouter(prefix="/api", tags=["Briefings"])


class BriefingListItem(BaseModel):
    """Brief briefing info for list view."""
    id: int
    title: str
    slug: str
    summary: str
    source_type: str
    tags: List[str]
    reading_level: str
    created_at: str


class BriefingListResponse(BaseModel):
    """Response for briefing list."""
    items: List[BriefingListItem]
    total: int


class BriefingDetailResponse(BaseModel):
    """Full briefing detail."""
    id: int
    title: str
    slug: str
    summary: str
    body: str
    source_type: str
    source_urls: List[str]
    source_metadata: Dict[str, Any]
    tags: List[str]
    charts: List[Dict[str, Any]]
    reading_level: str
    created_at: str
    disclaimer: str


class GenerateBriefingRequest(BaseModel):
    """Request to generate a new briefing."""
    source_type: BriefingSourceType = Field(
        description="Type of briefing to generate"
    )
    topic: Optional[str] = Field(
        None,
        description="Topic for article_summary briefings"
    )
    disease_stats: Optional[Dict[str, Any]] = Field(
        None,
        description="Disease statistics for data_analysis briefings"
    )
    reading_level: ReadingLevel = Field(
        ReadingLevel.GRADE_8,
        description="Target reading level"
    )
    use_mock_data: bool = Field(
        False,
        description="Use mock data for demo purposes"
    )


class GenerateBriefingResponse(BaseModel):
    """Response after generating a briefing."""
    created: bool
    briefing: BriefingListItem


@router.get("/briefings", response_model=BriefingListResponse)
async def list_briefings(
    limit: int = Query(10, ge=1, le=50, description="Number of briefings to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    source_type: Optional[BriefingSourceType] = Query(None, description="Filter by source type"),
    db: Session = Depends(get_db)
) -> BriefingListResponse:
    """
    List all briefings with pagination and filtering.
    """
    try:
        query = db.query(Briefing)

        # Filter by source type if specified
        if source_type:
            query = query.filter(Briefing.source_type == source_type.value)

        # Get total count
        total = query.count()

        # Apply pagination and ordering
        briefings = (
            query
            .order_by(desc(Briefing.created_at))
            .offset(offset)
            .limit(limit)
            .all()
        )

        items = [
            BriefingListItem(
                id=b.id,
                title=b.title,
                slug=b.slug,
                summary=b.summary,
                source_type=b.source_type,
                tags=b.tags or [],
                reading_level=b.reading_level,
                created_at=b.created_at.isoformat() if b.created_at else "",
            )
            for b in briefings
        ]

        return BriefingListResponse(items=items, total=total)

    except Exception as e:
        print(f"Error listing briefings: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve briefings: {str(e)}"
        )


@router.get("/briefings/{slug}", response_model=BriefingDetailResponse)
async def get_briefing(
    slug: str,
    db: Session = Depends(get_db)
) -> BriefingDetailResponse:
    """
    Get a specific briefing by slug.
    """
    try:
        briefing = db.query(Briefing).filter(Briefing.slug == slug).first()

        if not briefing:
            raise HTTPException(
                status_code=404,
                detail=f"Briefing not found: {slug}"
            )

        return BriefingDetailResponse(
            id=briefing.id,
            title=briefing.title,
            slug=briefing.slug,
            summary=briefing.summary,
            body=briefing.body,
            source_type=briefing.source_type,
            source_urls=briefing.source_urls or [],
            source_metadata=briefing.source_metadata or {},
            tags=briefing.tags or [],
            charts=briefing.charts or [],
            reading_level=briefing.reading_level,
            created_at=briefing.created_at.isoformat() if briefing.created_at else "",
            disclaimer=briefing.disclaimer,
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting briefing {slug}: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve briefing: {str(e)}"
        )


@router.post("/briefings/generate", response_model=GenerateBriefingResponse)
async def generate_briefing(
    request: GenerateBriefingRequest,
    db: Session = Depends(get_db)
) -> GenerateBriefingResponse:
    """
    Generate a new auto-briefing.

    Can generate from:
    - Disease data analysis (provide disease_stats or use_mock_data=true)
    - Article summaries (provide topic)
    """
    try:
        briefing_data = None

        # Generate based on source type
        if request.source_type == BriefingSourceType.DATA_ANALYSIS:
            if request.use_mock_data:
                briefing_data = briefing_generator.generate_mock_data_briefing(
                    reading_level=request.reading_level
                )
            elif request.disease_stats:
                briefing_data = briefing_generator.generate_data_analysis_briefing(
                    disease_stats=request.disease_stats,
                    reading_level=request.reading_level
                )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Either 'disease_stats' or 'use_mock_data=true' must be provided for data_analysis"
                )

        elif request.source_type == BriefingSourceType.ARTICLE_SUMMARY:
            if not request.topic:
                raise HTTPException(
                    status_code=400,
                    detail="'topic' must be provided for article_summary briefings"
                )

            briefing_data = briefing_generator.generate_article_summary_briefing(
                topic=request.topic,
                reading_level=request.reading_level,
                max_articles=3
            )

        if not briefing_data:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate briefing data"
            )

        # Save to database
        briefing = Briefing(**briefing_data)
        db.add(briefing)
        db.commit()
        db.refresh(briefing)

        return GenerateBriefingResponse(
            created=True,
            briefing=BriefingListItem(
                id=briefing.id,
                title=briefing.title,
                slug=briefing.slug,
                summary=briefing.summary,
                source_type=briefing.source_type,
                tags=briefing.tags or [],
                reading_level=briefing.reading_level,
                created_at=briefing.created_at.isoformat() if briefing.created_at else "",
            )
        )

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error generating briefing: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate briefing: {str(e)}"
        )
