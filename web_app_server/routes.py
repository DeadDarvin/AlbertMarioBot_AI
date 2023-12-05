from aiohttp import web
from aiohttp.web_response import json_response

from settings import BOT_TOKEN
from web_app_server.auth_validation import validate
from web_app_server.logic_layer.actioners import fix_user_companion_and_start_dialog

routes = web.RouteTableDef()


@routes.post("/")
async def web_app_data_handler(request):
    """
    This router receives POST-requests.
    1. Check request is valid (by tg_instruction)
    2. Call actioner for update user_companion in db
        and send companion first message from bot.
    """
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
    user_id = data["user_id"]
    person_id = data["person_id"]

    await fix_user_companion_and_start_dialog(user_id, person_id)
    return json_response(status=200, data={"success": True})
