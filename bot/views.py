from traceback import format_exc

from asgiref.sync import sync_to_async
from bot.apis.yookassa.youkassa import pay_for_mode
from bot.handlers import *
from bot.handlers.admin import *
from bot.handlers.user.ai import files_to_text_ai
from bot.handlers.user.image_gen import image_gen
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
        bot.send_message(settings.OWNER_ID, f'Error from index: {e}')
        logger.error(f"Unhandled exception. {e} {format_exc()}")
    return JsonResponse({"message": "OK"}, status=200)


"""
Common
"""

admin_panel = bot.message_handler(commands=["admin"])(admin_panel)
clear_chat_history = bot.message_handler(commands=["clear"])(clear_chat_history)
start = bot.message_handler(commands=["start"])(start)
help_ = bot.message_handler(commands=["help"])(help_)
transaction = bot.message_handler(commands=["balance"])(balance)
get_ref_link = bot.callback_query_handler(lambda c: c.data == "referal")(get_ref_link)

files_to_text_ai = bot.message_handler(content_types=["file", "document"])(files_to_text_ai)

get_sum = bot.callback_query_handler(lambda c: c.data.startswith('accept_'))(get_sum)
chat_with_ai = bot.message_handler(func=lambda message: True)(chat_with_ai)

pay_for_mode = bot.callback_query_handler(lambda call: call.data.startswith("pay_"))(pay_for_mode)
choice_pay = bot.callback_query_handler(lambda c: c.data == "payment")(choice_pay)

choice = bot.callback_query_handler(lambda c: c.data == "choice")(choice)
image_gen = bot.callback_query_handler(lambda c: c.data == 'image_gen')(image_gen)
buy = bot.callback_query_handler(lambda c: c.data.startswith('buy_'))(top_up_balance)
image_gen = bot.callback_query_handler(lambda c: c.data == 'image_gen')(image_gen)

month_statistic = bot.callback_query_handler(lambda c: c.data.startswith("month_"))(month_statistic)
choice_handler = bot.callback_query_handler(lambda c: c.data.startswith('choice_'))(choice_handler)
back_handler = bot.callback_query_handler(lambda c: c.data == "back")(back_handler)
purchase_handler = bot.callback_query_handler(lambda c: c.data.startswith("model_"))(purchase_handler)
# top_up_balance = bot.callback_query_handler(lambda c: c.data.startswith("pay_"))(top_up_balance) ЮКасса

voice_handler = bot.message_handler(content_types=["voice", "audio"])(voice_handler)

reject_payment = bot.callback_query_handler(lambda c: c.data.startswith('reject_'))(reject_payment)
