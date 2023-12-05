from db.dals import PersonDAL
from db.dals import UserDAL


async def change_user_companion(session, user_id, person_id):
    async with session.begin():
        user_dal = UserDAL(session)
        await user_dal.update_user_companion(user_id, person_id)


async def get_person_first_message_by_id(session, person_id):
    async with session.begin():
        person_dal = PersonDAL(session)
        person = await person_dal.get_person_by_id(person_id)
        return person.first_message_text
