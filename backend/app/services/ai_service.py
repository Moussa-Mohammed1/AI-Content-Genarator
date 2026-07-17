import logging
from abc import ABC, abstractmethod

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AIProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass


class OpenAIProvider(AIProvider):
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.AI_MODEL

    @property
    def name(self) -> str:
        return f"openai/{self.model}"

    async def generate(self, prompt: str, **kwargs) -> str:
        from openai import AsyncOpenAI

        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.chat.completions.create(
            model=kwargs.get("model", self.model),
            messages=[{"role": "user", "content": prompt}],
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 4000),
        )
        return response.choices[0].message.content or ""


class GeminiProvider(AIProvider):
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY

    @property
    def name(self) -> str:
        return "gemini"

    async def generate(self, prompt: str, **kwargs) -> str:
        import httpx

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={self.api_key}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]


class AnthropicProvider(AIProvider):
    def __init__(self):
        self.api_key = settings.ANTHROPIC_API_KEY

    @property
    def name(self) -> str:
        return "anthropic/claude"

    async def generate(self, prompt: str, **kwargs) -> str:
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": self.api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": "claude-3-haiku-20240307",
                    "max_tokens": 4000,
                    "messages": [{"role": "user", "content": prompt}],
                },
            )
            data = response.json()
            return data["content"][0]["text"]


class DeepSeekProvider(AIProvider):
    def __init__(self):
        self.api_key = settings.DEEPSEEK_API_KEY

    @property
    def name(self) -> str:
        return "deepseek"

    async def generate(self, prompt: str, **kwargs) -> str:
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": kwargs.get("temperature", 0.7),
                },
            )
            data = response.json()
            return data["choices"][0]["message"]["content"]


class OllamaProvider(AIProvider):
    def __init__(self):
        self.base_url = settings.OLLAMA_BASE_URL

    @property
    def name(self) -> str:
        return "ollama"

    async def generate(self, prompt: str, **kwargs) -> str:
        import httpx

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": kwargs.get("model", "llama3"),
                    "prompt": prompt,
                    "stream": False,
                },
            )
            data = response.json()
            return data.get("response", "")


class AIService:
    def __init__(self, provider: str | None = None):
        self._provider = self._create_provider(provider or settings.DEFAULT_AI_PROVIDER)

    def _create_provider(self, provider: str) -> AIProvider:
        providers = {
            "openai": OpenAIProvider,
            "gemini": GeminiProvider,
            "anthropic": AnthropicProvider,
            "deepseek": DeepSeekProvider,
            "ollama": OllamaProvider,
        }
        provider_cls = providers.get(provider)
        if not provider_cls:
            logger.warning(f"Unknown provider '{provider}', falling back to OpenAI")
            provider_cls = OpenAIProvider
        return provider_cls()

    @property
    def provider_name(self) -> str:
        return self._provider.name

    async def generate(self, prompt: str, **kwargs) -> str:
        return await self._provider.generate(prompt, **kwargs)

    async def rewrite(self, text: str, instruction: str = "Rewrite this text") -> str:
        prompt = f"{instruction}\n\nText:\n{text}"
        return await self._provider.generate(prompt)

    async def summarize(self, text: str) -> str:
        prompt = f"Summarize the following text concisely while preserving key information:\n\n{text}"
        return await self._provider.generate(prompt)

    async def translate(self, text: str, target_language: str) -> str:
        prompt = f"Translate the following text to {target_language}. Preserve the tone and style:\n\n{text}"
        return await self._provider.generate(prompt)

    async def expand(self, text: str) -> str:
        prompt = f"Expand the following text with more details, examples, and depth:\n\n{text}"
        return await self._provider.generate(prompt)

    async def shorten(self, text: str) -> str:
        prompt = f"Shorten the following text while preserving the core message:\n\n{text}"
        return await self._provider.generate(prompt)

    async def improve_seo(self, text: str, topic: str) -> dict:
        prompt = f"""Analyze and improve the SEO of the following content about '{topic}'.

Generate:
1. SEO Title (max 60 chars)
2. Meta Description (max 160 chars)
3. URL Slug
4. Focus Keywords (5)
5. H1/H2 Suggestions

Content:
{text}

Return as a JSON object with keys: seo_title, meta_description, url_slug, keywords, headings"""
        result = await self._provider.generate(prompt)
        import json

        try:
            parsed = json.loads(result)
            return {
                "seo_title": parsed.get("seo_title", ""),
                "meta_description": parsed.get("meta_description", ""),
                "url_slug": parsed.get("url_slug", ""),
                "keywords": parsed.get("keywords", ""),
                "headings": parsed.get("headings", ""),
            }
        except json.JSONDecodeError:
            return {
                "seo_title": "",
                "meta_description": "",
                "url_slug": "",
                "keywords": "",
                "headings": result,
            }

    async def change_tone(self, text: str, new_tone: str) -> str:
        prompt = f"Rewrite the following text in a {new_tone} tone. Maintain the original meaning:\n\n{text}"
        return await self._provider.generate(prompt)

    async def generate_outline(self, topic: str, keywords: str | None = None) -> str:
        prompt = f"Create a detailed outline for content about: {topic}\nKeywords: {keywords or ''}"
        return await self._provider.generate(prompt)

    async def generate_meta_description(self, text: str) -> str:
        prompt = f"Generate a compelling meta description (max 160 characters) for:\n\n{text}"
        return await self._provider.generate(prompt)

    async def generate_title(self, text: str) -> str:
        prompt = f"Generate an engaging title for the following content:\n\n{text}"
        return await self._provider.generate(prompt)
