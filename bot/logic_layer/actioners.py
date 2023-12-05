"""
This file contains general-logic actioners
for calling from handlers
"""
import asyncio

from aiohttp.client_exceptions import ClientError
from sqlalchemy.ext.asyncio import AsyncSession

from amplitude import send_notification_to_amplitude
from bot.logic_layer.db_api import get_user_by_id
from bot.logic_layer.db_api import register_new_user
from bot.logic_layer.db_api import save_message_reply
from bot.logic_layer.db_api import save_message_text
from bot.logic_layer.exc import GPTConnectionError
from bot.logic_layer.exc import UserHasNotCompanionError
from bot.logic_layer.gpt_request import send_request_to_gpt
from db.session import into_new_async_session


@into_new_async_session
async def register_new_user_if_does_not_exists(
    session: AsyncSession,
    telegram_id: int,
    username: str | None,
    name: str | None,
    surname: str | None,
):
    user = await get_user_by_id(session, telegram_id)
    if user is None:
        asyncio.create_task(
            send_notification_to_amplitude("Users Registrations", telegram_id)
        )
        await register_new_user(session, telegram_id, username, name, surname)


@into_new_async_session
async def user_dialog_message_actioner(
    session: AsyncSession, telegram_id: int, message_text: str
):
    """
    General logic-scope for handling user-message through gpt.
    1. Send notification to Amplitude about request from user.
    2. Save message_text in db if user has companion.
    3. Send request to OpenAI with message_text
    4. Send notification to Amplitude about response from gpt.
    5. Save message from gpt next to user_message in db.
    :return: response from gpt
    """
    asyncio.create_task(send_notification_to_amplitude("Users Requests", telegram_id))

    user = await get_user_by_id(session, telegram_id)
    user_companion = user.companion
    if user_companion is None:
        raise UserHasNotCompanionError(
            "User try to send message without changed companion"
        )

    message_id = await save_message_text(session, telegram_id, message_text)

    try:
        response = await send_request_to_gpt(user_companion.name, message_text)
    except ClientError as err:
        raise GPTConnectionError(err)

    asyncio.create_task(send_notification_to_amplitude("Gpt Responses", telegram_id))
    response_text = response["choices"][0]["message"]["content"]

    await save_message_reply(session, message_id, response_text)
    return response_text
