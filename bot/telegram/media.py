import io

from aiogram import Bot
from aiogram.types import Message

MAX_PHOTOS = 3


def get_largest_photo_ids(message: Message) -> list[str]:
    if not message.photo:
        return []
    # message.photo is a flat list of PhotoSize for a single image (different resolutions).
    # When multiple images are sent, aiogram groups them; each group's highest-res item
    # is the last one. Since Telegram sends each photo as a separate message in a media
    # group, we just take the largest size of the single photo attachment here.
    largest = message.photo[-1]
    return [largest.file_id]


async def download_file(bot: Bot, file_id: str) -> bytes:
    file = await bot.get_file(file_id)
    buf = io.BytesIO()
    await bot.download_file(file.file_path, destination=buf)
    return buf.getvalue()


async def download_photos(message: Message, bot: Bot) -> list[bytes]:
    file_ids = get_largest_photo_ids(message)
    results = []
    for file_id in file_ids[:MAX_PHOTOS]:
        results.append(await download_file(bot, file_id))
    return results
