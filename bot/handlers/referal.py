import hashlib

from bot import bot, logger
from django.conf import settings
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from bot.models import User, Transaction
from bot.keyboards import UNIVERSAL_BUTTONS


def generate_ref_link(user_id: int) -> str:
    """Генерирует реферальную ссылку для пользователя."""
    # Создаем уникальный хеш на основе user_id
    hash_object = hashlib.md5(str(user_id).encode())
    ref_code = hash_object.hexdigest()[:8]
    return f"https://t.me/{settings.BOT_NAME}?start=ref_{ref_code}"


def handle_ref_link(message: Message) -> None:
    """Обработчик реферальных ссылок."""
    try:
        # Получаем реферальный код из сообщения
        ref_code = message.text.split('ref_')[1]
        new_user_id = message.from_user.id

        # Находим пользователя, который создал ссылку
        for user in User.objects.all():
            hash_object = hashlib.md5(str(user.telegram_id).encode())
            if hash_object.hexdigest()[:8] == ref_code:
                if user.telegram_id != new_user_id:
                    # Увеличиваем баланс пользователя-реферера на 1
                    user.balance += 5  # изменть это значение для корректировки стоимости реферальной ссылки
                    user.save_balance(comment="Реферальная система", type="debit")
                    user.save()

                    bot.send_message(user.telegram_id,
                                     "Кто-то перешел по вашей реферальной ссылке! Вам начислено 5 рублей! 😊")
                    break
    except Exception as e:
        logger.error(f'Ошибка при обработке реферальной ссылки: {e}')


def get_ref_link(callback: CallbackQuery) -> None:
    """Отправляет пользователю его реферальную ссылку."""
    try:
        backMarkup = InlineKeyboardMarkup()
        backMarkup.add(InlineKeyboardButton(text="Назад в меню 🔙", callback_data="back"))
        user_id = callback.from_user.id
        ref_link = generate_ref_link(user_id)

        bot.edit_message_text(chat_id=user_id,
                              message_id=callback.message.id,
                              text=f"Ваша реферальная ссылка:\n{ref_link}\n\nПоделитесь ею с друзьями и получите +5 рублей за каждого нового пользователя!",
                              reply_markup=backMarkup
                              )
    except Exception as e:
        logger.error(f'Ошибка при генерации реферальной ссылки: {e}')
