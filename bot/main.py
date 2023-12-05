"""
This file is entry-point for launch bot.
"""
import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.enums import ParseMode

from bot.handlers import dp
from settings import BOT_TOKEN


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
