import logging

import mtranslate

from telebot.types import (
    CallbackQuery,
    Message
)

from django.conf import settings

from bot import AI_ASSISTANT, bot
from bot.core import check_registration
from bot.models import User, Mode, UserMode
from .registration import start_registration
from bot.texts import WE_ARE_WORKING
from bot.utils import is_there_requests


@check_registration
def image_gen(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id
    message_id = callback.message.id

    try:
        msg = bot.edit_message_text(chat_id=user_id, message_id=message_id, text='Пожалуйста напишите ваш запрос для генерации изображения:\n(Для отмены отправте команду /start)')

        bot.register_next_step_handler(msg, generate_image)
    except Exception as e:
        logging.error(e)
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')


def generate_image(message: Message) -> None:
    user_id = message.chat.id
    user_message = message.text

    try:
        user = User.objects.get(telegram_id=user_id)

        image_mode = Mode.objects.filter(is_image=True)

        if not image_mode.exists():
            bot.send_message(chat_id=settings.OWNER_ID, text="Добавь режимы, и хоть один базовый!")
            bot.send_message(chat_id=user_id, text=WE_ARE_WORKING)
            return

        image_mode = image_mode.first()

        if user.balance < 3:
            bot.send_message(user_id, "У вас низкий баланс, пополните /start.")
            return
        
        if user_message == "/start":
            start_registration(message)
            return

        now_mode = UserMode.objects.filter(user=user, mode=image_mode).first()
        requests_available = is_there_requests(now_mode)

        msg = bot.send_message(user_id, 'Ваш запрос генерируется...')

        user_message = mtranslate.translate(user_message, "en", "auto")

        image = AI_ASSISTANT.generate_image(user_message, image_mode.model)
        
        bot.delete_message(user_id, msg.message_id)
        bot.send_photo(user_id, image)

        if not user.has_plan or not requests_available:
            user.balance -= 1.25
            user.save_balance(comment=f"{image_mode.name}", type="none")
            user.save()

        if user.has_plan and requests_available:
            now_mode.quota -= 1
            now_mode.save()

        start_registration(message, delete=False)

    except Exception as e:
        bot.send_message(user_id, 'Пока мы чиним бот. Если это продолжается слишком долго, напишите нам - /help')
        print(e)
