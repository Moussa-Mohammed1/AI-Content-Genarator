import uuid
from datetime import datetime
from pydantic import BaseModel, Field


class TemplateResponse(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    category: str | None
    prompt_template: str
    icon: str | None
    is_favorite: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class TemplateListResponse(BaseModel):
    templates: list[TemplateResponse]
    total: int
