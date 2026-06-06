import uuid
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.content import ContentResponse, ContentUpdate, ContentListResponse
from app.services.content_service import ContentService

router = APIRouter(prefix="/contents", tags=["Content"])


@router.get("")
async def get_contents(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = None,
    status: str | None = None,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ContentService(db)
    result = await service.get_user_contents(
        current_user.id, page, page_size, search, status, sort_by, sort_order
    )
    return ContentListResponse(
        contents=[ContentResponse.model_validate(c) for c in result["contents"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
    )


@router.get("/{content_id}")
async def get_content(
    content_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ContentService(db)
    content = await service.get_by_id(content_id, current_user.id)
    return ContentResponse.model_validate(content)


@router.put("/{content_id}")
async def update_content(
    content_id: uuid.UUID,
    data: ContentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ContentService(db)
    content = await service.update(content_id, current_user.id, data)
    return ContentResponse.model_validate(content)


@router.delete("/{content_id}")
async def delete_content(
    content_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ContentService(db)
    await service.delete(content_id, current_user.id)
    return {"message": "Content deleted successfully"}


@router.get("/stats/summary")
async def get_content_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = ContentService(db)
    return await service.get_user_stats(current_user.id)
