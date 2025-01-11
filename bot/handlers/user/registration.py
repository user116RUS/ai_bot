import datetime

from bot import bot, logger
from bot.texts import WE_ARE_WORKING, LC_TEXT
from bot.models import User, Mode, UserMode
from bot.utils import create_user_quotas
from django.conf import settings
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.handlers.referal import handle_ref_link


def start_registration(message, delete=True):
    """ Функция для регистрации пользователей """
    user_id = message.from_user.id

    modes = Mode.objects.filter(is_base=True)
    if not modes.exists():
        bot.send_message(chat_id=settings.OWNER_ID, text="Добавь режимы, и хоть один базовый!")
        bot.send_message(chat_id=user_id, text=WE_ARE_WORKING)
        return

    user = User.objects.filter(telegram_id=user_id)

    if not user.exists():
        user = User.objects.create(
            telegram_id=user_id,
            name=message.from_user.first_name,
            message_context=None,
            balance=0,
            current_mode=modes[0],
            plan_end=datetime.datetime.now() - datetime.timedelta(days=1),
        )
        user.save()
        user.balance += 5
        user.save_balance(comment="Бонус", type="credit")
        user.save()
        handle_ref_link(message)
        create_user_quotas(user)
    else:
        user = User.objects.get(telegram_id=user_id)
        if not user.user_mode.filter().exists():
            create_user_quotas(user)

    menu_markup = InlineKeyboardMarkup()
    if delete:
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    if not user.is_trained:
        start_train_btn = InlineKeyboardButton(text='Начнем 🚀', callback_data=f'train_1')
        menu_markup.add(start_train_btn)
        bot.send_message(
            chat_id=user_id,
            text='Рады вас приветсвовать! Давайте начнем обучение'
                 ' и я вам расскажу, чем я могу быть полезен и как со мной работать 😊',
            reply_markup=menu_markup,
        )
        return

    for element in settings.MENU_LIST:
        button = InlineKeyboardButton(
            text=element[0],
            callback_data=element[1]
        )
        menu_markup.add(button)

    balance = round(user.balance, 2)

    status = 'Активна\n\nДоступные вам на сегодня запросы:' if user.has_plan else 'Не активна'
    plan_text = ""
    if user.has_plan:
        plans = UserMode.objects.filter(user=user)
        for plan in plans:
            plan_text += f"{plan.mode.name}: {plan.quota} запросов\n"

    text = f"{LC_TEXT}\nВаш текущий баланс 🧮: {balance} руб.\n\nВаша подписка: {status}\n{plan_text}\nВаша текущая модель ИИ 🤖: {user.current_mode}"
    bot.send_message(
        chat_id=message.chat.id,
        text=text,
        reply_markup=menu_markup,
    )
