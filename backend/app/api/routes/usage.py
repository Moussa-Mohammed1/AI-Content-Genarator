from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.usage import UsageSummaryResponse
from app.services.usage_service import UsageService
from app.repositories.usage_repository import UsageRepository

router = APIRouter(prefix="/usage", tags=["Usage"])


@router.get("")
async def get_usage(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UsageService(db)
    summary = await service.get_usage_summary(current_user.id)
    return UsageSummaryResponse(
        total_tokens=summary["total_tokens"],
        total_credits_used=summary["total_credits_used"],
        total_generations=summary["total_generations"],
        recent_usage=summary["recent_usage"],
    )
