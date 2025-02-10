from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


enable_button = KeyboardButton(text="🟢 Enable Offline Mode")
disable_button = KeyboardButton(text="🔴 Disable Offline Mode")

menu_keyboard_markup = ReplyKeyboardMarkup(
    keyboard=[[enable_button], [disable_button]], resize_keyboard=True
)
