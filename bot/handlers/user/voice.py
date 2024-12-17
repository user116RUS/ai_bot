import os

from telebot.types import (
    Message
)

from bot import AI_ASSISTANT, WHISPER_RECOGNITION, bot, logger
from bot.apis.voice_recognition import convert_ogg_to_mp3
from bot.handlers import clear_chat_history
from bot.core import check_registration
from bot.models import User
from django.conf import settings
from bot.apis.long_messages import save_message_to_file, split_message
from bot.keyboards import LONGMESSAGE_BUTTONS


@check_registration
def voice_handler(message: Message) -> None:
    """Whisper voice handler."""
    user_id = message.chat.id

    msg = bot.send_message(message.chat.id, 'Слушаю вопрос 🎶')

    user = User.objects.get(telegram_id=user_id)
    ai_mode = user.current_mode
    max_token = ai_mode.max_token

    if (user.balance < 2 and not ai_mode.is_base) or (ai_mode.is_base and user.balance < 1):
        bot.delete_message(user_id, msg.message_id)
        bot.send_message(user_id, 'У вас мало средств на балансе(\n Пополните баланс или выберете базовую модель')
        return

    try:
        file_id = message.voice.file_id
        file_info = bot.get_file(file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = settings.BASE_DIR / 'temp' / 'voice' / f'{message.message_id}.ogg'
        name = message.chat.first_name if message.chat.first_name else 'No_name'
        logger.info(f"Chat {name} (ID: {message.chat.id}) download file {file_name}")

        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        converted_file_path = convert_ogg_to_mp3(file_name)

        text = WHISPER_RECOGNITION.recognize(converted_file_path)

        bot.edit_message_text(chat_id=user_id, text='Думаю над ответом 💭', message_id=msg.message_id)
        bot.send_chat_action(user_id, 'typing')


        os.remove(converted_file_path)
        os.remove(file_name)

        response = AI_ASSISTANT.get_response(chat_id=user_id, text=text, model=ai_mode.model, max_token=max_token)
        response_message = response["message"]
        
        if len(response_message) > 4096:    
            user.ai_response = response_message
            bot.edit_message_text("Ответ ИИ слишком длинный, выберте как вы хотите его получить: ", user_id, msg.message_id, reply_markup=LONGMESSAGE_BUTTONS)
        else:
            try:
                bot.edit_message_text(response_message, user_id, msg.message_id, parse_mode='Markdown')
            except:
                bot.edit_message_text(response_message, user_id, msg.message_id)

        user.balance -= response['total_cost'] * ai_mode.price
        user.save()

    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')
        bot.send_message(settings.OWNER_ID, f'У {user_id} ошибка при whisper_recognition: {e}')
        clear_chat_history(message)
        logger.error(f'Error occurred: {e}')
