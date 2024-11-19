import os

import requests
from telebot.types import (
    Message
)

from django.conf import settings
from bot import AI_ASSISTANT, CONVERTING_DOCUMENTS, bot, logger
from bot.core import check_registration
from bot.models import User
from bot.texts import NOT_IN_DB_TEXT


@check_registration
def chat_with_ai(message: Message) -> None:
    """Chatting with AI handler.  """
    user_id = message.chat.id
    user_message = message.text

    msg = bot.send_message(message.chat.id, 'Думаю над ответом 💭')
    bot.send_chat_action(user_id, 'typing')

    try:
        user = User.objects.get(telegram_id=user_id)
        ai_mode = user.current_mode

        if user.balance > 1:
            response = AI_ASSISTANT.get_response(chat_id=user_id, text=user_message, model=ai_mode.model)

            bot.edit_message_text(response['message'], user_id, msg.message_id)

            user.balance -= response['total_cost'] * ai_mode.price
            user.save()

        else:
            bot.delete_message(user_id, msg.message_id)
            bot.send_message(user_id, "У вас низкий баланс, пополните /start.")
    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')
        bot.send_message(settings.OWNER_ID, f'У {user_id} ошибка при chat_with_ai: {e}')
        AI_ASSISTANT.clear_chat_history(user_id)
        #logger.error(f'Error occurred: {e}')
        print(f'Error occurred: {e}')


@bot.message_handler(content_types=["file", "document"])
@check_registration
def files_to_text_ai(message: Message) -> None:
    user_id = message.chat.id

    try:
        user = User.objects.get(telegram_id=user_id)
        ai_mode = user.current_mode

        if user.balance < 1:
            bot.send_message(user_id, 'У вас низкий баланс, пополните.')
            return
        
        msg = bot.send_message(message.chat.id, 'Начинаю сканировать файл...')

        caption = message.caption

        file_info = bot.get_file(message.document.file_id)
        download_url = f'https://api.telegram.org/file/bot{settings.BOT_TOKEN}/{file_info.file_path}'

        r = requests.get(download_url, allow_redirects=True)

        file_name = message.document.file_name
        file_path = os.path.join(settings.BASE_DIR, 'temp', 'files', f"{message.message_id}.{user_id}.{file_name}")

        with open(file_path, 'wb') as new_file:
            new_file.write(r.content)
                    
        #converted_text = CONVERTING_DOCUMENTS.convert(new_file)
        bot.edit_message_text(chat_id=user_id, text=str(new_file)[26:-5], message_id=msg.message_id)
        return
        AI_ASSISTANT.add_txt_to_user_chat_history(user_id, converted_text)

        if caption:
            bot.edit_message_text(chat_id=user_id, text='Думаю над ответом 💭', message_id=msg.message_id)
            bot.send_chat_action(user_id, 'typing')

            response = AI_ASSISTANT.get_response(chat_id=user_id, text=caption, model=ai_mode.model)

            bot.edit_message_text(response['message'], user_id, msg.message_id)

            user.balance -= response['total_cost'] * ai_mode.price
            user.save()
        else:
            bot.edit_message_text(chat_id=user_id, text="Файл был принят.\n Какие вопросы по нему вы хотите задать?", message_id=msg.message_id)

        os.remove(converted_text)

    except Exception as e:
        bot.send_message(user_id, NOT_IN_DB_TEXT)
        #logger.error(f'Error occurred: {e}')
        print(f'Error occurred: {e}')