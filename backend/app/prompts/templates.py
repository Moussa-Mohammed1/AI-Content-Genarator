BLOG_POST = """Write a {tone} blog post about {topic} targeting {audience}.
Keywords to include: {keywords}
Language: {language}
Target length: {word_count} words

Structure the post with:
- An engaging headline
- Introduction hook
- Main body with subheadings
- Conclusion with call to action

Generate the content in {language}."""

PRODUCT_DESCRIPTION = """Write a compelling product description for {product_name}.

Key features:
{features}

Target audience: {audience}
Tone: {tone}
Language: {language}

Highlight benefits, not just features. Include sensory words and persuasive language.
Generate the content in {language}."""

EMAIL_CAMPAIGN = """Write an email campaign with the goal: {goal}

Target audience: {audience}
Call to action: {cta}
Tone: {tone}
Language: {language}

Structure:
- Subject line
- Opening
- Body
- Call to action
- Signature

Write in {language}."""

SOCIAL_MEDIA = """Create a social media post for {platform} about {topic}.

Tone: {tone}
Language: {language}

Include:
- Engaging hook
- Main message
- Relevant hashtags
- Emojis where appropriate (max 3)

Write in {language}."""

LANDING_PAGE = """Write landing page copy for {product}.

Target audience: {audience}
Key benefits:
{benefits}
Primary CTA: {cta}
Tone: {tone}
Language: {language}

Structure:
- Hero headline and subheadline
- Problem statement
- Solution description
- Benefits section
- Social proof
- Call to action

Write in {language}."""

GOOGLE_ADS = """Write Google Ads copy for {topic}.

Tone: {tone}
Target audience: {audience}
Language: {language}

Include:
- 3 headline options (max 30 characters each)
- 2 description options (max 90 characters each)
- 5 keywords

Write in {language}."""

FACEBOOK_ADS = """Write Facebook Ad copy for {topic}.

Tone: {tone}
Target audience: {audience}
Language: {language}

Include:
- Primary text
- Headline
- Description
- Call to action

Write in {language}."""

LINKEDIN_POST = """Write a LinkedIn post about {topic}.

Tone: {tone}
Target audience: {audience}
Language: {language}

Structure:
- Hook
- Personal insight or story
- Value proposition
- Call to action
- 3-5 relevant hashtags

Write in {language}."""

PRESS_RELEASE = """Write a press release about {topic}.

Tone: {tone} (professional, formal)
Target audience: {audience}
Language: {language}

Structure:
- Headline
- Dateline
- Lead paragraph (who, what, when, where, why)
- Body with quotes
- Boilerplate
- Media contact information

Write in {language}."""

FAQ_SECTION = """Create an FAQ section about {topic}.

Tone: {tone}
Target audience: {audience}
Language: {language}

Include 5-8 frequently asked questions with comprehensive answers.
Format each as Q&A pair.
Write in {language}."""

YOUTUBE_DESCRIPTION = """Write a YouTube video description for a video titled {topic}.

Tone: {tone}
Target audience: {audience}
Keywords: {keywords}
Language: {language}

Include:
- Video description (2-3 paragraphs)
- Timestamps placeholder
- Links to social media
- Hashtags

Write in {language}."""

SEO_METADATA = """Generate SEO metadata for content about {topic}.

Target keywords: {keywords}
Language: {language}

Include:
- SEO Title (max 60 characters)
- Meta Description (max 160 characters)
- URL Slug
- Focus Keywords (5)
- H1 and H2 heading suggestions

Write in {language}."""

TEMPLATE_MAP = {
    "blog": {"template": BLOG_POST, "category": "blog"},
    "product_description": {"template": PRODUCT_DESCRIPTION, "category": "product"},
    "email": {"template": EMAIL_CAMPAIGN, "category": "email"},
    "social_media": {"template": SOCIAL_MEDIA, "category": "social"},
    "landing_page": {"template": LANDING_PAGE, "category": "landing"},
    "google_ads": {"template": GOOGLE_ADS, "category": "ads"},
    "facebook_ads": {"template": FACEBOOK_ADS, "category": "ads"},
    "linkedin_post": {"template": LINKEDIN_POST, "category": "social"},
    "press_release": {"template": PRESS_RELEASE, "category": "press"},
    "faq": {"template": FAQ_SECTION, "category": "faq"},
    "youtube_description": {"template": YOUTUBE_DESCRIPTION, "category": "youtube"},
    "seo_metadata": {"template": SEO_METADATA, "category": "seo"},
}
