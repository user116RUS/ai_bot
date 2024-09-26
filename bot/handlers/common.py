from telebot.types import (
    Message
)

from bot import bot, logger
from bot.models import User
from bot.texts import HELP_TEXT, GREETING_TEXT


def start(message: Message) -> None:
    """Обработчик команды /start  """
    user_id = message.from_user.id

    try:
        User.objects.update_or_create(
            telegram_id=user_id,
            name=message.from_user.first_name,
            message_context=None,
        )
        text = GREETING_TEXT
        bot.send_message(chat_id=user_id, text=text)
        logger.info(f'{user_id}, started registration')
        return
    except Exception as e:
        logger.info(e)

    bot.send_chat_action(user_id, "typing")

    logger.info(f"User {message.chat.id}: sent /start command")


def help_(message: Message) -> None:
    """Handler command /help."""

    msg_text = HELP_TEXT
    bot.send_message(message.chat.id, msg_text)