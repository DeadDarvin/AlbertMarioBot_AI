# Server-module for getting data from WebAppTelegram.
import hashlib
import hmac
from urllib.parse import unquote

import aiohttp_cors
from aiohttp import ClientSession
from aiohttp import web
from aiohttp.web_response import json_response
from sqlalchemy.ext.asyncio import AsyncSession

from amplitude import send_notification_to_amplitude
from db.dals import PersonDAL
from db.dals import UserDAL
from db.session import into_new_async_session
from settings import BOT_TOKEN


routes = web.RouteTableDef()
app = web.Application()


def validate(hash_str, init_data, token, c_str="WebAppData"):
    """
    Validates the data received from the Telegram web app, using the
    method documented here:
    https://core.telegram.org/bots/webapps#validating-data-received-via-the-web-app

    hash_str - the has string passed by the webapp
    init_data - the query string passed by the webapp
    token - Telegram bot's token
    c_str - constant string (default = "WebAppData")
    """

    init_data = sorted(
        [
            chunk.split("=")
            for chunk in unquote(init_data).split("&")
            if chunk[: len("hash=")] != "hash="
        ],
        key=lambda x: x[0],
    )
    init_data = "\n".join([f"{rec[0]}={rec[1]}" for rec in init_data])

    secret_key = hmac.new(c_str.encode(), token.encode(), hashlib.sha256).digest()
    data_check = hmac.new(secret_key, init_data.encode(), hashlib.sha256)

    return data_check.hexdigest() == hash_str


@into_new_async_session
async def change_user_companion(
    session: AsyncSession, telegram_id: int, person_id: int
):
    async with session.begin():
        user_dal = UserDAL(session)
        await user_dal.update_user_companion(telegram_id, person_id)


async def get_first_message_by_id(session: AsyncSession, person_id: int) -> str:
    async with session.begin():
        person_dal = PersonDAL(session)
        person = await person_dal.get_person_by_id(person_id)
        return person.first_message_text


@into_new_async_session
async def send_first_companion_message(
    session: AsyncSession, telegram_id: int, person_id: int
):

    companion_first_message = await get_first_message_by_id(session, person_id)
    url = (
        f"https://api.telegram.org/bot{BOT_TOKEN}"
        f"/sendMessage?chat_id={telegram_id}&text={companion_first_message}"
    )
    async with ClientSession() as session:
        async with session.get(url, ssl=False):
            return


@routes.post("/")
async def web_app_data_handler(request):
    headers = request.headers
    hash_str = headers.get("Authorization")
    init_data = headers.get("Init-Data")

    is_valid_request = validate(hash_str, init_data, BOT_TOKEN)
    if not is_valid_request:
        return json_response(
            status=403,
            data={"success": False, "details": "Could not validate credentials!"},
        )

    data = await request.json()
    await send_notification_to_amplitude("Users Selections", data["user_id"])
    await change_user_companion(data["user_id"], data["person_id"])
    await send_first_companion_message(data["user_id"], data["person_id"])
    return json_response(status=200, data={"success": True})


app.add_routes(routes)
cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True, expose_headers="*", allow_headers="*"
        )
    },
)
for route in list(app.router.routes()):
    cors.add(route)


if __name__ == "__main__":
    web.run_app(app=app, host="127.0.0.1", port=8080)
