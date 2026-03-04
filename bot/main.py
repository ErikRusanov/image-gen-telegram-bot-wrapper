import uvicorn
from aiogram import Bot
from aiogram.types import Update

from bot.config import settings
from bot.dispatcher import create_dispatcher

bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
dp = create_dispatcher()


async def app(scope, receive, send) -> None:
    if scope["type"] == "lifespan":
        while True:
            event = await receive()
            if event["type"] == "lifespan.startup":
                await bot.set_webhook(
                    url=settings.WEBHOOK_URL + settings.WEBHOOK_PATH,
                    drop_pending_updates=True,
                )
                await send({"type": "lifespan.startup.complete"})
            elif event["type"] == "lifespan.shutdown":
                await bot.delete_webhook()
                await bot.session.close()
                await send({"type": "lifespan.shutdown.complete"})
                return

    elif scope["type"] == "http":
        if scope["path"] == settings.WEBHOOK_PATH and scope["method"] == "POST":
            body = b""
            while True:
                event = await receive()
                body += event.get("body", b"")
                if not event.get("more_body"):
                    break
            update = Update.model_validate_json(body)
            await dp.feed_update(bot, update)
            await send({"type": "http.response.start", "status": 200, "headers": []})
            await send({"type": "http.response.body", "body": b"ok"})
        else:
            await send({"type": "http.response.start", "status": 404, "headers": []})
            await send({"type": "http.response.body", "body": b""})


def main() -> None:
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    main()
