from aiogram import Router
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import CommandStart

from settings import h4x0r_settings
from keyboards import menu_keyboard_markup, enable_button, disable_button
from llm import respond_on_message


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
    response = await respond_on_message(
        message="Introduce yourself in a brief form and tell about yourself."
    )
    await message.reply(
        response, parse_mode=ParseMode.MARKDOWN, reply_markup=menu_keyboard_markup
    )


@router.message()
async def message_handler(message: Message) -> None:
    try:
        response = await respond_on_message(message=message.text)
        await message.reply(response, parse_mode=ParseMode.MARKDOWN)

    except TypeError:
        await message.answer("Nice try!")
