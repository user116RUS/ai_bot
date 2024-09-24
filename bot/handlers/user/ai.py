from telebot.types import (
    Message
)

from bot import AI_ASSISTANT, bot, logger, models
from django.shortcuts import get_object_or_404


def chat_with_ai(message: Message) -> None:
    """Chatting with AI handler.  """
    user_id = message.chat.id
    user_message = message.text

    msg = bot.send_message(message.chat.id, 'Думаю над ответом 💭')
    bot.send_chat_action(user_id, 'typing')

    # Все перепроверить, исправить, доделать !!!

    try:
        user_mode = models.UserMode.objects.filter(User=models.User.objects.filter(user_id=user_id))
        # Проверяем количество оставшихся запросов
        if user_mode.requests_amount > 0:
            response = AI_ASSISTANT.get_response_only_text(user_id, user_message)

            # Уменьшаем количество запросов на 1
            user_mode.requests_amount -= 1
            user_mode.save()  # Сохраняем изменения в базе данных
            bot.delete_message(user_id, msg.message_id)
            bot.send_message(user_id, response)

        else:
            bot.delete_message(user_id, msg.message_id)
            bot.send_message(user_id, "У вас исчерпаны запросы. Пожалуйста, пополните баланс.")

    except Exception as e:
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
