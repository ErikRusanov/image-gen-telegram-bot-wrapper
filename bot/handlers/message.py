import logging

from aiogram import Bot, Router
from aiogram.types import Message

from bot.services import generation
from bot.telegram import media, replies

logger = logging.getLogger(__name__)

router = Router()


@router.message()
async def handle_message(message: Message, bot: Bot) -> None:
    thinking_msg = await replies.send_thinking(message)
    try:
        photos = await media.download_photos(message, bot)
        img_bytes, usage_text = await generation.generate_image(message.text or message.caption or "", photos)
        await replies.send_image(message, img_bytes, usage_text)
    except Exception:
        logger.exception("Failed to generate image")
        await replies.send_error(message)
    finally:
        await replies.delete_message(bot, message.chat.id, thinking_msg.message_id)
