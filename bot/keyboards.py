from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

"""InlineKeyboards"""

PAY_BUTTONS = InlineKeyboardMarkup()
pay = InlineKeyboardButton(text="Оплатить", pay=True)

PAY_BUTTONS.add(pay)

back_hub = InlineKeyboardButton(text="Назад", callback_data="back_hub")

"""ReplyKeyboards"""
