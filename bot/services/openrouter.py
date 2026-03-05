import logging

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from bot.config import settings

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL_PRO = "google/gemini-3-pro-image-preview"
MODEL_SIMPLE = "google/gemini-3.1-flash-image-preview"


def create_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=settings.OPENROUTER_API_KEY,
        max_retries=0,
    )


SYSTEM_PROMPT = "You are an image generation assistant. Always respond with a generated image."


async def call_model(
    client: AsyncOpenAI,
    content: list,
    model: str = MODEL_SIMPLE,
    aspect_ratio: str | None = None,
) -> ChatCompletion:
    image_config: dict = {"image_size": "2K"}
    if aspect_ratio:
        image_config["aspect_ratio"] = aspect_ratio

    logger.debug("Calling model %s | parts=%d aspect_ratio=%s", model, len(content), aspect_ratio)
    response = await client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ],
        extra_body={
            "modalities": ["image", "text"],
            "image_config": image_config,
        },
    )
    logger.debug("Model response received | finish_reason=%s", response.choices[0].finish_reason)
    return response
