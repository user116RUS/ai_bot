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
        choice = InlineKeyboardMarkup()
        for user_mode in user_modes:
            button = InlineKeyboardButton(
                text=f'{user_mode.mode.name}\nостаток: {user_mode.requests_amount} {"✅" if user_mode.is_actual else ""}',
                callback_data=f'choice_{user_mode.pk}'
            )
            choice.add(button)
            print(user_mode.pk, user_modes)
            print(button.callback_data)
        text = CHOICE_TEXT
        bot.send_message(chat_id=user_id, text=text, reply_markup=choice)
        logger.info(f'{user_id}, started registration')
        return
    except Exception as e:
        logger.info(e)

    logger.info(f"User {message.chat.id}: sent /start command")


def hub():
    print("hi")


def pick_me(callback: CallbackQuery) -> None:
    """Обработчик callback /choice """
    print("123123")
    pk = callback.data.split("_")
    try:
        user_modes = UserMode.objects.filter(pk=pk)

        for user_mode in user_modes:
            if user_mode.pk == pk:
                user_mode.is_actual = True
            else:
                break
        user_modes.save()

    except Exception as e:
        logger.info(e)

    logger.info(f"User {callback.chat.id}: sent /start command")
