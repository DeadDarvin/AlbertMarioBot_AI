"""
This file contains all handlers of the bot.
Handlers can only call methods from 'logic_layer' folder
"""
from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message

from amplitude import send_notification_to_amplitude
from bot.constans.keyboards import START_MARKUP
from bot.constans.texts import CHANGE_PERSON_TEXT
from bot.constans.texts import START_TEXT
from bot.logic_layer.actioners import register_new_user_if_does_not_exists
from bot.logic_layer.actioners import user_dialog_message_actioner
from bot.logic_layer.exc import GPTConnectionError
from bot.logic_layer.exc import UserHasNotCompanionError


dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command.
    1. Send notification about the user-registration to Amplitude.
    2. Save user in db if user doesn't exist id db.
    3. Send start-message with WebApp-keyboard to user.
    """
    user = message.from_user
    await register_new_user_if_does_not_exists(
        user.id, user.username, user.first_name, user.last_name
    )
    await message.answer(START_TEXT, reply_markup=START_MARKUP)


@dp.message(Command("menu"))
async def command_menu_handler(message: Message) -> None:
    """
    This handler receives messages with `/menu` command.
    Send WebApp button to user with text.
    """
    await message.answer(CHANGE_PERSON_TEXT, reply_markup=START_MARKUP)


@dp.message()
async def message_handler(message: Message):
    """
    This handler receives any messages except '/start' and '/menu'
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
        await message.answer(text=response_from_gpt)
        await send_notification_to_amplitude("Responses to users", user.id)
    except UserHasNotCompanionError:
        await message.answer("Выбери компаньона, дурень!", reply_markup=START_MARKUP)
    except GPTConnectionError:
        await message.answer("Ошибка на стороне OpenAI. Попробуйте позже!")
