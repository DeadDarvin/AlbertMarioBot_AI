import json

from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from amplitude import send_notification_to_amplitude
from db.dals import MessageDAL
from db.dals import UserDAL
from db.session import into_new_async_session
from settings import GPT_API_URL


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
            await send_notification_to_amplitude("Users Registrations", telegram_id)
            await user_dal.register_new_user(telegram_id, username, name, surname)


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
        new_message = await message_dal.create_message(user_id, message_text)
        return new_message.id


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


async def save_message_reply(session, m_id, m_response):
    async with session.begin():
        message_dal = MessageDAL(session)
        await message_dal.update_message(m_id, m_response)


@into_new_async_session
async def user_dialog_message_actioner(
    session: AsyncSession, user_id: int, message_text: str
):
    await send_notification_to_amplitude("Users Requests", user_id)
    user_companion = await get_user_companion(session, user_id)
    if user_companion is None:
        raise UserHasNotCompanion("tic-tic")
    m_id = await save_message_text(session, user_id, message_text)

    response = await send_request_to_gpt(user_companion.name, message_text)
    await send_notification_to_amplitude("Gpt Responses", user_id)
    response_text = response["choices"][0]["message"]["content"]

    await save_message_reply(session, m_id, response_text)
    return response_text
