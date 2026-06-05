from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    result = await service.register(data)
    return result


@router.post("/login")
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    result = await service.login(data.email, data.password)
    return result


@router.post("/refresh")
async def refresh(refresh_token: str, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    result = await service.refresh_token(refresh_token)
    return result


@router.post("/logout")
async def logout(current_user: User = Depends(get_current_user)):
    return {"message": "Logged out successfully"}
