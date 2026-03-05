# app/schemas/url.py

from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional


class URLCreate(BaseModel):
    url: HttpUrl


class URLResponse(BaseModel):
    short_url: str


class URLStatsResponse(BaseModel):
    original_url: str
    clicks: int
    created_at: datetime
    last_accessed: Optional[datetime]
    

class MessageResponse(BaseModel):
    message: str