from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.types import WebAppInfo


web_app = WebAppInfo(
    url="https://deaddarvin.github.io/AlbertMarioBot_AI/web_app/web_app.html"
)

start_markup_buttons = [
    InlineKeyboardButton(text="Выбрать", web_app=web_app),
]
start_keyboard_schema = [
    start_markup_buttons,
]
START_MARKUP = InlineKeyboardMarkup(inline_keyboard=start_keyboard_schema)
