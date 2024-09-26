from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    BotCommand,
    ReplyKeyboardRemove
)


"""InlineKeyboards"""

HUB_MENU = InlineKeyboardMarkup()
buy_more_btn = InlineKeyboardButton(text='купить больше', callback_data='buy_more')
change_model_btn = InlineKeyboardButton(text='сменить модель', callback_data='change_model_btn')
HUB_MENU.add(buy_more_btn).add(change_model_btn)



"""ReplyKeyboards"""


GET_PHONE_NUMS = ReplyKeyboardMarkup(
    one_time_keyboard=True,
    resize_keyboard=True,
)
btn = KeyboardButton(text='Предоставить номер', request_contact=True)
GET_PHONE_NUMS.add(btn)