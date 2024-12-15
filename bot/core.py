from functools import wraps

from telebot.types import (
    Message
)

from AI.settings import GROUP_ID
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

def is_message_forward_from(func):
    @wraps(func)
    def wrapped(message):
        if message.forward_from is not None:
            return func(message)

    return wrapped

def is_support_group(func):
    @wraps(func)
    def wrapped(message):
        if message.chat.id == GROUP_ID:
            return func(message)

    return wrapped

def is_message_reply(func):
    @wraps(func)
    def wrapped(message):
        if message.reply_to_message is not None:
            return func(message)

    return wrapped