from datetime import datetime

from django.db import transaction

from bot.models import User, UserMode, Mode
from AI.settings import tz


"""def is_plan_active(user: User) -> bool:
    now_date = datetime.now().astimezone(tz).strftime("%Y-%m-%d %H:%M")
    
    now_date = datetime.strptime(now_date, "%Y-%m-%d %H:%M")
    plan_end = datetime.strptime(user.plan_end.astimezone(tz).strftime("%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")

    try:
        if plan_end > now_date:
            return True
        return False
    except Exception as e:
        print(e)
        return False"""



def is_there_requests(now_mode) -> bool:

    if now_mode.quota > 0:
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


def update_user_quotas(user: User):
    user_modes = UserMode.objects.filter(user=user)
    if not user_modes.exists():
        create_user_quotas(user)

    for user_mode_quota in user_modes:
        mode = user_mode_quota.mode
        user_mode_quota.quota = mode.daily_quota
        user_mode_quota.save()


def create_user_quotas(user):
    all_modes = Mode.objects.all()
    for mode in all_modes:
        UserMode.objects.get_or_create(
            user=user,
            mode=mode,
            defaults={'quota': mode.daily_quota}
        )
