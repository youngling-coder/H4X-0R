import sys
import asyncio
import logging

from aiogram import Dispatcher

from assistant import client
from bot import router, H4X0R_bot


logging.basicConfig(level=logging.INFO, stream=sys.stdout)

dp = Dispatcher()
dp.include_router(router)


async def start_bot():
    await dp.start_polling(H4X0R_bot)


async def main():
    await asyncio.gather(start_bot(), client.start())


if __name__ == "__main__":
    asyncio.run(main())
