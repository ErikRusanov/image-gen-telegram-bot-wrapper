# Image Gen Telegram Bot

Telegram bot that generates images from text prompts using [Google Gemini 3.1 Flash Image Preview](https://openrouter.ai/google/gemini-3.1-flash-image-preview) via OpenRouter.

Send a text message → get a generated image back. Attach up to 3 photos to use them as references for editing.

Each response includes token usage and cost.

## Setup

```
cp .env.example .env
```

Fill in `.env`:

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | From [@BotFather](https://t.me/BotFather) |
| `OPENROUTER_API_KEY` | From [openrouter.ai/keys](https://openrouter.ai/keys) |
| `WEBHOOK_URL` | Public HTTPS URL of your server |
| `WEBHOOK_PATH` | URL path for the webhook (default: `/webhook`) |
| `HOST` | Bind address (default: `0.0.0.0`) |
| `PORT` | Bind port (default: `8080`) |

## Run

```bash
# Local
make run

# Docker
make build
docker run --env-file .env image-gen-bot
```

## Stack

- [aiogram](https://github.com/aiogram/aiogram) — Telegram bot framework
- [OpenRouter](https://openrouter.ai) — model API gateway
- [uvicorn](https://www.uvicorn.org) — ASGI server (webhook mode)
- [Poetry](https://python-poetry.org) — dependency management
