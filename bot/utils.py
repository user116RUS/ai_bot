import pytz
from telebot.types import Message
from datetime import datetime

from bot.models import User
from bot import AI_ASSISTANT, bot, logger
from django.utils import timezone

from AI.settings import tz

def is_plan_active(user: User) -> bool:
    now_date = datetime.now().astimezone(tz).strftime("%Y-%m-%d %H:%M")
    
    now_date = datetime.strptime(now_date, "%Y-%m-%d %H:%M")
    plan_end = datetime.strptime(user.plan_end.astimezone(tz).strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")

    try:
        if plan_end > now_date:
            return True
        return False
    except Exception as e:
        print(e)
        return False

def is_there_requests(user:User, mode_model) -> bool:
    
    requests = user.user_mode.modes_request[mode_model]
    if requests > 0:
        return True
    else:
        return False

def get_plan_status(modes: list, user: User, is_plan: bool) -> str:
    status_request = []

    status_text = "\n"

    if is_plan:
        for mode in modes:
            status_request.append([mode.name, user.user_mode.modes_request[mode.model]])

        for x in range(len(status_request)):
            status_text += f"{status_request[x][0]}: {status_request[x][1]} запросов\n"
        date = user.plan_end.astimezone(tz).strftime('%d.%m.%Y %H:%M')
        status = f"Активна до {date} (по МСК)\n\nВаши доступные запросы: {status_text}"

    else:    
        status = "Не активна"
    return status
