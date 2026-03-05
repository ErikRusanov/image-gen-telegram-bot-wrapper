from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.services.openrouter import MODEL_PRO, MODEL_SIMPLE


@dataclass(frozen=True)
class ModelOption:
    label: str
    model_id: str
    style: str


@dataclass(frozen=True)
class FormatOption:
    label: str
    aspect_ratio: str


MODEL_OPTIONS: dict[str, ModelOption] = {
    "pro": ModelOption("Pro", MODEL_PRO, "success"),
    "simple": ModelOption("Simple (Nano Banana 2)", MODEL_SIMPLE, "primary"),
}

FORMAT_OPTIONS: dict[str, FormatOption] = {
    "1_1": FormatOption("1:1", "1:1"),
    "9_16": FormatOption("9:16", "9:16"),
    "16_9": FormatOption("16:9", "16:9"),
    "4_3": FormatOption("4:3", "4:3"),
    "3_4": FormatOption("3:4", "3:4"),
}

DEFAULT_FORMAT = "1_1"


def _btn(text: str, callback_data: str, style: str | None = None) -> InlineKeyboardButton:
    btn = InlineKeyboardButton(text=text, callback_data=callback_data)
    if style:
        btn.style = style  # Bot API 9.4 colored buttons
    return btn


def model_selection(token: str) -> InlineKeyboardMarkup:
    buttons = [_btn(opt.label, f"model:{key}:{token}", opt.style) for key, opt in MODEL_OPTIONS.items()]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


def format_selection(token: str) -> InlineKeyboardMarkup:
    buttons = [_btn(opt.label, f"format:{key}:{token}") for key, opt in FORMAT_OPTIONS.items()]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
