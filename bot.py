from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties

from func import escape_markdown, photo_to_pil_object
from settings import h4x0r_settings
from llm import respond_on_message, create_new_chat, get_chat


H4X0R_bot = Bot(
    token=h4x0r_settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)

router = Router()


@router.message(Command("hector"))
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
            chat = create_new_chat(title=username)

        response = await respond_on_message(
            message="Introduce yourself to your owner in a brief form and tell about yourself.",
            chat_name=username,
            chat_object=chat,
        )

        await message.reply(
            escape_markdown(response),
            parse_mode=ParseMode.MARKDOWN,
        )


@router.message()
async def message_handler(message: Message) -> None:

    chat_type = message.chat.type

    if chat_type in ("group", "supergroup") and (
        (message.text or message.caption) or message.photo
    ):
        title = message.chat.id
        chat = get_chat(title=title)

        if not chat:

            chat = create_new_chat(title=title)

        final_message = [
            f"message by: {message.from_user.username} ({message.from_user.first_name} {message.from_user.last_name})\n\n"
        ]

        if message.photo:
            if message.caption:
                final_message[0] += message.caption
            image = await photo_to_pil_object(message.photo[-1])

            final_message.append(image)

        else:
            final_message[0] += message.text

        response = await respond_on_message(
            message=final_message, chat_name=str(message.chat.id), chat_object=chat
        )

        if response.strip() != h4x0r_settings.EMPTY_ANSWER_PLACEHOLDER.strip():
            await message.reply(
                escape_markdown(response), parse_mode=ParseMode.MARKDOWN
            )
