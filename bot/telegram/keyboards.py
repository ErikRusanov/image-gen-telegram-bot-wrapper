from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.services.openrouter import MODEL_PRO, MODEL_SIMPLE

# (label, model_id, style) — style uses Bot API 9.4 colored buttons
MODEL_OPTIONS: dict[str, tuple[str, str, str]] = {
    "pro": ("Pro", MODEL_PRO, "success"),
    "simple": ("Simple (Nano Banana 2)", MODEL_SIMPLE, "primary"),
}


def model_selection(token: str) -> InlineKeyboardMarkup:
    """Single-row inline keyboard for model selection."""
    buttons = []
    for key, (label, _, style) in MODEL_OPTIONS.items():
        btn = InlineKeyboardButton(text=label, callback_data=f"model:{key}:{token}")
        btn.style = style  # Bot API 9.4 colored buttons
        buttons.append(btn)
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
