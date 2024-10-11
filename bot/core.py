from functools import wraps

from telebot.types import (
    Message
)

from bot import bot
from bot.models import User
from bot.texts import NOT_IN_DB_TEXT


def check_registration(func):
    """Check registration for message func"""
    @wraps(func)
    def wrapped(message: Message):
        user_id = message.from_user.id
        if User.objects.filter(telegram_id=user_id).exists():
            return func(message)
        bot.send_message(user_id, NOT_IN_DB_TEXT)
    return wrapped
