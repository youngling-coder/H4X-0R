import random

from aiogram import Router, Bot
from aiogram import types, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart, Filter, Command
from aiogram.client.default import DefaultBotProperties

from func import escape_markdown, photo_to_pil_object
from settings import h4x0r_settings
from llm import respond_on_message, create_new_chat, get_chat


H4X0R_bot = Bot(
    token=h4x0r_settings.TELEGRAM_BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
)

router = Router()

is_activated = lambda message: message and list(
    filter(lambda x: message.lower().startswith(x), h4x0r_settings.BOT_NAMES)
)


class ReplyToUserFilter(Filter):
    def __init__(self, username: str):
        self.username = username

    async def __call__(self, message: types.Message) -> bool:
        if message.reply_to_message and message.reply_to_message.from_user:
            return message.reply_to_message.from_user.username == self.username
        return False


@router.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:

    username = (
        message.from_user.username
        if message.from_user.username
        else message.from_user.id
    )

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


@router.message(ReplyToUserFilter("h4x0r_hector_bot"))
async def message_handler(message: types.Message) -> None:
    await get_answer(message=message)


@router.message(
    lambda message: (is_activated(message.caption) or is_activated(message.text))
)
async def message_handler(message: types.Message) -> None:
    await get_answer(message=message)


async def get_answer(message: types.Message):
    is_content_appropriate = (
        lambda message: message.text or message.caption or message.photo
    )
    is_group = lambda message: message.chat.type in ("group", "supergroup")

    if (
        is_content_appropriate(message)
        and is_group(message)
        and (F.reply_to_message)
        or (is_activated(message.caption) or is_activated(message.text))
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

        await message.reply(escape_markdown(response))
