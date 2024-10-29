from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    BotCommand,
    ReplyKeyboardRemove
)

from telebot import types

"""InlineKeyboards"""

PAY_BUTTONS = types.InlineKeyboardMarkup()
pay = types.InlineKeyboardButton(text="Оплатить", pay=True)
PAY_BUTTONS.add(pay).add('back_button')

UNIVERSAL_KEYBOARD = types.InlineKeyboardMarkup()
back_hub = types.InlineKeyboardButton(text="Назад", callback_data="back_hub")
back = types.InlineKeyboardButton(text="Назад в меню", callback_data="back_to_menu")

"""ReplyKeyboards"""

GET_PHONE_NUMS = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
)
btn = KeyboardButton(text='Предоставить номер', request_contact=True)
GET_PHONE_NUMS.add(btn)
