import aiohttp
import io
import os

from PIL import Image
import speech_recognition as sr
from pydub import AudioSegment
from aiogram.types.photo_size import PhotoSize
from aiogram.types.sticker import Sticker
from google.generativeai.generative_models import ChatSession

from settings import h4x0r_settings
from bot import H4X0R_bot


async def voice_to_text(file_id: str):
    text = ""
    recognizer = sr.Recognizer()

    file_info = await H4X0R_bot.get_file(file_id)
    file_path = file_info.file_path

    if not file_path:
        return "Ошибка: не удалось получить путь к файлу"

    # Пути сохранения файлов
    ogg_path = os.path.join(h4x0r_settings.VOICE_MESSAGES_FOLDER, f"{file_id}.ogg")
    wav_path = os.path.join(h4x0r_settings.VOICE_MESSAGES_FOLDER, f"{file_id}.wav")

    # Загрузка и конвертация аудиофайла
    await H4X0R_bot.download_file(file_info.file_path, ogg_path)
    audio = AudioSegment.from_file(ogg_path, format="ogg")
    audio = audio.set_frame_rate(16000)
    audio.export(wav_path, format="wav")
    os.remove(ogg_path)

    with sr.AudioFile(wav_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language="ru-RU")
        finally:
            os.remove(wav_path)

    return text


async def photo_to_pil_object(photo: PhotoSize):

    file_info = await H4X0R_bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{h4x0r_settings.TELEGRAM_BOT_TOKEN}/{file_info.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            image_bytes = await response.read()

    image = Image.open(io.BytesIO(image_bytes))

    return image


async def sticker_to_pil_object(sticker: Sticker):

    if sticker.is_animated or sticker.is_video:
        photo = await photo_to_pil_object(photo=sticker.thumbnail)

        return photo

    file_info = await H4X0R_bot.get_file(sticker.file_id)
    file_url = f"https://api.telegram.org/file/bot{h4x0r_settings.TELEGRAM_BOT_TOKEN}/{file_info.file_path}"

    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            image_bytes = await response.read()

    image = Image.open(io.BytesIO(image_bytes))

    return image


def truncate_history(chat_object: ChatSession):

    while len(chat_object.history) > h4x0r_settings.DUMP_FILE_MAXIMUM_ITEMS_COUNT:
        if not chat_object.history:
            break
        chat_object.history.pop(1)
