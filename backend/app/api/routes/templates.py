import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.template import TemplateResponse, TemplateListResponse
from app.services.template_service import TemplateService

router = APIRouter(prefix="/templates", tags=["Templates"])


@router.get("")
async def get_templates(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TemplateService(db)
    templates = await service.get_all()
    return TemplateListResponse(
        templates=[TemplateResponse.model_validate(t) for t in templates],
        total=len(templates),
    )


@router.get("/{template_id}")
async def get_template(
    template_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = TemplateService(db)
    template = await service.get_by_id(template_id)
    return TemplateResponse.model_validate(template)
