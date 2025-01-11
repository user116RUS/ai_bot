import os

import requests
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from datetime import datetime
from bot.utils import is_there_requests

from django.conf import settings
from bot import AI_ASSISTANT, CONVERTING_DOCUMENTS, bot, logger
from bot.core import check_registration

from bot.models import User, Transaction, Mode, UserMode
from bot.texts import NOT_IN_DB_TEXT
from bot.handlers.user.image_gen import generate_image
from bot.apis.long_messages import split_message
from bot.keyboards import LONGMESSAGE_BUTTONS
from bot.utils import access_for_subscribers, create_user_quotas


@check_registration
def chat_with_ai(message: Message) -> None:
    """Chatting with AI handler."""
    user_id = message.chat.id
    user_message = message.text
    msg = bot.send_message(message.chat.id, 'Думаю над ответом 💭')
    bot.send_chat_action(user_id, 'typing')

    formed_msg = message.text.lower()
    if 'нарисуй' in formed_msg:
        bot.delete_message(user_id, msg.message_id)
        generate_image(message)
        return

    try:
        user = User.objects.get(telegram_id=user_id)

        if not user.current_mode:
            user.current_mode = Mode.objects.filter(is_base=True).first()
            user.save()
        ai_mode = user.current_mode
        now_mode = UserMode.objects.filter(user=user, mode=ai_mode)

        if not user.user_mode.filter().exists():
            create_user_quotas(user)

        if not now_mode.exists:
            create_user_quotas(user)
            now_mode = UserMode.objects.filter(user=user, mode=ai_mode)
        now_mode = now_mode.first()

        requests_available = is_there_requests(now_mode)
        is_plan_active = user.has_plan
        if (((user.balance < 1 and ai_mode.is_base) or (user.balance < 3 and not ai_mode.is_base)) and not user.has_plan) or (user.has_plan and not requests_available):
            bot.delete_message(user_id, msg.message_id)
            bot.send_message(
                user_id,
                "У вас низкий баланс, пополните /start."
                " Или же пригласите друзей по вашей реферальной ссылке, но лучше оформить подписку!"
            )
            return

        response = AI_ASSISTANT.get_response(chat_id=user_id, text=user_message, model=ai_mode.model, max_token=ai_mode.max_token)
        response_message = response['message']

        if len(response_message) > 4096:    
            user.ai_response = response_message
            user.save()
            bot.edit_message_text(
                "Ответ ИИ слишком длинный, выберте как вы хотите его получить: ",
                user_id,
                msg.message_id,
                reply_markup=LONGMESSAGE_BUTTONS
            )
        else:
            try:
                bot.edit_message_text(
                    text=response_message,
                    chat_id=user_id,
                    message_id=msg.message_id,
                    parse_mode='Markdown')
            except:
                bot.edit_message_text(text=response_message, chat_id=user_id, message_id=msg.message_id)

        if not is_plan_active or not requests_available:
            user.balance -= response['total_cost'] * ai_mode.price
            user.save_balance(comment=f"{ai_mode.name}", type="none")
            user.save()

        if is_plan_active and requests_available:
            now_mode.quota -= 1
            now_mode.save()

    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')
        bot.send_message(settings.GROUP_ID, f'У {user_id} ошибка при chat_with_ai: {e}')
        logger.critical(e)


@access_for_subscribers
@check_registration
def files_to_text_ai(message: Message) -> None:
    user_id = message.chat.id

    try:
        user = User.objects.get(telegram_id=user_id)

        user.mode = 'doc'
        user.save()

        kb = InlineKeyboardMarkup()
        btn_accept = InlineKeyboardButton(text='Выйти из режима документа', callback_data=f'clear')
        kb.add(btn_accept)

        ai_mode = Mode.objects.get(is_base=True)
        now_mode = UserMode.objects.get(user=user, mode=ai_mode)
        is_plan: bool = user.has_plan
        requests_available: bool = is_there_requests(now_mode)

        if not requests_available:
            bot.send_message(user_id, 'У вас закончились базовые запросы.')
            return

        msg = bot.send_message(message.chat.id, 'Начинаю сканировать файл...', reply_to_message_id=message.message_id)

        caption = message.caption

        file_info = bot.get_file(message.document.file_id)
        download_url = f'https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file_info.file_path}'

        r = requests.get(download_url, allow_redirects=True)

        file_name = message.document.file_name
        file_path = os.path.join(
            settings.BASE_DIR, 'temp', 'files', str(message.message_id) + str(file_name[file_name.rfind("."):])
        )

        with open(file_path, 'wb') as new_file:
            new_file.write(r.content)

        converted_text = CONVERTING_DOCUMENTS.convert(str(new_file)[26:-2])

        os.remove(file_path)

        AI_ASSISTANT.add_txt_to_user_chat_history(
            user_id,
            f"Дальше будет текст документа от пользователя. Он может задвать вопросы по нему: {converted_text}"
        )

        if caption:
            bot.edit_message_text(chat_id=user_id, text='Думаю над ответом 💭', message_id=msg.message_id)
            bot.send_chat_action(user_id, 'typing')

            response = AI_ASSISTANT.get_response(
                chat_id=user_id,
                text=caption,
                model=ai_mode,
                max_token=ai_mode.max_token
            )
            response_message = response["message"]
            
            if len(response_message) > 4096:    
                user.ai_response = response_message
                user.save()
                bot.edit_message_text(
                    "Ответ ИИ слишком длинный, выберте как вы хотите его получить: ",
                    user_id, msg.message_id,
                    reply_markup=LONGMESSAGE_BUTTONS
                )
            else:
                try:
                    bot.edit_message_text(response_message, user_id, msg.message_id, parse_mode='Markdown')
                except:
                    bot.edit_message_text(response_message, user_id, msg.message_id)

            if not is_plan or not requests_available:
                user.balance -= response['total_cost'] * ai_mode.price
                user.save()

            if is_plan and requests_available:
                now_mode -= 1
                now_mode.save()
        else:
            bot.edit_message_text(
                chat_id=user_id,
                text="Файл был принят.\nДля очистки контекста нажмите /clear\n"
                     "Какие вопросы по нему вы хотите задать?",
                message_id=msg.message_id)

    except Exception as e:
        bot.send_message(user_id, NOT_IN_DB_TEXT)
        logger.error(f'Error occurred: {e}')
