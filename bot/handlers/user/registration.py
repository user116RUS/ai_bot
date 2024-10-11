from bot import bot, logger
from bot.texts import GREETING_TEXT
from bot.models import User, UserMode, Mode
from AI.settings import REQUESTS_AMOUNT_BASE


def start_registration(message):
    """ Функция для регистрации пользователей """
    user_id = message.from_user.id

    modes = Mode.objects.all()

    User.objects.update_or_create(
        telegram_id=user_id,
        name=message.from_user.first_name,
        message_context=None,
    )
    user = User.objects.get(telegram_id=user_id)

    # Создание связи Пользователя с его тарифами
    for mode in modes:
        UserMode.objects.update_or_create(
            user=user,
            mode=mode,
            requests_amount=REQUESTS_AMOUNT_BASE if mode.is_base else 0,
            is_actual=True if mode.is_base else False
        )

    logger.info(f'{user_id} registration successful')

    bot.send_chat_action(user_id, "typing")
    bot.send_message(chat_id=user_id, text=GREETING_TEXT)

    logger.info(f"User {message.chat.id}: sent /start command")
