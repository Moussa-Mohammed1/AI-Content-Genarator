import uuid
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.content import GeneratedContent


class ContentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, content: GeneratedContent) -> GeneratedContent:
        self.db.add(content)
        await self.db.flush()
        return content

    async def get_by_id(self, content_id: uuid.UUID) -> GeneratedContent | None:
        result = await self.db.execute(select(GeneratedContent).where(GeneratedContent.id == content_id))
        return result.scalar_one_or_none()

    async def get_by_user(
        self,
        user_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        status: str | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
    ) -> tuple[list[GeneratedContent], int]:
        query = select(GeneratedContent).where(GeneratedContent.user_id == user_id)

        if search:
            query = query.where(
                or_(
                    GeneratedContent.title.ilike(f"%{search}%"),
                    GeneratedContent.generated_text.ilike(f"%{search}%"),
                )
            )

        if status:
            query = query.where(GeneratedContent.status == status)

        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar() or 0

        sort_column = getattr(GeneratedContent, sort_by, GeneratedContent.created_at)
        if sort_order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        query = query.offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def update(self, content: GeneratedContent) -> GeneratedContent:
        await self.db.flush()
        return content

    async def delete(self, content: GeneratedContent) -> None:
        await self.db.delete(content)
        await self.db.flush()

    async def get_user_stats(self, user_id: uuid.UUID) -> dict:
        total_query = select(func.count()).where(GeneratedContent.user_id == user_id)
        total_result = await self.db.execute(total_query)
        total = total_result.scalar() or 0

        favorites_query = select(func.count()).where(
            GeneratedContent.user_id == user_id, GeneratedContent.is_favorite == True
        )
        fav_result = await self.db.execute(favorites_query)
        favorites = fav_result.scalar() or 0

        recent_query = (
            select(GeneratedContent)
            .where(GeneratedContent.user_id == user_id)
            .order_by(GeneratedContent.created_at.desc())
            .limit(5)
        )
        recent_result = await self.db.execute(recent_query)
        recent = list(recent_result.scalars().all())

        return {"total": total, "favorites": favorites, "recent": recent}
