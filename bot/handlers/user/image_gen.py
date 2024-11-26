import threading
import queue

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
from bot.keyboards import UNIVERSAL_BUTTONS

@check_registration
def image_gen(callback: CallbackQuery) -> None:
    try:
        user_id = callback.from_user.id
        message_id = callback.message.id

        msg = bot.edit_message_text(chat_id=user_id, message_id=message_id, text='Пожалуйста напишите ваш запрос для генерации изображения: ', reply_markup=UNIVERSAL_BUTTONS)

        if callback.data != 'image_gen':
            return
        
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

        bot.delete_message(user_id, message.message_id)

        msg = bot.send_message(user_id, 'Генерирую изображение...')

        result_queue = queue.Queue()
        threading.Thread(target=IMAGE_GEN.generate_image_fusion, args=(user_message, settings.CURRENT_MODEL)).start()
        image_url = result_queue.get()

        bot.send_message(user_id, image_url)
        return
        
        bot.send_message(user_id, str(image_url))

        bot.delete_message(user_id, msg.message_id)
        bot.send_photo(user_id, image_url)
        start_registration(message)

        user.balance -= 1
        user.save()

    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')