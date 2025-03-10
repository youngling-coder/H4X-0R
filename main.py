import sys
import asyncio
import logging

from aiogram import Dispatcher

from handlers import router
from bot import H4X0R_bot

logging.basicConfig(level=logging.INFO, stream=sys.stdout)


dp = Dispatcher()
dp.include_router(router)


async def main():
    await dp.start_polling(H4X0R_bot)


if __name__ == "__main__":
    asyncio.run(main())
