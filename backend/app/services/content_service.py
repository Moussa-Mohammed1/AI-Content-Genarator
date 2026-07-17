import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import GeneratedContent
from app.repositories.content_repository import ContentRepository
from app.schemas.content import ContentUpdate
from app.core.exceptions import NotFoundError, ForbiddenError


class ContentService:
    def __init__(self, db: AsyncSession):
        self.repo = ContentRepository(db)

    async def create(
        self,
        user_id: uuid.UUID,
        template_id: uuid.UUID | None,
        title: str | None,
        prompt: str,
        generated_text: str | None = None,
        model_used: str | None = None,
        tone: str | None = None,
        audience: str | None = None,
        keywords: str | None = None,
        language: str = "english",
        word_count: int | None = None,
        status: str = "draft",
    ) -> GeneratedContent:
        content = GeneratedContent(
            user_id=user_id,
            template_id=template_id,
            title=title,
            prompt=prompt,
            generated_text=generated_text,
            model_used=model_used,
            tone=tone,
            audience=audience,
            keywords=keywords,
            language=language,
            word_count=word_count,
            status=status,
        )
        return await self.repo.create(content)

    async def get_by_id(self, content_id: uuid.UUID, user_id: uuid.UUID) -> GeneratedContent:
        content = await self.repo.get_by_id(content_id)
        if not content:
            raise NotFoundError("Content not found")
        if content.user_id != user_id:
            raise ForbiddenError("Access denied")
        return content

    async def get_user_contents(
        self,
        user_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        status: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> dict:
        contents, total = await self.repo.get_by_user(
            user_id, page, page_size, search, status, sort_by, sort_order
        )
        return {
            "contents": contents,
            "total": total,
            "page": page,
            "page_size": page_size,
        }

    async def update(self, content_id: uuid.UUID, user_id: uuid.UUID, data: ContentUpdate) -> GeneratedContent:
        content = await self.get_by_id(content_id, user_id)

        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(content, key, value)

        return await self.repo.update(content)

    async def delete(self, content_id: uuid.UUID, user_id: uuid.UUID) -> None:
        content = await self.get_by_id(content_id, user_id)
        await self.repo.delete(content)

    async def get_user_stats(self, user_id: uuid.UUID) -> dict:
        return await self.repo.get_user_stats(user_id)
