import os

import requests
from telebot.types import (
    Message
)

from datetime import datetime

from django.conf import settings
from bot import AI_ASSISTANT, CONVERTING_DOCUMENTS, bot, logger
from bot.core import check_registration
from bot.models import User, Transaction
from bot.texts import NOT_IN_DB_TEXT
from bot.apis.long_messages import split_message, save_message_to_file
from bot.utils import is_plan_active


@check_registration
def chat_with_ai(message: Message) -> None:
    """Chatting with AI handler."""
    user_id = message.chat.id
    user_message = message.text
    msg = bot.send_message(message.chat.id, 'Думаю над ответом 💭')
    bot.send_chat_action(user_id, 'typing')

    try:
        user = User.objects.get(telegram_id=user_id)
        is_plan = is_plan_active(user)
        ai_mode = user.current_mode

        if ((user.balance < 1 and ai_mode.is_base) or (user.balance < 3 and not ai_mode.is_base)) and not is_plan:
            bot.delete_message(user_id, msg.message_id)
            bot.send_message(user_id, "У вас низкий баланс, пополните /start. Или попробуйте поставить базовую модель")
            return

        response = AI_ASSISTANT.get_response(chat_id=user_id, text=user_message, model=ai_mode.model)
        response_message = response["message"]
        if len(response_message) > 4096:
            chunks = split_message(response_message)
            for chunk in chunks:
                if chunks.index(chunk) == 0:
                    try:
                        bot.edit_message_text(chunk, user_id, msg.message_id, parse_mode='Markdown')
                    except:
                        bot.edit_message_text(chunk, user_id, msg.message_id)
                else:
                    try:
                        bot.send_message(user_id, chunk, parse_mode='Markdown')
                    except:
                        bot.send_message(user_id, chunk)
        else:
            try:
                bot.edit_message_text(response_message, user_id, msg.message_id, parse_mode='Markdown')
            except:
                bot.edit_message_text(response_message, user_id, msg.message_id)

        if not is_plan:
            user.balance -= response['total_cost'] * ai_mode.price
            user.save()
        if is_plan:
            user.usermode.modes_request[ai_mode.model] -= 1
            user.save()
    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')
        bot.send_message(settings.GROUP_ID, f'У {user_id} ошибка при chat_with_ai: {e}')
        print(e)


@check_registration
def files_to_text_ai(message: Message) -> None:
    user_id = message.chat.id

    try:
        user = User.objects.get(telegram_id=user_id)
        ai_mode = user.current_mode

        if not ai_mode.is_base:
            bot.send_message(user_id, 'Эта функция доступна только в базовой модели')
            return

        if user.balance < 1:
            bot.send_message(user_id, 'У вас низкий баланс, пополните.')
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

        AI_ASSISTANT.add_txt_to_user_chat_history(user_id, f"Дальше будет текст документа от пользователя. Он может задвать вопросы по нему: {converted_text}")

        if caption:
            bot.edit_message_text(chat_id=user_id, text='Думаю над ответом 💭', message_id=msg.message_id)
            bot.send_chat_action(user_id, 'typing')

            response = AI_ASSISTANT.get_response(chat_id=user_id, text=caption, model=ai_mode.model)
            response_message = response["message"]
            if len(response_message) > 4096:
                chunks = split_message(response_message)
                for chunk in chunks:
                    if chunks.index(chunk) == 0:
                        try:
                            bot.edit_message_text(chunk, user_id, msg.message_id, parse_mode='Markdown')
                        except:
                            bot.edit_message_text(chunk, user_id, msg.message_id)
                    else:
                        try:
                            bot.send_message(user_id, chunk, parse_mode='Markdown')
                        except:
                            bot.send_message(user_id, chunk)
            else:
                try:
                    bot.edit_message_text(response_message, user_id, msg.message_id, parse_mode='Markdown')
                except:
                    bot.edit_message_text(response_message, user_id, msg.message_id)

            user.balance -= response['total_cost'] * ai_mode.price
            user.save()
        else:
            bot.edit_message_text(chat_id=user_id, text="Файл был принят.\nДля очистки контекста нажмите /clear\nКакие вопросы по нему вы хотите задать?", message_id=msg.message_id)

        os.remove(file_path)

    except Exception as e:
        bot.send_message(user_id, NOT_IN_DB_TEXT)
        logger.error(f'Error occurred: {e}')
