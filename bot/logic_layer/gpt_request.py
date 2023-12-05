import json

from aiohttp import ClientSession

from settings import GPT_API_URL


async def send_request_to_gpt(person_name, message_text):
    system_content = (
        f"Instructions: You are {person_name}. Do not give dangerous information."
    )
    user_content = f"User message: {message_text}"
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content},
        ],
    }
    async with ClientSession() as session:
        async with session.post(
            url=GPT_API_URL, ssl=False, data=json.dumps(data)
        ) as response:
            return await response.json()
