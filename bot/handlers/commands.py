from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

router = Router()


@router.message(CommandStart())
async def handle_start(message: Message) -> None:
    await message.answer(
        "👋 Send me a text prompt and I'll generate an image.\n"
        "You can also attach up to 3 photos as reference."
    )
