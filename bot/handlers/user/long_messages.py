from telebot.types import (
    CallbackQuery,
)

from django.conf import settings
from bot import bot
from bot.models import User
from bot.apis.long_messages import split_message, save_message_to_file
from bot.keyboards import DOCUMENT_BUTTONS, LONGMESSAGE_BUTTONS

def long_message_get_send_option(call: CallbackQuery):
    user_id = call.from_user.id
    _, way = call.data.split('_')

    user = User.objects.get(telegram_id=user_id)
    response_message = user.ai_response

    try:
        if way == "msg":            
            chunks = split_message(response_message)
            for chunk in chunks:
                if chunks.index(chunk) == 0:
                    try:
                        bot.edit_message_text(chunk, user_id, call.message.id, parse_mode='Markdown', reply_markup=None)
                    except:
                        bot.edit_message_text(chunk, user_id, call.message.id, reply_markup=None)
                else:
                    try:
                        bot.send_message(user_id, chunk, parse_mode='Markdown', reply_markup=None)
                    except:
                        bot.send_message(user_id, chunk, reply_markup=None)
            
            user.ai_response = None
            user.save()
            
        elif way == "docs":
            bot.edit_message_reply_markup(user_id, call.message.id, reply_markup=DOCUMENT_BUTTONS)
        

    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')
        bot.send_message(settings.GROUP_ID, f'У {user_id} ошибка при long_message_get_send_option: {e}')
        
        user.ai_response = None
        user.save()

def long_message_get_send_option_docs(call: CallbackQuery):
    user_id = call.from_user.id
    _, extension = call.data.split('_')

    user = User.objects.get(telegram_id=user_id)
    response_message = user.ai_response

    try:
        if extension == 'pdf':
            bot.delete_message(user_id, call.message.id)
            bot.send_document(user_id, save_message_to_file(response_message, 'pdf'), caption="Ваш ответ", reply_markup=None)
            
            user.ai_response = None
            user.save()
        elif extension == 'docx':
            bot.delete_message(user_id, call.message.id)
            bot.send_document(user_id, save_message_to_file(response_message, 'docx'), caption="Ваш ответ", reply_markup=None)

            user.ai_response = None
            user.save()
        
        if extension == 'back':
            bot.edit_message_reply_markup(user_id, call.message.id, reply_markup=LONGMESSAGE_BUTTONS)

    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')
        bot.send_message(settings.GROUP_ID, f'У {user_id} ошибка при long_message_get_send_option_docs: {e}')
        
        user.ai_response = None
        user.save()