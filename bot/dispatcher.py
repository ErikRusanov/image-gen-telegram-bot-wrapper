from aiogram import Dispatcher

from bot.handlers.message import router as message_router


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(message_router)
    return dp
