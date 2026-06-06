from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("")
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)


@router.put("")
async def update_profile(
    data: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    service = UserService(db)
    user = await service.update_profile(current_user.id, data)
    return UserResponse.model_validate(user)
