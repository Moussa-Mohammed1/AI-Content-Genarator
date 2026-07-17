import uuid
from datetime import datetime
from pydantic import BaseModel


class UsageResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    tokens: int
    credits_used: int
    action: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class UsageSummaryResponse(BaseModel):
    total_tokens: int
    total_credits_used: int
    total_generations: int
    recent_usage: list[UsageResponse]
