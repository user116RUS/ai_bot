from bot import bot, logger
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
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


def choice(message: Message) -> None:
    """Обработчик команды /choice  """
    user_id = message.from_user.id
    print('work')

    try:
        user = User.objects.get(telegram_id=user_id)
        user_modes = UserMode.objects.filter(user=user)
        choice_keyboard = InlineKeyboardMarkup()
        for user_mode in user_modes:
            text = f'{user_mode.mode.name}\nостаток: {user_mode.requests_amount} {"✅" if user_mode.is_actual else ""}'
            button = InlineKeyboardButton(
                text=text,
                callback_data=f'mode_choice#{user_mode.mode.pk}'
            )
            choice_keyboard.add(button)
        text = CHOICE_TEXT
        bot.send_message(chat_id=user_id, text=text, reply_markup=choice_keyboard)
        # logger.info(f'{user_id}, started registration')
    except Exception as e:
        logger.info(e)
    # logger.info(f"User {message.chat.id}: sent /start command")


def choice_handler(call: CallbackQuery) -> None:
    """Обработчик callback /choice """
    _, pk = call.data.split("#")
    user_id = call.from_user.id
    try:
        user = User.objects.get(telegram_id=user_id)
        user_modes = UserMode.objects.filter(user=user)

        for user_mode in user_modes:
            if user_mode.mode.pk == pk:
                user_mode.is_actual = True
            else:
                user_mode.is_actual = False
        user_modes.save()

    except Exception as e:
        logger.info(e)

    logger.info(f"User {call.chat.id}: switched user_mode")
