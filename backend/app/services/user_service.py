import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import ConflictError, NotFoundError, BadRequestError
from app.utils.security import hash_password, verify_password
from app.auth.jwt import create_access_token, create_refresh_token, decode_token
from app.config import get_settings

settings = get_settings()


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)

    async def register(self, data: UserCreate) -> dict:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ConflictError("Email already registered")

        user = User(
            name=data.name,
            email=data.email,
            password_hash=hash_password(data.password),
            credits=settings.DEFAULT_CREDITS,
        )
        user = await self.repo.create(user)

        return {
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "credits": user.credits,
                "subscription": user.subscription,
            },
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }

    async def login(self, email: str, password: str) -> dict:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            raise BadRequestError("Invalid email or password")

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
            "user": {
                "id": str(user.id),
                "name": user.name,
                "email": user.email,
                "credits": user.credits,
                "subscription": user.subscription,
            },
        }

    async def refresh_token(self, refresh_token: str) -> dict:
        try:
            payload = decode_token(refresh_token)
            if payload.get("type") != "refresh":
                raise BadRequestError("Invalid token type")
            user_id = uuid.UUID(payload.get("sub"))
        except Exception:
            raise BadRequestError("Invalid or expired refresh token")

        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        return {
            "access_token": create_access_token(user.id),
            "refresh_token": create_refresh_token(user.id),
        }

    async def get_profile(self, user_id: uuid.UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user

    async def update_profile(self, user_id: uuid.UUID, data: UserUpdate) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")

        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            existing = await self.repo.get_by_email(data.email)
            if existing and existing.id != user_id:
                raise ConflictError("Email already in use")
            user.email = data.email

        return await self.repo.update(user)

    async def deduct_credits(self, user_id: uuid.UUID, amount: int) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        if user.credits < amount:
            from app.core.exceptions import InsufficientCreditsError

            raise InsufficientCreditsError()
        return await self.repo.deduct_credits(user, amount)
