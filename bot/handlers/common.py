from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot import bot, logger

from bot.models import User, Mode, UserMode
from bot.texts import HELP_TEXT, GREETING_TEXT, CHOICE_TEXT

from .user.registration import start_registration


def start(message: Message) -> None:
    """Обработчик команды /start  """
    start_registration(message)
    '''if True:
        User.objects.update_or_create(
            telegram_id=user_id,
            name=message.from_user.first_name,
            message_context=None,
        )

        user = User.objects.get(telegram_id=user_id)
        print(user)
        for mode in Mode.objects.filter():
            UserMode.objects.update_or_create(
                user=user,
                mode=mode,
                requests_amount=10 if mode.is_base else 0,
                is_actual=False
            )
        text = GREETING_TEXT
        bot.send_message(chat_id=user_id, text=text)
        logger.info(f'{user_id}, started registration')
        return
    else:
        logger.info(e)
        text = GREETING_TEXT
        bot.send_message(chat_id=user_id, text=text)'''


def help_(message: Message) -> None:
    """Handler command /help."""

    msg_text = HELP_TEXT
    bot.send_message(message.chat.id, msg_text)


def choice(message: Message) -> None:
    """Обработчик команды /choice  """
    user_id = message.from_user.id
    print('work')

    try:
        user = User.objects.get(telegram_id=user_id)
        user_modes = UserMode.objects.filter(user=user)
        choice = InlineKeyboardMarkup()
        for user_mode in user_modes:
            button = InlineKeyboardButton(
                text=f'{user_mode.mode.name}\n {user_mode.mode.model}\n {user_mode.requests_amount}',
                callback_data=f'btw_choice{user_mode.mode.model}'
            )
            choice.add(button)
        text = CHOICE_TEXT
        bot.send_message(chat_id=user_id, text=text, reply_markup=choice)
        logger.info(f'{user_id}, started registration')
        return
    except Exception as e:
        logger.info(e)

    logger.info(f"User {message.chat.id}: sent /start command")
