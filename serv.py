# Server-module for getting data from WebAppTelegram.
import hashlib
import hmac
from urllib.parse import unquote

import aiohttp_cors
from aiohttp import web
from aiohttp.web_response import json_response

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

    # data = await request.json()
    # await moc_mark_user_person(data)
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
