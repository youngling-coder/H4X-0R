import aiohttp
import io
import os

from PIL import Image
import speech_recognition as sr
from pydub import AudioSegment
from aiogram.types.photo_size import PhotoSize
from aiogram.types.sticker import Sticker
from google.generativeai.generative_models import ChatSession

import crud
from settings import h4x0r_settings
from bot import H4X0R_bot


async def voice_to_text(file_id: str, buffer: int = 20):
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

        try:
            while True:

                audio_data = recognizer.record(source, duration=buffer)

                if not audio_data.frame_data:
                    break

                text += recognizer.recognize_google(audio_data, language="ru-RU")
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

    if len(chat_object.history) > h4x0r_settings.MAXIMUM_HISTORY_LENGTH:
        chat_object.history = chat_object.history[
            1 : h4x0r_settings.MAXIMUM_HISTORY_LENGTH + 1
        ]


def get_chunks_from_message(text: str):

    if len(text) <= 4096:
        yield text

    else:
        words = text.split()
        part = ""

        for word in words:
            if len(part + word) < 4096:
                part += f"{word} "
                
            else:
                yield part
                part = ""
        else:
            if part:
                yield part


def generate_report(chat_id: str):

    settings_dict = h4x0r_settings.model_dump()
    
    filtered_settings_dict = {}
    for key, value in settings_dict.items():
        if not key.startswith("SECRET_"):
            filtered_settings_dict[key] = value

    current_messages_amount = crud.get_amount_messages_in_chat(chat_id)
    messages_percent = current_messages_amount * 100 / h4x0r_settings.MAXIMUM_HISTORY_LENGTH 
    progress_bar_history = f"[{"🟩" * (rounded_message_percent:=int(messages_percent // 20))}{"⬜️" * (5-rounded_message_percent)}]"

    report = f"""
<b>🎛 System Healthcheck</b>

<b>🤖 Bot:</b> {h4x0r_settings.BOT_NAME} {h4x0r_settings.VERSION}
<b>🔧 LLM Version:</b> {h4x0r_settings.LLM_NAME}
<b>📏 History:</b> {messages_percent}% {progress_bar_history}
"""
    
    return report