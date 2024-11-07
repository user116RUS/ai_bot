from bot import bot, logger
from telebot.types import Message
from bot.models import User, UserMode
import hashlib


def generate_ref_link(user_id: int) -> str:
    """Генерирует реферальную ссылку для пользователя."""
    # Хэшируем user_id с использованием hashlib
    ref_code = hashlib.sha256(str(user_id).encode()).hexdigest()
    # Проверяем, что ссылка корректно формируется
    return ref_code

def handle_ref_link(message: Message) -> None:
    """Обработчик реферальных ссылок."""
    try:
        # Получаем реферальный код из сообщения
        if not message.text.startswith('/start ref_'):
            return
            
        ref_code = message.text.split('/start ref_')[1]
        new_user_id = message.from_user.id
        
        # Находим пользователя, который создал ссылку
        try:
            # Получаем хэш из ref_code
            referrer_hash = ref_code
            # Ищем пользователя по хэшу
            for user in User.objects.all():
                if generate_ref_link(user.telegram_id) == referrer_hash:
                    referrer = user
                    break
            else:
                logger.error(f'Не найден пользователь с хэшем {referrer_hash}')
                return

            # Проверяем, что новый пользователь еще не зарегистрирован
            if not User.objects.filter(telegram_id=new_user_id).exists():
                # Добавляем +1 запрос к активному режиму пользователя
                user_mode = UserMode.objects.filter(user=referrer, is_actual=True).first()
                if user_mode:
                    user_mode.requests_amount += 1
                    user_mode.save()
                    bot.send_message(referrer.telegram_id, "Ваш друг перешел по реферальной ссылке! Вам начислен +1 запрос.", disable_web_page_preview=True)
                    logger.info(f'Пользователь {referrer.telegram_id} получил бонус за реферала {new_user_id}')
        except User.DoesNotExist:
            logger.error(f'Пользователь не найден')
    except Exception as e:
        logger.error(f'Ошибка при обработке реферальной ссылки: {e}')

def get_ref_link(message: Message) -> None:
    """Отправляет пользователю его реферальную ссылку."""
    try:
        user_id = message.chat.id
        ref_link = f'https://t.me/Sto_print_bot?start=ref_{generate_ref_link(user_id)}'
        bot.send_message(user_id, ref_link, parse_mode='HTML')
    except Exception as e:
        logger.error(f'Ошибка при генерации реферальной ссылки: {e}')
