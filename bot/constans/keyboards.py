from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import WebAppInfo

from settings import WEB_APP_URL

web_app = WebAppInfo(url=WEB_APP_URL)

start_markup_buttons = [
    InlineKeyboardButton(text="Выбрать", web_app=web_app),
]
start_keyboard_schema = [
    start_markup_buttons,
]
PERSON_SELECTION_MARKUP = InlineKeyboardMarkup(inline_keyboard=start_keyboard_schema)
