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
index = 0
btn = InlineKeyboardButton(text="Понятно!", callback_data=f"next_{index}")

tutorial_markup = InlineKeyboardMarkup

tutorial_markup.add(btn)
CHOOSE = InlineKeyboardMarkup()
yes = InlineKeyboardButton(text="Да", callback_data="tutorial_yes")
no = InlineKeyboardButton(text="Нет", callback_data="tutorial_no")

CHOOSE.add(yes, no)
"""ReplyKeyboards"""
