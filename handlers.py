import random

from aiogram import Router
from aiogram import types
from aiogram.filters import CommandStart, Command

import func
from settings import h4x0r_settings
from llm import respond_on_message, create_new_chat, get_chat


router = Router()

is_activated = lambda message: message and list(
    filter(lambda x: message.lower().startswith(x), h4x0r_settings.BOT_NAMES)
)


@router.message(Command("syscheck"))
async def system_check_handler(message: types.Message):
    
    await message.reply(func.generate_report(message.chat.id), parse_mode=ParseMode.HTML)


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:

    chat_id = message.chat.id

    if chat_id == h4x0r_settings.OWNER_USERNAME:
        chat = get_chat(chat_id=chat_id)

        if not chat:
            chat = create_new_chat(chat_id=chat_id)

        response = await respond_on_message(
            message="Introduce yourself to your owner in a brief form and tell about yourself.",
            chat_id=chat_id,
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
async def group_message_handler(message: types.Message) -> None:
    if (
        (message.reply_to_message and message.reply_to_message.from_user.is_bot)
        or is_activated(message.caption)
        or is_activated(message.text)
    ):
        if is_allowed_content(message):
            await get_answer(message=message)

    crud.create_user_if_not_exists(message.from_user.id)



@router.message(lambda message: message.chat.type == "private")
async def private_message_handler(message: types.Message) -> None:
    if is_allowed_content(message):
        await get_answer(message=message)


def is_allowed_content(message: types.Message) -> bool:
    return bool(
        message.text
        or message.caption
        or message.photo
        or message.sticker
        or message.voice
    )


async def get_answer(message: types.Message):
    crud.create_user_if_not_exists(message.from_user.id)

    chat_id = message.chat.id
    chat = get_chat(chat_id=chat_id)
    image = None

    if not chat:
        chat = create_new_chat(chat_id=chat_id)

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

    response = await respond_on_message(
        message=final_message, chat_object=chat
    )

    for chunk in func.get_chunks_from_message(response):
    
        exec_time = time.perf_counter() - start_time

        to_send = f"{chunk}\n⏱️ ~{int(exec_time * 1000)} ms"
        await message.reply(to_send, parse_mode=None)

    crud.create_message(chat_id, content=final_message[0], role="user")
    crud.create_message(chat_id, content=response, role="model")
