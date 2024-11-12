from bot import bot, logger
from telebot.types import Message
from bot.models import User
import hashlib


def generate_ref_link(user_id: int) -> str:
    """Генерирует реферальную ссылку для пользователя."""
    # Создаем уникальный хеш на основе user_id
    hash_object = hashlib.md5(str(user_id).encode())
    ref_code = hash_object.hexdigest()[:8]
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
                # Проверяем, что новый пользователь еще не зарегистрирован
                if not User.objects.filter(telegram_id=new_user_id).exists():
                    # Добавляем +1 запрос к активному режиму пользователя
                    user_modes = User.objects.filter(user=user, is_actual=True)
                    if user_modes.exists():
                        user_mode = user_modes.first()
                        user_mode.balance += 1
                        user_mode.save()
                        bot.send_message(user.telegram_id, "Ваш друг перешел по реферальной ссылке! Вам начислен +1 запрос.")
                        logger.info(f'Пользователь {user.telegram_id} получил бонус за реферала {new_user_id}')
                break
    except Exception as e:
        logger.error(f'Ошибка при обработке реферальной ссылки: {e}')

@bot.message_handler(commands=['ref'])
def get_ref_link(message: Message) -> None:
    """Отправляет пользователю его реферальную ссылку."""
    try:
        user_id = message.from_user.id
        ref_link = generate_ref_link(user_id)
        bot.send_message(
            user_id,
            f"Ваша реферальная ссылка:\n{ref_link}\n\nПоделитесь ею с друзьями и получите +1бубль за каждого нового пользователя!"
        )
    except Exception as e:
        logger.error(f'Ошибка при генерации реферальной ссылки: {e}')
