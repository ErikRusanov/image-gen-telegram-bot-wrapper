from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from bot.config import settings
from bot.dispatcher import create_dispatcher


async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(
        url=settings.WEBHOOK_URL + settings.WEBHOOK_PATH,
        drop_pending_updates=True,
    )


async def on_shutdown(bot: Bot) -> None:
    await bot.delete_webhook()


def create_app(dp: Dispatcher, bot: Bot) -> web.Application:
    app = web.Application()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)

    return app


def main() -> None:
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = create_dispatcher()
    app = create_app(dp, bot)
    web.run_app(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()
