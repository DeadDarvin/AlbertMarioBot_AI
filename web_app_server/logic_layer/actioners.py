import asyncio

from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from amplitude import send_notification_to_amplitude
from db.session import into_new_async_session
from settings import BOT_TOKEN
from web_app_server.logic_layer.db_api import change_user_companion
from web_app_server.logic_layer.db_api import get_person_first_message_by_id


@into_new_async_session
async def fix_user_companion_and_start_dialog(
    session: AsyncSession, user_id: int, person_id: int
):
    """
    General WebApp logic-scope.
    1. Send notification about the user selected person to Amplitude.
    2. Change user companion on selected in db.
    3. Get first companion message from db.
    4. Send first_companion message to user.
    """
    asyncio.create_task(send_notification_to_amplitude("Users Selections", user_id))

    await change_user_companion(session, user_id, person_id)
    companion_first_message = await get_person_first_message_by_id(session, person_id)

    url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}"
        f"/sendMessage?chat_id={user_id}&text={companion_first_message}"
    )
    async with ClientSession() as session:
        async with session.get(url, ssl=False):
            return
