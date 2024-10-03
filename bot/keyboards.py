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

from bot import bot, logger
from bot.models import User

"""InlineKeyboards"""

PAY_BUTTONS = types.InlineKeyboardMarkup()
pay = types.InlineKeyboardButton(text="Оплатить", pay=True)
PAY_BUTTONS.add(pay).add('back_button')
CHOOSE_MODEL_MENU = InlineKeyboardMarkup()
model_1 = InlineKeyboardButton(text='1 модель сложный', callback_data='model_1')
model_2 = InlineKeyboardButton(text='2 модель легкий', callback_data='model_2')
model_3 = InlineKeyboardButton(text='3 модель легкий', callback_data='model_3')
CHOOSE_MODEL_MENU.add(model_1).add(model_2).add(model_3)

"""ReplyKeyboards"""

GET_PHONE_NUMS = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
)
btn = KeyboardButton(text='Предоставить номер', request_contact=True)
GET_PHONE_NUMS.add(btn)
