from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    template_id: str | None = None
    prompt: str
    title: str | None = None
    tone: str | None = None
    audience: str | None = None
    keywords: str | None = None
    language: str = "english"
    word_count: int | None = None


class GenerateResponse(BaseModel):
    id: str
    generated_text: str
    model_used: str
    tokens_used: int


class RewriteRequest(BaseModel):
    content_id: str
    text: str
    instruction: str = "Rewrite this text"


class SummarizeRequest(BaseModel):
    content_id: str | None = None
    text: str


class TranslateRequest(BaseModel):
    content_id: str | None = None
    text: str
    target_language: str = "spanish"


class SEOGenerateRequest(BaseModel):
    text: str
    topic: str
