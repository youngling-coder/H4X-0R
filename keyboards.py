from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


enable_button = KeyboardButton(text="🟢 Enable H4X-0R")
disable_button = KeyboardButton(text="🔴 Disable H4X-0R")

menu_keyboard_markup = ReplyKeyboardMarkup(
    keyboard=[[enable_button], [disable_button]], resize_keyboard=True
)
