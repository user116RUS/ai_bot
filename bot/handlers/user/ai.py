from telebot.types import (
    Message
)

from bot import AI_ASSISTANT, bot, logger
from bot.models import Mode, UserMode, User
from bot.texts import NOT_IN_DB_TEXT


def chat_with_ai(message: Message) -> None:
    """Chatting with AI handler.  """
    user_id = message.chat.id
    user_message = message.text

    msg = bot.send_message(message.chat.id, 'Думаю над ответом 💭')
    bot.send_chat_action(user_id, 'typing')

    try:
        user = User.objects.get(telegram_id=user_id)
        user_modes = user.user_mode

        print(user_modes)

        for user_mode in user_modes.all():
            if user_mode.is_actual is False:
                pass
            else:
                ai_mode = user_mode
                print(ai_mode)

                # Проверяем количество оставшихся запросов
                if ai_mode.requests_amount > 0:
                    response = AI_ASSISTANT.get_response(chat_id=user_id, text=user_message, model=ai_mode)

                    # Уменьшаем количество запросов на 1
                    ai_mode.requests_amount -= 1
                    ai_mode.save()  # Сохраняем изменения в базе данных
                    bot.delete_message(user_id, msg.message_id)
                    bot.send_message(user_id, response)

                else:
                    bot.delete_message(user_id, msg.message_id)
                    bot.send_message(user_id, "У вас исчерпаны запросы. Пожалуйста, пополните баланс.")

    except Exception as e:
        bot.send_message(user_id, NOT_IN_DB_TEXT)
        AI_ASSISTANT.clear_chat_history(user_id)
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
