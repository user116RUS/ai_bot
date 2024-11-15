from bot import bot, logger
from telebot.types import CallbackQuery, Message
from bot.models import User
import hashlib


def generate_ref_link(user_id: int) -> str:
    """Генерирует реферальную ссылку для пользователя."""
    # Создаем уникальный хеш на основе user_id
    hash_object = hashlib.md5(str(user_id).encode())
    ref_code = hash_object.hexdigest()[:8]
    get_ref_link(message=...)
    return f"https://t.me/Sto_print_bot?start=ref_{ref_code}"


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
                    user.save()
                    bot.send_message(user.telegram_id,
                                     "Кто-то перешел по вашей реферальной ссылке! Вам начислено 5 рублей.")
                    break
    except Exception as e:
        logger.error(f'Ошибка при обработке реферальной ссылки: {e}')


def get_ref_link(callback: CallbackQuery) -> None:
    """Отправляет пользователю его реферальную ссылку."""
    try:
        user_id = callback.from_user.id
        ref_link = generate_ref_link(user_id)
        bot.send_message(
            user_id,
            f"Ваша реферальная ссылка:\n{ref_link}\n\nПоделитесь ею с друзьями и получите +5 рублей за каждого нового пользователя!"
        )
    except Exception as e:
        logger.error(f'Ошибка при генерации реферальной ссылки: {e}')
