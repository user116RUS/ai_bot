from telebot.types import Message
from datetime import datetime

from bot.models import User
from bot import AI_ASSISTANT, bot, logger


def is_plan_active(user: User) -> bool:
    now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if user.plan_end < now_date:
        return True
    return False
