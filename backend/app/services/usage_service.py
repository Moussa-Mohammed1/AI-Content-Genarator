import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usage import Usage
from app.repositories.usage_repository import UsageRepository


class UsageService:
    def __init__(self, db: AsyncSession):
        self.repo = UsageRepository(db)

    async def record_usage(
        self,
        user_id: uuid.UUID,
        tokens: int,
        credits_used: int,
        action: str | None = None,
    ) -> Usage:
        usage = Usage(
            user_id=user_id,
            tokens=tokens,
            credits_used=credits_used,
            action=action,
        )
        return await self.repo.create(usage)

    async def get_usage_summary(self, user_id: uuid.UUID) -> dict:
        return await self.repo.get_summary(user_id)
