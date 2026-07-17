import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Boolean, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class GeneratedContent(Base):
    __tablename__ = "generated_contents"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    template_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("templates.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(500), nullable=True)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    generated_text: Mapped[str] = mapped_column(Text, nullable=True)
    model_used: Mapped[str] = mapped_column(String(100), nullable=True)
    tone: Mapped[str] = mapped_column(String(50), nullable=True)
    audience: Mapped[str] = mapped_column(String(255), nullable=True)
    keywords: Mapped[str] = mapped_column(String(500), nullable=True)
    language: Mapped[str] = mapped_column(String(50), default="english")
    word_count: Mapped[int] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="draft")
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    seo_title: Mapped[str] = mapped_column(String(500), nullable=True)
    seo_meta_description: Mapped[str] = mapped_column(Text, nullable=True)
    seo_url_slug: Mapped[str] = mapped_column(String(500), nullable=True)
    seo_keywords: Mapped[str] = mapped_column(String(500), nullable=True)
    seo_headings: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="contents")
    template = relationship("Template", back_populates="contents")
