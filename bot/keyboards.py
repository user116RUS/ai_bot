from telebot.types import (
    Message
)

from bot import bot, logger
from telebot import types

PAY_BUTTONS = types.InlineKeyboardMarkup()
pay = types.InlineKeyboardButton(text="Оплатить", pay=True)
PAY_BUTTONS.add(pay).add(back_button)