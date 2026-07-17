import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.template_repository import TemplateRepository
from app.core.exceptions import NotFoundError


class TemplateService:
    def __init__(self, db: AsyncSession):
        self.repo = TemplateRepository(db)

    async def get_all(self) -> list:
        templates = await self.repo.get_all()
        return templates

    async def get_by_id(self, template_id: uuid.UUID):
        template = await self.repo.get_by_id(template_id)
        if not template:
            raise NotFoundError("Template not found")
        return template

    async def get_by_category(self, category: str) -> list:
        return await self.repo.get_by_category(category)
