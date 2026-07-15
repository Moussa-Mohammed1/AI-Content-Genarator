from functools import lru_cache
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession

from app.config import get_settings


@lru_cache()
def get_engine():
    settings = get_settings()
    return create_async_engine(settings.DATABASE_URL, echo=settings.DEBUG)


@lru_cache()
def get_session_factory():
    return async_sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
