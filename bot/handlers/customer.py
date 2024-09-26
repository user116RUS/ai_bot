from telebot.types import (
    Message, CallbackQuery
)
from bot.models import Mode, UserMode, User
from bot import bot, logger
from bot.texts import HELP_TEXT, GREETING_TEXT, MODEL_TEXT
from bot.keyboards import BUY_MENU




def buy_message(call: CallbackQuery) -> None:
    bot.delete_message(call.message.chat.id, call.message.message_id)
    user = User.objects.get(telegram_id=call.message.from_user.id)
    plan_name = user.mode.name
    model = user.mode.model
    amount = user.user_mode.requests_amount
    txt = f'ваш план: {plan_name} \nваша модель {model} \nоставшиеся запросы {amount}'
    bot.send_message(call.message.chat.id, txt, reply_markup=BUY_MENU)