from telebot.types import (
    CallbackQuery,
    Message
)

from django.conf import settings
from bot import IMAGE_GEN, AI_ASSISTANT, bot
from bot.core import check_registration
from bot.models import User
from bot.texts import NOT_IN_DB_TEXT
from .registration import start_registration

@check_registration
def image_gen(callback: CallbackQuery) -> None:
    try:
        user_id = callback.from_user.id
        message_id = callback.message.message_id
        
        bot.delete_message(user_id, message_id)

        msg = bot.send_message(chat_id=user_id, text='Пожалуйста напишите ваш запрос для генерации изображения: ')

        bot.register_next_step_handler(msg, generate_image)

    except Exception as e:
        pass
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')

def generate_image(message: Message) -> None:
    user_id = message.chat.id
    user_message = message.text

    try:
        user = User.objects.get(telegram_id=user_id)

        if user.balance < 1:
            bot.send_message(user_id, "У вас низкий баланс, пополните /start.")
            return

        response = IMAGE_GEN.generate_text_to_image(text=user_message, model=settings.CURRENT_MODEL)["url"]

        user.balance -= 1
        user.save()

        bot.send_photo(user_id, response)

        bot.delete_message(user_id, message.message_id)
        start_registration(message)
    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')