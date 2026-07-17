import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class ContentResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    template_id: uuid.UUID | None
    title: str | None
    prompt: str
    generated_text: str | None
    model_used: str | None
    tone: str | None
    audience: str | None
    keywords: str | None
    language: str | None
    word_count: int | None
    status: str
    is_favorite: bool
    seo_title: str | None
    seo_meta_description: str | None
    seo_url_slug: str | None
    seo_keywords: str | None
    seo_headings: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ContentUpdate(BaseModel):
    title: str | None = None
    generated_text: str | None = None
    status: str | None = None
    is_favorite: bool | None = None
    seo_title: str | None = None
    seo_meta_description: str | None = None
    seo_url_slug: str | None = None
    seo_keywords: str | None = None
    seo_headings: str | None = None


class ContentListResponse(BaseModel):
    contents: list[ContentResponse]
    total: int
    page: int
    page_size: int
