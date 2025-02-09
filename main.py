import sys
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from settings import h4x0r_settings
from assistant import client
from bot import router


logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

dp = Dispatcher()
dp.include_router(router)


async def start_bot():
    bot = Bot(
        token=h4x0r_settings.TELEGRAM_BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN),
    )
    await dp.start_polling(bot)


async def main():
    await asyncio.gather(start_bot(), client.start())


if __name__ == "__main__":
    asyncio.run(main())
