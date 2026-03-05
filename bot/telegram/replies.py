import logging

from aiogram import Bot
from aiogram.types import BufferedInputFile, Message

logger = logging.getLogger(__name__)


async def send_thinking(message: Message) -> Message:
    return await message.answer("🎨 Generating your image, please wait...")


async def send_image(
    message: Message, img_bytes: bytes, usage_text: str | None = None, caption: str | None = None
) -> None:
    photo = BufferedInputFile(img_bytes, filename="generated.png")
    caption = caption if caption is not None else (message.text or message.caption or "")
    if usage_text:
        caption = f"{caption}\n\n{usage_text}".strip()
    await message.answer_photo(photo=photo, caption=caption)


async def send_error(message: Message) -> None:
    await message.answer("❌ Something went wrong. Please try again.")


async def delete_message(bot: Bot, chat_id: int, message_id: int) -> None:
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception:
        logger.debug("Could not delete message %s in chat %s", message_id, chat_id)
