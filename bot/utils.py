import pytz
from telebot.types import Message
from datetime import datetime

from bot.models import User
from bot import AI_ASSISTANT, bot, logger


def is_plan_active(user: User) -> bool:
    now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(type(now_date), type(user.plan_end))
    now_date = datetime.strptime(now_date, "%Y-%m-%d %H:%M:%S")
    try:
        if user.plan_end < pytz.UTC.localize(now_date):
            return True
        return False
    except Exception as e:
        print(e)
        return False
      

def get_plan_status(modes: list, user: User, is_plan: bool) -> str:
    status_request = []

    status_text = "\n"

    if is_plan:
        for mode in modes:
            status_request.append([mode.name, user.user_mode.modes_request[mode.model]])

        for x in range(len(status_request)):
            status_text += f"{status_request[x][0]}: {status_request[x][1]} запросов\n"
        status = f"Активна до {user.plan_end}\n\nВаши доступные запросы: {status_text}"

    else:    
        status = "Не активна"
    return status
