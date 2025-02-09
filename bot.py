from aiogram import Router
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart

from func import escape_markdown
from settings import h4x0r_settings
from keyboards import menu_keyboard_markup, enable_button, disable_button
from llm import respond_on_message, create_new_chat, get_chat
from assistant import client


router = Router()


@router.message(lambda message: message.text == enable_button.text)
async def start_hector_assistant(message: Message):
    if not h4x0r_settings.IS_ENABLED:
        h4x0r_settings.IS_ENABLED = True
        await message.reply("☑️ Hector is enabled!")
    else:
        await message.reply("Hector is already enabled!")


@router.message(lambda message: message.text == disable_button.text)
async def stop_hector_assistant(message: Message):
    if h4x0r_settings.IS_ENABLED:
        h4x0r_settings.IS_ENABLED = False
        await message.reply("☑️ Hector is disabled!")
    else:
        await message.reply("Hector is already disabled!")


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:

    username = (
        message.from_user.username
        if message.from_user.username
        else message.from_user.id
    )
    full_name = f"{message.chat.first_name} {message.chat.last_name}"

    if username == h4x0r_settings.OWNER_USERNAME:
        chat = get_chat(title=username)

        if not chat:
            chat = create_new_chat(
                title=username, type_="private", participants={username: full_name}
            )

        response = await respond_on_message(
            message="Introduce yourself to your owner in a brief form and tell about yourself.",
            chat_name=username,
            chat_object=chat,
        )

        await message.reply(
            escape_markdown(response),
            reply_markup=menu_keyboard_markup,
            parse_mode=ParseMode.MARKDOWN,
        )


@router.message()
async def message_handler(message: Message) -> None:

    chat_type = message.chat.type

    if chat_type in ("group", "supergroup") and message.text:
        title = message.chat.id
        chat = get_chat(title=title)

        if not chat:
            participants = await client.get_participants(message.chat.id)

            participants = {
                (
                    participant.username
                    if participant.username
                    else str(participant.id)
                ): f"{participant.first_name} {participant.last_name}"
                for participant in participants
            }
            chat = create_new_chat(
                title=title, type_=chat_type, participants=participants
            )

        message_text = message.text
        message_text = (
            f"message by: {message.from_user.username} ({message.from_user.first_name} {message.from_user.last_name})\n\n"
            + message_text
        )

        response = await respond_on_message(
            message=message_text, chat_name=str(message.chat.id), chat_object=chat
        )

        await message.reply(escape_markdown(response), parse_mode=ParseMode.MARKDOWN)
