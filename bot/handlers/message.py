import logging
import uuid

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from bot.services import generation
from bot.telegram import keyboards, media, replies

logger = logging.getLogger(__name__)

router = Router()

# Temporary storage: token -> (prompt, photos)
_pending: dict[str, tuple[str, list[bytes]]] = {}


@router.message()
async def handle_message(message: Message, bot: Bot) -> None:
    prompt = message.text or message.caption or ""
    photos = await media.download_photos(message, bot)

    token = uuid.uuid4().hex
    _pending[token] = (prompt, photos)

    await message.answer("Choose model:", reply_markup=keyboards.model_selection(token))


@router.callback_query(F.data.startswith("model:"))
async def handle_model_choice(callback: CallbackQuery, bot: Bot) -> None:
    _, model_key, token = callback.data.split(":", 2)

    pending = _pending.pop(token, None)
    if pending is None:
        await callback.answer("Session expired, please send your message again.")
        return

    prompt, photos = pending
    _, model_id, _ = keyboards.MODEL_OPTIONS[model_key]

    short_prompt = prompt[:200] if prompt else "(image)"
    await callback.message.edit_text(f"Generating for: {short_prompt}")
    await callback.answer()

    try:
        img_bytes, usage_text = await generation.generate_image(prompt, photos, model=model_id)
        await replies.send_image(callback.message, img_bytes, usage_text, caption=prompt)
    except Exception:
        logger.exception("Failed to generate image")
        await callback.message.answer("Something went wrong. Please try again.")
