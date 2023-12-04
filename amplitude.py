import json

from aiohttp import ClientSession

from settings import AMPLITUDE_API_KEY


async def send_notification_to_amplitude(event_name: str, user_id: int):
    headers = {"Content-Type": "application/json", "Accept": "*/*"}

    data = {
        "api_key": AMPLITUDE_API_KEY,
        "events": [{"user_id": user_id, "event_type": event_name}],
    }
    url = "https://api2.amplitude.com/2/httpapi"
    async with ClientSession() as session:
        async with session.post(url, headers=headers, data=json.dumps(data), ssl=False):
            return
