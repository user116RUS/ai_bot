from functools import wraps
from datetime import datetime

from telebot.types import Message
from bot import bot, logger

from AI import settings
from bot.texts import ADMIN_PANEL_TEXT
from bot.models import User

def admin_permission(func):
    """
    Checking user for admin permission to access the function.
    """
    @wraps(func)
    def wrapped(message: Message) -> None:
        user_id = message.from_user.id
        user = User.objects.get(telegram_id=user_id)
        if not user.is_admin:
            bot.send_message(user_id, '⛔ У вас нет администраторского доступа')
            logger.warning(f'Попытка доступа к админ панели от {user_id}')
            return
        return func(message)
    return wrapped

@admin_permission
def admin_panel(message: Message):
    user_id = message.from_user.id
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(chat_id=message.chat.id,
                     text=f"{ADMIN_PANEL_TEXT}, {user_id}\n\nВот статистика за {datetime.now().month}:\n\nПотрачено токенов пользователями: {settings.token_counter}",
    )