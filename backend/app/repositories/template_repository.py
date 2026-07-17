import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.template import Template


class TemplateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[Template]:
        result = await self.db.execute(select(Template).order_by(Template.name))
        return list(result.scalars().all())

    async def get_by_id(self, template_id: uuid.UUID) -> Template | None:
        result = await self.db.execute(select(Template).where(Template.id == template_id))
        return result.scalar_one_or_none()

    async def get_by_category(self, category: str) -> list[Template]:
        result = await self.db.execute(
            select(Template).where(Template.category == category).order_by(Template.name)
        )
        return list(result.scalars().all())
