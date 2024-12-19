import mtranslate

from telebot.types import (
    CallbackQuery,
    Message
)

from asgiref.sync import sync_to_async
from django.conf import settings
from bot import AI_ASSISTANT, bot
from bot.core import check_registration
from bot.models import User
from bot.texts import NOT_IN_DB_TEXT
from .registration import start_registration
from bot.keyboards import UNIVERSAL_BUTTONS

@check_registration
def image_gen(callback: CallbackQuery) -> None:
    try:
        user_id = callback.from_user.id
        message_id = callback.message.id

        msg = bot.edit_message_text(chat_id=user_id, message_id=message_id, text='Пожалуйста напишите ваш запрос для генерации изображения:\n(Для отмены отправте команду /start)')

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
        
        if user_message == "/start":
            start_registration(message)
            return

        msg = bot.send_message(user_id, 'Ваш запрос генерируется...')

        user_message = mtranslate.translate(user_message, "en", "auto")

        image = AI_ASSISTANT.generate_image(user_message)
        
        bot.delete_message(user_id, msg.message_id)
        bot.send_photo(user_id, image)
        
        user.balance -= 1.25
        user.save()

        start_registration(message, delete=False)

    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')
