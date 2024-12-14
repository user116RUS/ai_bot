from .utils import is_plan_active
from .models import User, UserMode, Mode
from AI import settings
from bot import bot

def dayly_update():
    plan_users = []
    users = User.objects.all()
    modes = Mode.objects.all()
    for user in users:
         if is_plan_active(user):
              plan_users.append(user)
    for user in plan_users:
         usermode = UserMode.objects.update_or_create(
            user=user,
            modes_request={mode.model: settings.DAYLY_AMOUNT for mode in modes}
            )
         usermode.save()

def check_cron():
    bot.send_message(settings.OWNER_ID, 'Gh!')