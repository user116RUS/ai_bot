from telebot.types import (
    Message
)

from django.conf import settings
from bot import IMAGE_GEN, bot, logger
from bot.core import check_registration
from bot.models import User
from bot.texts import NOT_IN_DB_TEXT

@bot.message_handler(commands= ["image_gen"])
@check_registration
def image_gen(message: Message) -> None:
    user_id = message.from_user.id
    user_message = message.text

    try:
        bot.send_message(user_id, user_message)
    except Exception as e:
        bot.send_message(user_id, NOT_IN_DB_TEXT)