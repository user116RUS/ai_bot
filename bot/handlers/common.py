from telebot.types import (
    Message
)

from bot import bot, logger
from bot.texts import HELP_TEXT, GREETING_TEXT
from bot.models import User, UserMode


def start(message: Message) -> None:
    """Обработчик команды /start  """
    user_id = message.from_user.id

    try:
        text = GREETING_TEXT
        bot.send_message(chat_id=user_id, text=text)
        logger.info(f'{user_id}, started registration')
        return
    except Exception as e:
        logger.info(e)

    # bot.set_state(user_id, AiChattingStates)
    bot.send_chat_action(user_id, "typing")

    logger.info(f"User {message.chat.id}: sent /start command")


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
        for user_mode in user_modes:
            button = InlineKeyboardButton(
                text=f'{user_mode.name}\n {user_mode.model}\n {user_mode.requests_amount}',
                callback_data=f'btw_choice{user_mode.model}'
            )
            CHOICE.add(button)
        text = CHOICE_TEXT
        bot.send_message(chat_id=user_id, text=text, reply_markup=CHOICE)
        logger.info(f'{user_id}, started registration')
        return
    except Exception as e:
        logger.info(e)

    # bot.set_state(user_id, AiChattingStates)
    # bot.send_chat_action(user_id, "typing")

    logger.info(f"User {message.chat.id}: sent /start command")
