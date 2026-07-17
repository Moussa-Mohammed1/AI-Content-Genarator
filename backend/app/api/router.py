from fastapi import APIRouter

from  app.api.routes.auth import router as auth_router
from  app.api.routes.templates import router as templates_router
from  app.api.routes.generation import router as generation_router
from  app.api.routes.content import router as content_router
from  app.api.routes.profile import router as profile_router
from  app.api.routes.usage import router as usage_router

api_router = APIRouter(prefix="/api")

api_router.include_router(auth_router)
api_router.include_router(templates_router)
api_router.include_router(generation_router)
api_router.include_router(content_router)
api_router.include_router(profile_router)
api_router.include_router(usage_router)
