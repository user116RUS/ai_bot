from telebot.types import (
    Message, CallbackQuery,    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from bot.models import Mode, UserMode, User
from bot import bot, logger
from bot.texts import HELP_TEXT, GREETING_TEXT, MODEL_TEXT



def buy_message(callback: CallbackQuery) -> None:
    chat_id = callback.message.chat.id
    _, pk = callback.data.split('_')
    bot.delete_message(chat_id, callback.message.id)
    bot.delete_message(callback.message.chat.id, callback.message.message_id)
    user = User.objects.get(telegram_id=callback.message.from_user.id)
    plan_name = user.mode.name
    model = user.mode.model
    amount = user.user_mode.requests_amount
    txt = f'ваш план: {plan_name} \nваша модель {model} \nоставшиеся запросы {amount}'
    BUY_MENU = InlineKeyboardMarkup()
    back = InlineKeyboardButton(text='назад', callback_data='back_choose_model')
    buy = InlineKeyboardButton(text='купить', callback_data=f'pay_{pk}')
    BUY_MENU.add(back).add(buy)
    bot.send_message(callback.message.chat.id, txt, reply_markup=BUY_MENU)