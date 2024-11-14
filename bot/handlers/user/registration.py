from bot import bot, logger
from bot.texts import GREETING_TEXT, WE_ARE_WORKING
from bot.models import User, Mode

from django.conf import settings


def start_registration(message):
    """ Функция для регистрации пользователей """
    user_id = message.from_user.id

    modes = Mode.objects.filter(is_base=True)
    if not modes.exists():
        bot.send_message(chat_id=settings.OWNER_ID, text="Добавь режимы, и хоть одит базовый!")
        bot.send_message(chat_id=user_id, text=WE_ARE_WORKING)
        return

    if not User.objects.filter(telegram_id=user_id).exists():

        User.objects.update_or_create(
            telegram_id=user_id,
            name=message.from_user.first_name,
            message_context=None,
            balance=10,
            current_mode=modes[0]
        )

        logger.info(f'{user_id} registration successful')

        bot.send_chat_action(user_id, "typing")
        bot.send_message(chat_id=user_id, text=GREETING_TEXT)

        logger.info(f"User {message.chat.id}: sent /start command")
    else:
        bot.send_message(user_id, GREETING_TEXT)
