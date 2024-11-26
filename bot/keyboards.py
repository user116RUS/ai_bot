from telebot.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

"""InlineKeyboards"""
UNIVERSAL_BUTTONS = InlineKeyboardMarkup()

back = InlineKeyboardButton(text="Назад в меню 🔙", callback_data="back")

UNIVERSAL_BUTTONS.add(back)

PAY_BUTTONS = InlineKeyboardMarkup()
pay = InlineKeyboardButton(text="Оплатить", pay=True)

PAY_BUTTONS.add(pay)

back_hub = InlineKeyboardButton(text="Назад", callback_data="back_hub")


"""ReplyKeyboards"""
