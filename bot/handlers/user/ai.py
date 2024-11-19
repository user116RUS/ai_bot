from telebot.types import (
    Message
)

from bot import AI_ASSISTANT, WHISPER_RECOGNITION, bot, logger
from bot.apis.voice_recognition import convert_ogg_to_mp3
from bot.core import check_registration
from bot.models import Mode, User
from bot.texts import NOT_IN_DB_TEXT

import os


@check_registration
def chat_with_ai(message: Message) -> None:
    """Chatting with AI handler.  """
    user_id = message.chat.id
    user_message = message.text

    msg = bot.send_message(message.chat.id, 'Думаю над ответом 💭')
    bot.send_chat_action(user_id, 'typing')

    if True:
        user = User.objects.get(telegram_id=user_id)
        ai_mode = user.current_mode

        if user.balance > 1:
            response = AI_ASSISTANT.get_response(chat_id=user_id, text=user_message, model=ai_mode.model, User=User)

            user.balance -= response['total_cost'] * ai_mode.price
            user.save()
            bot.edit_message_text(response['message'], user_id, msg.message_id)

        else:
            bot.delete_message(user_id, msg.message_id)
            bot.send_message(user_id, "У вас низкий баланс, пополните /buy.")

'''    except Exception as e:
        bot.send_message(user_id, NOT_IN_DB_TEXT)
        AI_ASSISTANT.clear_chat_history(user_id)
        logger.error(f'Error occurred: {e}')'''


@bot.message_handler(content_types=["voice", "audio"])
@check_registration
def whisper_voice(message: Message) -> None:
    """Whisper voice handler."""
    user_id = message.chat.id

    msg = bot.send_message(message.chat.id, 'Слушаю вопрос 🎶')

    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = f"temp/voice/{message.message_id}.ogg"
    name = message.chat.first_name if message.chat.first_name else 'No_name'
    logger.info(f"Chat {name} (ID: {message.chat.id}) download file {file_name}")

    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)


    try:
        user = User.objects.get(telegram_id=user_id)
        user_modes = user.user_mode

        for user_mode in user_modes.all():
            if user_mode.is_actual is False:
                pass
            else:
                if message.voice is not None:
                    file_info = bot.get_file(message.voice.file_id)
                    converted_file_path = convert_ogg_to_mp3(file_name)
                else:
                    file_info = bot.get_file(message.audio.file_id)
                    converted_file_path = convert_ogg_to_mp3(file_name)

                text = WHISPER_RECOGNITION.recognize(converted_file_path)
                bot.edit_message_text(chat_id=user_id, text='Думаю над ответом 💭', message_id=msg.message_id)
                bot.send_chat_action(user_id, 'typing')

                ai_mode = str(user_mode.mode.model)

                if user_mode.requests_amount > 0:
                    response = AI_ASSISTANT.get_response(chat_id=user_id, text=text, model=ai_mode)

                    # Уменьшаем количество запросов на 1
                    user_mode.requests_amount -= 1
                    user_mode.save()  # Сохраняем изменения в базе данных
                    bot.delete_message(user_id, msg.message_id)
                    bot.send_message(user_id, response)
                    os.remove(converted_file_path)

                else:
                    bot.delete_message(user_id, msg.message_id)
                    bot.send_message(user_id, "У вас исчерпаны запросы. Пожалуйста, пополните баланс.")
    except Exception as e:
        bot.send_message(user_id, NOT_IN_DB_TEXT)
        #AI_ASSISTANT.clear_chat_history(user_id)
        logger.error(f'Error occurred: {e}')


def clean_history(message: Message) -> None:
    """Clean AI chatting history."""
    try:
        AI_ASSISTANT.clear_chat_history(message.chat.id)
        bot.send_message(message.chat.id, 'Успешно')
    except Exception as e:
        bot.send_message(message.chat.id, 'Уже очищено')
        logger.error(e)
    return
