from bot import bot, logger
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from bot.models import User, Mode, UserMode
from .user.registration import start_registration
from bot.texts import HELP_TEXT, GREETING_TEXT, MODEL_TEXT, CHOICE_TEXT, HUB_TEXT


def start(message: Message) -> None:
    """Обработчик команды /start  """
    start_registration(message)


def help_(message: Message) -> None:
    """Handler command /help."""

    msg_text = HELP_TEXT
    bot.send_message(message.chat.id, msg_text)


def hub(message: Message) -> None:
    CHOOSE_MODEL_MENU = InlineKeyboardMarkup()
    modes = Mode.objects.filter()
    for mode in modes:
        btn = InlineKeyboardButton(text=f'{mode.name}', callback_data=f'model_{mode.pk}')
        CHOOSE_MODEL_MENU.add(btn)
    bot.send_message(message.chat.id, HUB_TEXT, reply_markup=CHOOSE_MODEL_MENU)


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
