from db.dals import MessageDAL
from db.dals import UserDAL


async def get_user_by_id(session, telegram_id):
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_id(telegram_id)
        return user


async def register_new_user(session, *args):
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.register_new_user(*args)
        return user


async def save_message_text(session, user_id, message_text):
    async with session.begin():
        message_dal = MessageDAL(session)
        new_message = await message_dal.create_message(user_id, message_text)
        return new_message.id


async def save_message_reply(session, m_id, m_response):
    async with session.begin():
        message_dal = MessageDAL(session)
        await message_dal.update_message(m_id, m_response)
