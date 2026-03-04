import base64

from openai.types.chat import ChatCompletion

from bot.services.openrouter import call_model, create_client

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
    content = response.choices[0].message.content
    if isinstance(content, str):
        raise ValueError("Expected structured content with image_url parts, got plain string")
    for part in content:
        if isinstance(part, dict):
            if part.get("type") == "image_url":
                url = part["image_url"]["url"]
                if url.startswith("data:"):
                    _, data = url.split(",", 1)
                    return base64.b64decode(data)
        else:
            # Handle SDK content block objects
            if getattr(part, "type", None) == "image_url":
                url = part.image_url.url
                if url.startswith("data:"):
                    _, data = url.split(",", 1)
                    return base64.b64decode(data)
    raise ValueError("No image found in model response")


async def generate_image(prompt: str, images: list[bytes]) -> bytes:
    client = create_client()
    content = build_content(prompt, images)
    response = await call_model(client, content)
    return extract_image(response)
