# app/api/routes.py

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.url import (
    URLCreate,
    URLResponse,
    URLStatsResponse,
    MessageResponse,
)
from app.services import url_service


router = APIRouter()


@router.get("/", response_model=MessageResponse)
def home():
    return {"message": "URL Shortener API"}


@router.post("/shorten", response_model=URLResponse)
def shorten_url(
    request: URLCreate,
    db: Session = Depends(get_db),
):
    normalized_url = str(request.url).rstrip("/")
    short_url = url_service.create_short_url(db, normalized_url)
    return {"short_url": short_url}


@router.get("/health")
def health():
    return {"message": "healthy"}


@router.get("/{short_code}")
def redirect_to_url(
    short_code: str,
    db: Session = Depends(get_db),
):
    original_url = url_service.get_original_url(db, short_code)

    if not original_url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shortened URL not found",
        )

    url_service.increment_clicks(db, short_code)

    return RedirectResponse(url=original_url)


@router.get("/stats/{short_code}", response_model=URLStatsResponse)
def get_url_stats(
    short_code: str,
    db: Session = Depends(get_db),
):
    stats = url_service.get_stats(db, short_code)

    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="URL stats not found",
        )

    return stats
