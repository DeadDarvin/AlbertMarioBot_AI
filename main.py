import asyncio
import logging
import sys

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import Message
from aiogram.types import WebAppInfo
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import UserDAL
from db.session import into_new_async_session
from settings import BOT_TOKEN


dp = Dispatcher()


async def _moc_amplitude():
    pass


@into_new_async_session
async def register_new_user_if_does_not_exists(
    session: AsyncSession,
    telegram_id: int,
    username: str | None,
    name: str | None,
    surname: str | None,
):
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(telegram_id)
        if user is None:
            await user_dal.register_new_user(telegram_id, username, name, surname)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command.
    1. Send notification to Amplitude (Moc now).
    2. Save user in db if user doesn't exist id db.
    3. Send start-message with WebApp-keyboard to user.
    """

    await _moc_amplitude()
    user = message.from_user
    await register_new_user_if_does_not_exists(
        user.id, user.username, user.first_name, user.last_name
    )
    keyboards = []
    web_app = WebAppInfo(url="https://ya.ru")
    buttons = [
        InlineKeyboardButton(text="Выбери, с кем хочешь общаться", web_app=web_app),
    ]
    keyboards.append(buttons)
    markup = InlineKeyboardMarkup(inline_keyboard=keyboards)
    await message.answer("Hello, man!", reply_markup=markup)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
