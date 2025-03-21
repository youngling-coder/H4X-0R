import random
import time
import os

from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.enums.parse_mode import ParseMode

import func, crud, schemas, models
from settings import h4x0r_settings
from llm import respond_on_message, get_chat_session


router = Router()

is_activated = lambda message: message and list(
    filter(lambda x: message.lower().startswith(x), h4x0r_settings.BOT_NAMES)
)


@router.message(Command("voice"))
async def send_voice_message(message: types.Message):

    user = await crud.create_user_if_not_exists(schemas.User(telegram_id=message.from_user.id))

    temp_message = await message.answer("🧠 Generating response...")
    start_time = time.perf_counter()

    chat, response, generation_time_ms = await get_answer(message, user)

    await temp_message.edit_text("🎙️ Recording voice...")
    audio_path = func.text_to_speech(response)
    exec_time = time.perf_counter() - start_time

    telegram_audio = types.FSInputFile(audio_path)
    sent_message = await message.answer_voice(
        telegram_audio, caption=f"⏱️ ~{int(exec_time * 1000)} ms"
    )

    await crud.create_message(
        schemas.Message(
            telegram_id=sent_message.message_id,
            chat_id=chat.id,
            user_id=user.id,
            content=response,
            generation_time_ms=generation_time_ms,
            history_part=True,
            from_bot=True,
        )
    )

    await temp_message.delete()
    os.remove(audio_path)


@router.message(Command("syscheck"))
async def system_check_handler(message: types.Message):

    await message.reply(
        func.generate_report(message.chat.id), parse_mode=ParseMode.HTML
    )


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:

    chat_id = str(message.chat.id)

    if chat_id == h4x0r_settings.SECRET_OWNER_CHAT_ID:
        chat = get_chat_session(message)

        response = await respond_on_message(
            message="Introduce yourself to your owner in a brief form and tell about yourself.",
            chat_object=chat,
        )

        await message.reply(response, parse_mode=None)


@router.message(Command("names"))
async def what_is_my_name(message: types.Message):

    await message.reply(
        "These are some of my names: "
        + ", ".join(
            [
                choice.capitalize()
                for choice in random.choices(
                    h4x0r_settings.BOT_NAMES, k=random.randint(3, 6)
                )
            ]
        )
    )


@router.message(lambda message: message.chat.type in ("group", "supergroup"))
async def group_message_handler(message: types.Message):

    user = await crud.create_user_if_not_exists(schemas.User(telegram_id=message.from_user.id))

    if (
        (message.reply_to_message and message.reply_to_message.from_user.is_bot)
        or is_activated(message.caption)
        or is_activated(message.text)
    ):
        if is_allowed_content(message):
            start_time = time.perf_counter()
            chat, response, generation_time_ms = await get_answer(message, user)

            chunks = func.get_chunks_from_message(response)

            for i, chunk in enumerate(chunks):
                if i == len(chunks) - 1:
                    exec_time = time.perf_counter() - start_time
                    chunk += f"\n⏱️ ~{int(exec_time * 1000)} ms"

                sent_message = await message.reply(chunk, parse_mode=None)

            await crud.create_message(
                schemas.Message(
                    telegram_id=sent_message.message_id,
                    chat_id=chat.id,
                    user_id=user.id,
                    content=response,
                    generation_time_ms=generation_time_ms,
                    history_part=True,
                    from_bot=True,
                )
            )


@router.message(lambda message: message.chat.type == "private")
async def private_message_handler(message: types.Message):

    user = await crud.create_user_if_not_exists(schemas.User(telegram_id=message.from_user.id))

    if is_allowed_content(message):
        start_time = time.perf_counter()
        chat, response, generation_time_ms = await get_answer(message, user)

        chunks = func.get_chunks_from_message(response)

        for i, chunk in enumerate(chunks):
            if i == len(chunks) - 1:
                exec_time = time.perf_counter() - start_time
                chunk += f"\n⏱️ ~{int(exec_time * 1000)} ms"
            sent_message = await message.reply(chunk, parse_mode=None)

        await crud.create_message(
            schemas.Message(
                telegram_id=sent_message.message_id,
                chat_id=chat.id,
                user_id=user.id,
                content=response,
                generation_time_ms=generation_time_ms,
                history_part=True,
                from_bot=True,
            )
        )


def is_allowed_content(message: types.Message) -> bool:
    return bool(
        message.text
        or message.caption
        or message.photo
        or message.sticker
        or message.voice
    )

async def get_answer(message: types.Message, user: models.User):

    chat_session = await get_chat_session(message)
    chat: models.Chat = await crud.get_chat(message.chat.id)

    await crud.add_user_to_chat_if_not_added(user.id, chat.id)

    image = None

    final_message = [
        f"message by: {message.from_user.username} ({message.from_user.first_name} {message.from_user.last_name})\n\n"
    ]

    if message.photo:
        if message.caption:
            final_message[0] += message.caption
        image = await func.photo_to_pil_object(message.photo[-1])
    elif message.voice:
        final_message[0] += await func.voice_to_text(message.voice.file_id)
    elif message.sticker:
        image = await func.sticker_to_pil_object(message.sticker)
    elif message.text:
        final_message[0] += message.text

    if image:
        final_message.append(image)

    start_time = time.perf_counter()
    response = await respond_on_message(message=final_message, chat_object=chat_session)

    generation_time_ms = int((time.perf_counter() - start_time) * 1000)

    await crud.create_message(
        schemas.Message(
            telegram_id=message.message_id,
            chat_id=chat.id,
            user_id=user.id,
            content=final_message[0],
            history_part=True,
            from_bot=False,
        )
    )

    return chat, response, generation_time_ms
