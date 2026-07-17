from app.prompts.templates import TEMPLATE_MAP


class PromptBuilder:
    def build(
        self,
        template: str | None = None,
        user_prompt: str | None = None,
        tone: str | None = None,
        audience: str | None = None,
        keywords: str | None = None,
        language: str = "english",
        word_count: int | None = None,
        **kwargs,
    ) -> str:
        if template and template in TEMPLATE_MAP:
            prompt_template = TEMPLATE_MAP[template]["template"]
        elif user_prompt:
            prompt_template = user_prompt
        else:
            prompt_template = "Write about: {topic}"

        format_args = {
            "tone": tone or "professional",
            "audience": audience or "general",
            "keywords": keywords or "",
            "language": language,
            "word_count": word_count or 500,
            **kwargs,
        }

        try:
            return prompt_template.format(**format_args)
        except KeyError:
            return prompt_template

    def build_seo_prompt(self, topic: str, keywords: str | None = None, language: str = "english") -> str:
        from app.prompts.templates import SEO_METADATA

        return SEO_METADATA.format(
            topic=topic,
            keywords=keywords or "",
            language=language,
        )

    def build_rewrite_prompt(self, text: str, instruction: str = "Rewrite this text") -> str:
        return f"{instruction}\n\nText:\n{text}"

    def build_summarize_prompt(self, text: str) -> str:
        return f"Summarize the following text concisely while preserving key information:\n\n{text}"

    def build_translate_prompt(self, text: str, target_language: str) -> str:
        return f"Translate the following text to {target_language}. Preserve the tone and style:\n\n{text}"

    def build_expand_prompt(self, text: str) -> str:
        return f"Expand the following text with more details, examples, and depth:\n\n{text}"

    def build_shorten_prompt(self, text: str) -> str:
        return f"Shorten the following text while preserving the core message:\n\n{text}"

    def build_tone_change_prompt(self, text: str, new_tone: str) -> str:
        return f"Rewrite the following text in a {new_tone} tone. Maintain the original meaning:\n\n{text}"
