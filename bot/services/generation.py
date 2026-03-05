import base64
import logging

from openai.types.chat import ChatCompletion

from bot.services.openrouter import MODEL_SIMPLE, call_model, create_client

logger = logging.getLogger(__name__)

MAX_IMAGES = 3


def build_text_part(prompt: str) -> dict:
    return {"type": "text", "text": prompt}


def build_image_part(image_bytes: bytes) -> dict:
    encoded = base64.b64encode(image_bytes).decode("utf-8")
    return {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}}


def build_content(prompt: str, images: list[bytes]) -> list[dict]:
    parts: list[dict] = [build_text_part(prompt)]
    for img in images[:MAX_IMAGES]:
        parts.append(build_image_part(img))
    return parts


def extract_image(response: ChatCompletion) -> bytes:
    # Images are returned in message.images (OpenRouter-specific field)
    message = response.choices[0].message
    images = (message.model_extra or {}).get("images") or []
    for img in images:
        url = img.get("image_url", {}).get("url", "")
        if url.startswith("data:"):
            _, data = url.split(",", 1)
            return base64.b64decode(data)
    raise ValueError(
        f"No image found in model response. "
        f"finish_reason={response.choices[0].finish_reason!r} "
        f"images={images!r} "
        f"content={message.content!r} "
        f"model_extra={message.model_extra!r}"
    )


def format_usage(response: ChatCompletion) -> str | None:
    usage = response.usage
    if usage is None:
        return None
    parts = [f"🔢 {usage.total_tokens} tokens ({usage.prompt_tokens} in / {usage.completion_tokens} out)"]
    # OpenRouter may include cost in usage.model_extra
    extra = usage.model_extra or {}
    cost = extra.get("cost")
    if cost is not None:
        parts.append(f"💰 ${cost:.4f}")
    return " · ".join(parts)


async def generate_image(
    prompt: str,
    images: list[bytes],
    model: str | None = None,
    aspect_ratio: str | None = None,
) -> tuple[bytes, str | None]:
    model = model or MODEL_SIMPLE
    logger.info(
        "Generating image | prompt=%r images=%d model=%s aspect_ratio=%s",
        prompt[:80], len(images), model, aspect_ratio,
    )
    client = create_client()
    content = build_content(prompt, images)
    response = await call_model(client, content, model=model, aspect_ratio=aspect_ratio)
    img = extract_image(response)
    usage_text = format_usage(response)
    logger.info("Image generated | size=%d bytes usage=%s", len(img), usage_text)
    return img, usage_text
