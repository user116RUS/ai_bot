from traceback import format_exc

from asgiref.sync import sync_to_async
from bot.apis.yookassa.youkassa import pay_for_mode
from bot.handlers import *
from bot.handlers.admin import *
from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from telebot.apihelper import ApiTelegramException
from telebot.types import Update

from bot import bot, logger


@require_GET
def set_webhook(request: HttpRequest) -> JsonResponse:
    """Setting webhook."""
    bot.set_webhook(url=f"{settings.HOOK}/bot/{settings.BOT_TOKEN}")
    bot.send_message(settings.OWNER_ID, "webhook set")
    return JsonResponse({"message": "OK"}, status=200)


@require_GET
def status(request: HttpRequest) -> JsonResponse:
    return JsonResponse({"message": "OK"}, status=200)


@csrf_exempt
@require_POST
@sync_to_async
def index(request: HttpRequest) -> JsonResponse:
    if request.META.get("CONTENT_TYPE") != "application/json":
        return JsonResponse({"message": "Bad Request"}, status=403)

    json_string = request.body.decode("utf-8")
    update = Update.de_json(json_string)
    try:
        bot.process_new_updates([update])
    except ApiTelegramException as e:
        logger.error(f"Telegram exception. {e} {format_exc()}")
    except ConnectionError as e:
        logger.error(f"Connection error. {e} {format_exc()}")
    except Exception as e:
        user_id = update.message.from_user.id if update.message else update.callback_query.from_user.id
        bot.send_message(user_id, 'help')
        logger.error(f"Unhandled exception. {e} {format_exc()}")
    return JsonResponse({"message": "OK"}, status=200)


"""
Common
"""


start = bot.message_handler(commands=["start"])(start)
top_up_balance = bot.message_handler(commands=["buy"])(top_up_balance)
generate_ref_link = bot.message_handler(commands=["generate_ref_link"])(generate_ref_link)
menu = bot.message_handler(commands=["menu"])(menu)
clear_chat_history = bot.message_handler(commands=["clear"])(clear_chat_history)


get_sum = bot.callback_query_handler(lambda c: c.data.startswith('accept_'))(get_sum)
chat_with_ai = bot.message_handler(func=lambda message: True)(chat_with_ai)

pay_for_mode = bot.callback_query_handler(lambda call: call.data.startswith("pay_"))(pay_for_mode)


help_ = bot.callback_query_handler(lambda c: c.data == "help")(help_)
choice = bot.callback_query_handler(lambda c: c.data == "choice")(choice)
buy = bot.callback_query_handler(lambda c: c.data == 'buy')(buy)
clear_chat_history = bot.callback_query_handler(lambda c: c.data == 'clear')(clear_chat_history)
personal_account = bot.callback_query_handler(lambda c: c.data == "lc")(personal_account)

back_handler = bot.callback_query_handler(lambda c: c.data == "back")(back_handler)