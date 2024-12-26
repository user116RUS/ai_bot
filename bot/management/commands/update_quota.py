from django.core.management.base import BaseCommand

from bot.utils import update_user_quotas
from bot.models import User


class Command(BaseCommand):
    help = "Checking user's plan status"

    def handle(self, *args, **options):
        users = User.objects.filter(has_plan=True)
        for user in users:
            update_user_quotas(user)
            user.save()
            