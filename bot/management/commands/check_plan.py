import pytz
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand, CommandError

from bot.models import User, UserMode


class Command(BaseCommand):
    help = "Checking user's plan status"

    def handle(self, *args, **options):
        users = User.objects.filter(has_plan=True)
        for user in users:
            if user.plan_end.replace(tzinfo=None) + timedelta(hours=2) < (datetime.now().replace(tzinfo=None)):
                print(user.plan_end.replace(tzinfo=None)), print(datetime.now().replace(tzinfo=None) + timedelta(hours=3))
                user.has_plan = False
                user.save()
