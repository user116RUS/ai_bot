from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from bot import bot

from bot.texts import tutorial_texts
from bot.keyboards import tutorial_markup


def tutorial(call):
    bot.send_message(chat_id=call.message.chat.id, text=tutorial_texts[0], reply_markup=tutorial_markup)



def tutorial_next(call):
    _, index = call.data.split("_")
    index += 1
    bot.send_message(chat_id=call.message.chat.id, text=tutorial_texts[index], reply_markup=tutorial_markup)
