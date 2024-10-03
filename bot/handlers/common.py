from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from bot.models import Mode, UserMode, User
from bot import bot, logger
from bot.texts import HELP_TEXT, GREETING_TEXT


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


def hub(message: Message) -> None:
    CHOOSE_MODEL_MENU = InlineKeyboardMarkup()
    for i in range(len(Mode.pk)):
        btn = InlineKeyboardButton(text=f'{Mode.pk[i]} модель', callback_data=f'model_{Mode.pk[i]}')
        CHOOSE_MODEL_MENU.add(btn)
    txt = 9
    bot.send_message(message.chat.id, txt, reply_markup=CHOOSE_MODEL_MENU)


def help_(message: Message) -> None:
    """Handler command /help."""

    msg_text = HELP_TEXT
    bot.send_message(message.chat.id, msg_text)