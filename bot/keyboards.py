from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    BotCommand,
    ReplyKeyboardRemove
)

from bot.models import User




"""InlineKeyboards"""



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