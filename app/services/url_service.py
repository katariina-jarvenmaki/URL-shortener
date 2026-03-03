# app/services/url_service.py

from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from typing import Optional

from app.db.models import URL
from app.utils.short_code import generate_short_code
from app.core.config import settings

SHORT_CODE_LENGTH = 6
MAX_GENERATION_ATTEMPTS = 5


def create_short_url(db: Session, original_url: str) -> str:
    """
    Create a shortened URL or return existing one if already present.
    """

    # 1️⃣ Check if URL already exists
    existing = db.execute(
        select(URL).where(URL.original_url == original_url)
    ).scalar_one_or_none()

    if existing:
        return f"{settings.base_url}/{existing.short_code}"

    # 2️⃣ Generate unique short code with collision handling
    for _ in range(MAX_GENERATION_ATTEMPTS):
        short_code = generate_short_code(SHORT_CODE_LENGTH)

        collision = db.execute(
            select(URL).where(URL.short_code == short_code)
        ).scalar_one_or_none()

        if not collision:
            new_url = URL(
                short_code=short_code,
                original_url=original_url,
            )
            db.add(new_url)
            db.commit()
            db.refresh(new_url)

            return f"{settings.base_url}/{new_url.short_code}"

    # If we somehow fail multiple times
    raise RuntimeError("Failed to generate unique short code")


def get_original_url(db: Session, short_code: str) -> Optional[str]:
    """
    Retrieve original URL for redirection.
    """

    url_entry = db.execute(
        select(URL).where(URL.short_code == short_code)
    ).scalar_one_or_none()

    if not url_entry:
        return None

    return url_entry.original_url


def increment_clicks(db: Session, short_code: str) -> bool:
    """
    Increment click counter and update last_accessed timestamp.
    """

    url_entry = db.execute(
        select(URL).where(URL.short_code == short_code)
    ).scalar_one_or_none()

    if not url_entry:
        return False

    url_entry.clicks += 1
    url_entry.last_accessed = datetime.utcnow()

    db.commit()
    return True


def get_stats(db: Session, short_code: str) -> Optional[dict]:
    """
    Return URL statistics.
    """

    url_entry = db.execute(
        select(URL).where(URL.short_code == short_code)
    ).scalar_one_or_none()

    if not url_entry:
        return None

    return {
        "original_url": url_entry.original_url,
        "clicks": url_entry.clicks,
        "created_at": url_entry.created_at,
        "last_accessed": url_entry.last_accessed,
    }