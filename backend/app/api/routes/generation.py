import uuid
import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import get_current_user
from app.dependencies.database import get_db
from app.models.user import User
from app.schemas.generation import (
    GenerateRequest,
    GenerateResponse,
    RewriteRequest,
    SummarizeRequest,
    TranslateRequest,
    SEOGenerateRequest,
)
from app.services.ai_service import AIService
from app.services.prompt_builder import PromptBuilder
from app.services.content_service import ContentService
from app.services.usage_service import UsageService
from app.services.user_service import UserService
from app.core.exceptions import InsufficientCreditsError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/generate", tags=["Generation"])

CREDITS_PER_GENERATION = 1
CREDITS_PER_1000_TOKENS = 1


def estimate_tokens(text: str) -> int:
    return len(text.split()) * 1.3


@router.post("")
async def generate_content(
    request: GenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    prompt_builder = PromptBuilder()
    ai_service = AIService()
    content_service = ContentService(db)
    usage_service = UsageService(db)
    user_service = UserService(db)

    if current_user.credits < CREDITS_PER_GENERATION:
        raise InsufficientCreditsError()

    built_prompt = prompt_builder.build(
        template=request.template_id,
        user_prompt=request.prompt,
        tone=request.tone,
        audience=request.audience,
        keywords=request.keywords,
        language=request.language,
        word_count=request.word_count,
    )

    generated_text = await ai_service.generate(built_prompt)
    tokens_used = int(estimate_tokens(built_prompt) + estimate_tokens(generated_text))
    credits_used = max(CREDITS_PER_GENERATION, tokens_used // 1000 * CREDITS_PER_1000_TOKENS)

    template_uuid = None
    if request.template_id:
        try:
            from app.prompts.templates import TEMPLATE_MAP

            if request.template_id in TEMPLATE_MAP:
                pass
            template_uuid = uuid.UUID(request.template_id)
        except (ValueError, KeyError):
            template_uuid = None

    content = await content_service.create(
        user_id=current_user.id,
        template_id=template_uuid,
        title=request.title or "Untitled",
        prompt=request.prompt,
        generated_text=generated_text,
        model_used=ai_service.provider_name,
        tone=request.tone,
        audience=request.audience,
        keywords=request.keywords,
        language=request.language,
        word_count=request.word_count,
        status="completed",
    )

    await user_service.deduct_credits(current_user.id, credits_used)
    await usage_service.record_usage(current_user.id, tokens_used, credits_used, "generate")

    return GenerateResponse(
        id=str(content.id),
        generated_text=generated_text,
        model_used=ai_service.provider_name,
        tokens_used=tokens_used,
    )


@router.post("/rewrite")
async def rewrite_content(
    request: RewriteRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ai_service = AIService()
    usage_service = UsageService(db)
    user_service = UserService(db)

    if current_user.credits < CREDITS_PER_GENERATION:
        raise InsufficientCreditsError()

    generated_text = await ai_service.rewrite(request.text, request.instruction)
    tokens_used = int(estimate_tokens(request.text) + estimate_tokens(generated_text))

    await user_service.deduct_credits(current_user.id, CREDITS_PER_GENERATION)
    await usage_service.record_usage(current_user.id, tokens_used, CREDITS_PER_GENERATION, "rewrite")

    return {"generated_text": generated_text, "model_used": ai_service.provider_name}


@router.post("/summarize")
async def summarize_content(
    request: SummarizeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ai_service = AIService()
    usage_service = UsageService(db)
    user_service = UserService(db)

    if current_user.credits < CREDITS_PER_GENERATION:
        raise InsufficientCreditsError()

    generated_text = await ai_service.summarize(request.text)
    tokens_used = int(estimate_tokens(request.text) + estimate_tokens(generated_text))

    await user_service.deduct_credits(current_user.id, CREDITS_PER_GENERATION)
    await usage_service.record_usage(current_user.id, tokens_used, CREDITS_PER_GENERATION, "summarize")

    return {"generated_text": generated_text, "model_used": ai_service.provider_name}


@router.post("/translate")
async def translate_content(
    request: TranslateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ai_service = AIService()
    usage_service = UsageService(db)
    user_service = UserService(db)

    if current_user.credits < CREDITS_PER_GENERATION:
        raise InsufficientCreditsError()

    generated_text = await ai_service.translate(request.text, request.target_language)
    tokens_used = int(estimate_tokens(request.text) + estimate_tokens(generated_text))

    await user_service.deduct_credits(current_user.id, CREDITS_PER_GENERATION)
    await usage_service.record_usage(current_user.id, tokens_used, CREDITS_PER_GENERATION, "translate")

    return {"generated_text": generated_text, "model_used": ai_service.provider_name}


@router.post("/seo")
async def generate_seo(
    request: SEOGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    ai_service = AIService()
    content_service = ContentService(db)
    usage_service = UsageService(db)
    user_service = UserService(db)

    if current_user.credits < CREDITS_PER_GENERATION:
        raise InsufficientCreditsError()

    seo_data = await ai_service.improve_seo(request.text, request.topic)
    tokens_used = int(estimate_tokens(request.text))

    await user_service.deduct_credits(current_user.id, CREDITS_PER_GENERATION)
    await usage_service.record_usage(current_user.id, tokens_used, CREDITS_PER_GENERATION, "seo")

    return seo_data
