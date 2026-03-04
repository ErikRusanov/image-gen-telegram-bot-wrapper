from aiogram import Dispatcher

from bot.handlers.commands import router as commands_router
from bot.handlers.message import router as message_router


def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    dp.include_router(commands_router)
    dp.include_router(message_router)
    return dp
