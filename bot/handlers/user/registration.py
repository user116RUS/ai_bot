import hashlib

from bot import bot, logger
from bot.texts import WE_ARE_WORKING, MENU_TEXT, LC_TEXT
from bot.models import User, Mode
from django.conf import settings
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.handlers.referal import handle_ref_link


def start_registration(message):
    """ Функция для регистрации пользователей """
    user_id = message.from_user.id

    modes = Mode.objects.filter(is_base=True)
    if not modes.exists():
        bot.send_message(chat_id=settings.OWNER_ID, text="Добавь режимы, и хоть один базовый!")
        bot.send_message(chat_id=user_id, text=WE_ARE_WORKING)
        return

    user = User.objects.filter(telegram_id=user_id)

    if not user.exists():
        bot.send_message(settings.OWNER_ID, user_id)
        user = User.objects.create(
            telegram_id=user_id,
            balance=5.0,
            name=message.from_user.first_name,
            message_context=None,
            current_mode=modes[0],
        )
        user.save()

    logger.info(f'{user_id} registration successful')

    menu_markup = InlineKeyboardMarkup()
    for element in settings.MENU_LIST:
        button = InlineKeyboardButton(
            text=element[0],
            callback_data=element[1]
        )
        menu_markup.add(button)
    balance = round(user[0].balance, 2)

    text = f"{LC_TEXT}\nВаш текущий баланс 🧮: {balance} руб.\n\nВаша текущая модель ИИ 🤖: {user[0].current_mode}"
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(
        chat_id=message.chat.id,
        text=f"{MENU_TEXT}\n{text}",
        reply_markup=menu_markup,
    )
