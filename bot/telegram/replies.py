import logging

from aiogram import Bot
from aiogram.types import BufferedInputFile, Message

logger = logging.getLogger(__name__)

_MIME_TO_EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp"}


async def send_thinking(message: Message) -> Message:
    return await message.answer("🎨 Generating your image, please wait...")


async def send_image(
    message: Message,
    img_bytes: bytes,
    mime_type: str,
    usage_text: str | None = None,
    caption: str | None = None,
) -> None:
    ext = _MIME_TO_EXT.get(mime_type, "jpg")
    file = BufferedInputFile(img_bytes, filename=f"generated.{ext}")
    caption = caption if caption is not None else (message.text or message.caption or "")
    if usage_text:
        caption = f"{caption}\n\n{usage_text}".strip()
    if len(caption) > 1024:
        caption = caption[:1021] + "..."
    # Send as document to skip Telegram's photo recompression pipeline
    await message.answer_document(document=file, caption=caption)


async def send_error(message: Message) -> None:
    await message.answer("❌ Something went wrong. Please try again.")


async def delete_message(bot: Bot, chat_id: int, message_id: int) -> None:
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        logger.debug("Could not delete message %s in chat %s", message_id, chat_id)
