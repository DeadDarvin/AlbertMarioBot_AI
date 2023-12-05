"""
This file contains all handlers of the bot.
Handlers can only call methods from 'logic_layer' folder
"""
import asyncio

from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.filters import CommandStart
from aiogram.types import Message

from amplitude import send_notification_to_amplitude
from bot.constans.keyboards import PERSON_SELECTION_MARKUP
from bot.constans.texts import BAD_MESSAGE_TEXT
from bot.constans.texts import CHANGE_PERSON_TEXT
from bot.constans.texts import OPEN_AI_ERROR_TEXT
from bot.constans.texts import SELECT_PERSON_TEXT
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
    await message.answer(START_TEXT, reply_markup=PERSON_SELECTION_MARKUP)


@dp.message(Command("menu"))
async def command_menu_handler(message: Message) -> None:
    """
    This handler receives messages with `/menu` command.
    Send WebApp button to user with text.
    """
    await message.answer(CHANGE_PERSON_TEXT, reply_markup=PERSON_SELECTION_MARKUP)


@dp.message()
async def message_handler(message: Message):
    """
    This handler receives any messages except '/start' and '/menu'.
    Try to response to user through gpt.
    Handle system-logic-exceptions.
    """
    user_id = message.from_user.id
    message_text = message.text
    if message_text is None:
        await message.answer(BAD_MESSAGE_TEXT)
        return
    try:
        response_from_gpt = await user_dialog_message_actioner(user_id, message.text)
        asyncio.create_task(
            send_notification_to_amplitude("Responses to users", user_id)
        )
        await message.answer(text=response_from_gpt)
    except UserHasNotCompanionError:
        await message.answer(SELECT_PERSON_TEXT, reply_markup=PERSON_SELECTION_MARKUP)
    except GPTConnectionError as err:
        print(f"Logger here: GPTConnectionError -- {err}")
        await message.answer(OPEN_AI_ERROR_TEXT)
    except Exception as err:
        print(f"Logger here: Unhandled error -- {err}")
        await message.answer("Что-то пошло не так!")
