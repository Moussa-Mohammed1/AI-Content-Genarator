import uuid
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.usage import Usage


class UsageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, usage: Usage) -> Usage:
        self.db.add(usage)
        await self.db.flush()
        return usage

    async def get_by_user(self, user_id: uuid.UUID, limit: int = 20) -> list[Usage]:
        result = await self.db.execute(
            select(Usage)
            .where(Usage.user_id == user_id)
            .order_by(Usage.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get_summary(self, user_id: uuid.UUID) -> dict:
        tokens_query = select(func.coalesce(func.sum(Usage.tokens), 0)).where(
            Usage.user_id == user_id
        )
        tokens_result = await self.db.execute(tokens_query)
        total_tokens = tokens_result.scalar() or 0

        credits_query = select(func.coalesce(func.sum(Usage.credits_used), 0)).where(
            Usage.user_id == user_id
        )
        credits_result = await self.db.execute(credits_query)
        total_credits = credits_result.scalar() or 0

        count_query = select(func.count()).where(Usage.user_id == user_id)
        count_result = await self.db.execute(count_query)
        total_generations = count_result.scalar() or 0

        recent = await self.get_by_user(user_id, 10)

        return {
            "total_tokens": total_tokens,
            "total_credits_used": total_credits,
            "total_generations": total_generations,
            "recent_usage": recent,
        }
