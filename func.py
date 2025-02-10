import aiohttp
import sys
import re
import io

from PIL import Image
from telethon import TelegramClient
from aiogram.types.photo_size import PhotoSize
from google.generativeai.generative_models import ChatSession

from settings import h4x0r_settings



client = TelegramClient("session", h4x0r_settings.APP_ID, h4x0r_settings.API_HASH)


async def get_chat_members(chat_id: int):
    return await client.get_participants(chat_id)


def escape_markdown(text: str) -> str:

    escape_chars = r"_*`["

    return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", text)


async def photo_to_pil_object(photo: PhotoSize):

    from bot import H4X0R_bot

    file_info = await H4X0R_bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{h4x0r_settings.TELEGRAM_BOT_TOKEN}/{file_info.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            image_bytes = await response.read()

    image = Image.open(io.BytesIO(image_bytes))

    return image


def truncate_history(chat_object: ChatSession):

    while (
        sum(sys.getsizeof(str(item)) for item in chat_object.history)
        > h4x0r_settings.DUMP_FILE_MAXIMUM_SIZE_BYTES
        or len(chat_object.history) > h4x0r_settings.DUMP_FILE_MAXIMUM_ITEMS_COUNT
    ):
        if not chat_object.history:
            break
        chat_object.history.pop(0)
