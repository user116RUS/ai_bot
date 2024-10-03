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


def pick_me(call: CallbackQuery) -> None:
    """Обработчик callback /choice """
    user_id = call.from_user.id
    try:
        user = User.objects.get(telegram_id=user_id)
        user_mode = UserMode.objects.filter(user=user)

        for user_mods in user_mode:
            if user_mods.mode.pk == call.data:
                user_mods.is_actual = True
            else:
                user_mods.is_actual = False
        user_mode.save()
        
    except Exception as e:
        logger.info(e)
    
    logger.info(f"User {call.chat.id}: sent /start command")