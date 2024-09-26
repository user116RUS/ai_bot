from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    BotCommand,
    ReplyKeyboardRemove
)
from bot.models import Mode

"""InlineKeyboards"""

HUB_MENU = InlineKeyboardMarkup()
buy_more_btn = InlineKeyboardButton(text='купить', callback_data='buy_message')
change_model_btn = InlineKeyboardButton(text='сменить модель', callback_data='change_model_btn')
HUB_MENU.add(buy_more_btn).add(change_model_btn)

CHOOSE_MODEL_MENU = InlineKeyboardMarkup()
model_1 = InlineKeyboardButton(text='1 модель сложный', callback_data='model_1')
model_2 = InlineKeyboardButton(text='2 модель легкий', callback_data='model_2')
model_3 = InlineKeyboardButton(text='3 модель легкий', callback_data='model_3')
CHOOSE_MODEL_MENU.add(model_1).add(model_2).add(model_3)

BUY_MENU = InlineKeyboardMarkup()
back = InlineKeyboardButton(text='назад', callback_data='back_choose_model')
buy = InlineKeyboardButton(text='купить', callback_data=f'buy_{Mode.name}')
CHOOSE_MODEL_MENU.add(back).add(buy)

"""ReplyKeyboards"""


GET_PHONE_NUMS = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
)
btn = KeyboardButton(text='Предоставить номер', request_contact=True)
GET_PHONE_NUMS.add(btn)