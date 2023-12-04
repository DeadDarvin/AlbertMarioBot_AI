import asyncio
import json
import logging
import sys

from aiogram import Bot
from aiogram import Dispatcher
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from db.dals import MessageDAL
from db.dals import UserDAL
from db.session import into_new_async_session
from keyboards import START_MARKUP
from settings import BOT_TOKEN
from settings import GPT_API_URL
from texts import START_TEXT


dp = Dispatcher()


async def _moc_amplitude():
    pass


class UserHasNotCompanion(Exception):
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
    await message.answer(START_TEXT, reply_markup=START_MARKUP)


async def get_user_companion(
    session: AsyncSession,
    telegram_id: int,
):
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(telegram_id)
        return user.companion


async def save_message_text(session, user_id, message_text):
    async with session.begin():
        message_dal = MessageDAL(session)
        await message_dal.create_message(user_id, message_text)


async def send_request_to_gpt(person_name, message_text):
    content = (
        f"Instructions: You are {person_name}. Do not give dangerous information."
        f"User message: {message_text}"
    )
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": content}],
    }
    async with ClientSession() as session:
        async with session.post(
            url=GPT_API_URL, ssl=False, data=json.dumps(data)
        ) as response:
            return await response.json()


@into_new_async_session
async def user_dialog_message_actioner(
    session: AsyncSession, user_id: int, message_text: str
):
    user_companion = await get_user_companion(session, user_id)
    if user_companion is None:
        raise UserHasNotCompanion("tic-tic")
    await save_message_text(session, user_id, message_text)
    response = await send_request_to_gpt(user_companion.name, message_text)
    return response["choices"][0]["message"]["content"]


@dp.message()
async def message_handler(message: Message):
    """
    his handler receives any messages except '/start'
    1. Save message_text in db if user has companion.
    2. Send notification to Amplitude (Moc now).
    3. Send request to OpenAI with message_text
    4. Send notification to Amplitude (Moc now).
    5. Send message from OpenAI to user.
    6. Save message from OpenAI next to user_message in db.
    7. Send notification to Amplitude (Moc now).
    """
    user = message.from_user
    try:
        response_from_gpt = await user_dialog_message_actioner(user.id, message.text)
    except UserHasNotCompanion:
        await message.answer("Выбери компаньона, дурень!", reply_markup=START_MARKUP)
        return
    await message.answer(text=response_from_gpt)


async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
