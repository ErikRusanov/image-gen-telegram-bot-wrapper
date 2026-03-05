import logging
import uuid
from dataclasses import dataclass, field

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message

from bot.services import generation
from bot.telegram import keyboards, media, replies

logger = logging.getLogger(__name__)

router = Router()


@dataclass
class PendingState:
    prompt: str
    photos: list[bytes] = field(default_factory=list)
    model_id: str | None = None


_pending: dict[str, PendingState] = {}


@router.message()
async def handle_message(message: Message, bot: Bot) -> None:
    prompt = message.text or message.caption or ""
    photos = await media.download_photos(message, bot)

    token = uuid.uuid4().hex
    _pending[token] = PendingState(prompt=prompt, photos=photos)

    await message.answer("Choose model:", reply_markup=keyboards.model_selection(token))


@router.callback_query(F.data.startswith("model:"))
async def handle_model_choice(callback: CallbackQuery, bot: Bot) -> None:
    _, model_key, token = callback.data.split(":", 2)

    state = _pending.get(token)
    if state is None:
        await callback.answer("Session expired, please send your message again.")
        return

    state.model_id = keyboards.MODEL_OPTIONS[model_key].model_id

    await callback.message.edit_text("Choose format:", reply_markup=keyboards.format_selection(token))
    await callback.answer()


@router.callback_query(F.data.startswith("format:"))
async def handle_format_choice(callback: CallbackQuery, bot: Bot) -> None:
    _, format_key, token = callback.data.split(":", 2)

    state = _pending.pop(token, None)
    if state is None:
        await callback.answer("Session expired, please send your message again.")
        return

    aspect_ratio = keyboards.FORMAT_OPTIONS[format_key].aspect_ratio
    short_prompt = state.prompt[:200] if state.prompt else "(image)"
    await callback.message.edit_text(f"Generating for: {short_prompt}")
    await callback.answer()

    try:
        img_bytes, usage_text = await generation.generate_image(
            state.prompt, state.photos, model=state.model_id, aspect_ratio=aspect_ratio
        )
        await replies.send_image(callback.message, img_bytes, usage_text, caption=state.prompt)
    except Exception:
        logger.exception("Failed to generate image")
        await callback.message.answer("Something went wrong. Please try again.")
