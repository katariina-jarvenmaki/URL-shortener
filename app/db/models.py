# app/db/models.py

from sqlalchemy import String, Integer, DateTime, func, Index
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.base import Base
from typing import Optional

class URL(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    short_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
        index=True
    )

    original_url: Mapped[str] = mapped_column(
        String(2048),
        nullable=False,
        index=True
    )

    clicks: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    last_accessed: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Additional compound index for faster lookups
    __table_args__ = (
        Index("idx_short_original", "short_code", "original_url"),
    )

    def __repr__(self) -> str:
        return (
            f"<URL(id={self.id}, short_code='{self.short_code}', "
            f"original_url='{self.original_url}', clicks={self.clicks})>"
        )