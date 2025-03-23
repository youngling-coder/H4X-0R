import aiohttp
import io
import os
import uuid
from aiogram import types
from typing import Optional

from PIL import Image
from pydub import AudioSegment
import speech_recognition as sr
from pydub import AudioSegment
from aiogram.types.photo_size import PhotoSize
from aiogram.types.sticker import Sticker
from google.generativeai.generative_models import ChatSession

import tts
import crud, models
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
    ogg_path = os.path.join(
        h4x0r_settings.SECRET_VOICE_MESSAGES_FOLDER, f"{file_id}.ogg"
    )
    wav_path = os.path.join(
        h4x0r_settings.SECRET_VOICE_MESSAGES_FOLDER, f"{file_id}.wav"
    )

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
    file_url = f"https://api.telegram.org/file/bot{h4x0r_settings.SECRET_TELEGRAM_BOT_TOKEN}/{file_info.file_path}"

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
    file_url = f"https://api.telegram.org/file/bot{h4x0r_settings.SECRET_TELEGRAM_BOT_TOKEN}/{file_info.file_path}"

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


def get_chunks_from_message(text: str, chunk_size: int = 4096):

    parts = []

    if len(text) <= chunk_size:
        return [
            text,
        ]

    words = text.split()
    part = ""

    for word in words:
        if len(part + word) < chunk_size:
            part += f"{word} "

        else:
            parts.append(part)
            part = ""
    else:
        if part:
            parts.append(part)

    return parts


async def generate_report(chat: models.Chat):

    settings_dict = h4x0r_settings.model_dump()

    filtered_settings_dict = {}
    for key, value in settings_dict.items():
        if not key.startswith("SECRET_"):
            filtered_settings_dict[key] = value
    current_messages_count = await crud.get_messages(
        chat_id=chat.id, history_part=True, count=True
    )

    messages_percent = current_messages_count * 100 / chat.history_depth
    progress_bar_history = f"{"■" * (rounded_message_percent:=int(messages_percent // 10))}{"□" * (10-rounded_message_percent)}"

    report = f"""
<b>🎛 System Healthcheck</b>

<b>🤖 Bot:</b> {h4x0r_settings.BOT_NAME} {h4x0r_settings.VERSION}
<b>🧠 LLM:</b> {h4x0r_settings.LLM_NAME}
<b>🎙 TTS Model:</b> {chat.tts_model}
<b>📖 History:</b> {messages_percent}% {progress_bar_history}
"""

    return report


def text_to_speech(text: str):

    processed_text = tts.accentizer.process_all(text)

    voice_parts = []

    for chunk in get_chunks_from_message(processed_text, chunk_size=1000):
        filepath = os.path.join(
            h4x0r_settings.SECRET_VOICE_MESSAGES_FOLDER, f"{uuid.uuid4()}.wav"
        )
        voice_parts.append(filepath)
        audio = tts.tts_model(text=chunk, lenght_scale=0.8)
        tts.tts_model.save_wav(audio, filepath)

    if voice_parts:
        audio = AudioSegment.from_wav(voice_parts[0])

        try:
            for voice_part in voice_parts[1:]:
                audio += AudioSegment.from_wav(voice_part)
                os.remove(voice_part)
        finally:
            filepath = os.path.join(
                h4x0r_settings.SECRET_VOICE_MESSAGES_FOLDER, f"{uuid.uuid4()}.ogg"
            )
            voice_parts.append(filepath)
            audio.export(voice_parts[0], format="ogg")

    return voice_parts[0]


def get_full_name(user: types.User) -> str:

    name = user.id

    if user.username:
        name = user.username

    if user.full_name:
        name = user.full_name

    return str(name)


def get_username(user: types.User) -> Optional[str]:

    if user.username:
        return f"{user.username}"

    return None
