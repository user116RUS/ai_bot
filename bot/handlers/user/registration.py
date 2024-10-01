from bot import bot, logger
from bot.texts import GREETING_TEXT
from bot.models import User, UserMode, Mode
from AI.settings import REQUESTS_AMOUNT_BASE


def start_registration(message):
    """ Функция для регистрации пользователей """
    user_id = message.from_user.id
    modes = Mode.objects.filter() # Достаем все Моды ИИ
    users = User.objects.filter(telegram_id=user_id) # Достаем пользователя по айди
    print(users)

    # Проверка на наличие пользователя в дб, если такового нет - он создается
    if len(users) == 0:
        # Добавление пользователя в БД
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
                is_actual=False
            )

        logger.info(f'{user_id}, started registration')
    else:
        logger.info(f"{user_id} attempt repeated registration")

    bot.send_message(chat_id=user_id, text=GREETING_TEXT)
    bot.send_chat_action(user_id, "typing")

    logger.info(f"User {message.chat.id}: sent /start command")
