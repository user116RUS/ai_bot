from telebot.types import (
    Message
)

from bot import bot, logger
from bot.texts import GREETING_TEXT
from .models import User


def choice(message: Message) -> None:
    """Обработчик команды /start  """
    user_id = message.from_user.id

    try:
        CHOICE = types.ReplyKeyboardMarkup(row_width=2)
        user = User.object.get(telegram_id=user_id)
        user_modes = UserMode.objects.filter(user=user)
        cnt = 0
        for user_mode in user_modes:
            BUTTON = InlineKeyboardButton(
                text=f'{user_mode.name}\n {user_mode.model}\n {user_mode.requests_amount}',
                callback_data=f'btw_choice{cnt}'
            )
            CHOICE.add(BUTTON)
            cnt += 1

        text = GREETING_TEXT
        bot.send_message(chat_id=user_id, text=text, reply_markup=CHOICE)
        logger.info(f'{user_id}, started registration')
        return
    except Exception as e:
        logger.info(e)

    # bot.set_state(user_id, AiChattingStates)
    bot.send_chat_action(user_id, "typing")

    logger.info(f"User {message.chat.id}: sent /start command")
