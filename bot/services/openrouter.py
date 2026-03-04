import logging

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from bot.config import settings

logger = logging.getLogger(__name__)

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
MODEL = "google/gemini-3.1-flash-image-preview"


def create_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        base_url=OPENROUTER_BASE_URL,
        api_key=settings.OPENROUTER_API_KEY,
    )


async def call_model(client: AsyncOpenAI, content: list) -> ChatCompletion:
    logger.debug("Calling model %s | parts=%d", MODEL, len(content))
    response = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": content}],
    )
    logger.debug("Model response received | finish_reason=%s", response.choices[0].finish_reason)
    return response
