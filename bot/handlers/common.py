from bot import bot, logger, AI_ASSISTANT
from django.conf import settings
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from bot.keyboards import UNIVERSAL_BUTTONS, back
from bot.models import User, Mode, Transaction
from .user.registration import start_registration
from bot.texts import CHOICE_TEXT, BUY_TEXT, FAQ, MENU_TEXT, LC_TEXT, BALANCE_TEXT, WE_ARE_WORKING


def start(message: Message) -> None:
    """Обработчик команды /start."""
    start_registration(message)
    

'''def menu(message: Message):
    menu_markup = InlineKeyboardMarkup()
    for element in menu_list:
        button = InlineKeyboardButton(
            text=element[0],
            callback_data=element[1]
        )
        menu_markup.add(button)
    bot.send_message(
        chat_id=message.chat.id,
        text=MENU_TEXT,
        reply_markup=menu_markup,
    )
'''


def help_(message: Message) -> None:
    """Обработчик команды /help."""
    bot.send_message(chat_id=message.chat.id, text=FAQ, parse_mode='Markdown')


def choice(call: CallbackQuery) -> None:
    """Обработчик команды /mode."""
    user_id = call.from_user.id

    try:
        modes = Mode.objects.all()
        user = User.objects.get(telegram_id=user_id)

        choice_markup = InlineKeyboardMarkup()
        for mode in modes:
            button = InlineKeyboardButton(
                text=f'{mode.name} {"✅" if user.current_mode == mode else ""}',
                callback_data=f'choice_{mode.pk}'
            )
            choice_markup.add(button)
        # button3 = InlineKeyboardButton(text='получить рефссылку', callback_data='generate_ref_link')
        # choice_markup.add(button3)
        choice_markup.add(back)
        bot.edit_message_text(chat_id=user_id, message_id=call.message.id, text=CHOICE_TEXT, reply_markup=choice_markup)
        logger.info(f'{user_id}, attempt /choice')
    except User.DoesNotExist:
        logger.warning(f'Пользователь с ID {user_id} не найден.')
        bot.send_message(chat_id=user_id, text="Пользователь не найден.")
    except Exception as e:
        logger.error(f'Ошибка при обработке команды /choice: {e}')


def buy(call: CallbackQuery) -> None:
    """Обработчик команды /hub."""
    choose_model_menu = InlineKeyboardMarkup()
    modes = Mode.objects.all()

    if not modes.exists():
        bot.edit_message_text(call.message.chat.id, message_id=call.message.id, text="Нет доступных моделей.")
        return

    for mode in modes:
        btn = InlineKeyboardButton(
            text=f'Название: {mode.name}\nМодель ИИ: {mode.model}',
            callback_data=f'model_{mode.pk}'
        )
        choose_model_menu.add(btn)
    choose_model_menu.add(back)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=BUY_TEXT,
                          reply_markup=choose_model_menu)


def balance(message: Message):
    user = User.objects.get(telegram_id=message.from_user.id)
    history = Transaction.objects.filter(user=user).order_by('-adding_time')[:30]
    text_of_transactions = f"Ваш баланс равен _{round(user.balance, 2)}_ руб. \n"+BALANCE_TEXT

    for transaction in history:
        time = transaction.adding_time.strftime('%Y-%m-%d %H:%M:%S')
        if transaction.is_addition is True:
            text_of_transactions += f"_{time}_ *+{round(transaction.cash, 2)}* {transaction.comment}\n\n"
        else:
            text_of_transactions += f"_{time}_ *-{round(transaction.cash, 2)}* {transaction.mode}\n\n"

    bot.send_message(
        chat_id=message.chat.id,
        text=f"{text_of_transactions}",
        parse_mode='Markdown',
    )


def choice_handler(callback: CallbackQuery) -> None:
    """Обработчик callback /choice."""
    _, pk = callback.data.split("_")
    user_id = callback.from_user.id

    try:
        modes = Mode.objects.all()
        user = User.objects.get(telegram_id=user_id)
        mode = Mode.objects.get(pk=pk)

        user.current_mode = mode
        user.save()

        choice_markup = InlineKeyboardMarkup()
        for m in modes:
            button = InlineKeyboardButton(
                text=f'{m.name} {"✅" if user.current_mode == m else ""}',
                callback_data=f'choice_{m.pk}'
            )
            choice_markup.add(button)
        choice_markup.add(back)
        bot.edit_message_text(
            text=CHOICE_TEXT,
            chat_id=user_id,
            message_id=callback.message.message_id,
            reply_markup=choice_markup
        )
    except Exception as e:
        logger.error(f'Ошибка при обработке callback /choice: {e}')


def clear_chat_history(message: Message) -> None:
    chat_id = message.chat.id
    try:
        AI_ASSISTANT.clear_chat_history(chat_id)
        bot.send_message(chat_id, 'Очистил контекст 🧽')
    except:
        bot.send_message(chat_id, 'Контекст чист ✨')


def back_handler(call: CallbackQuery):
    user = User.objects.get(telegram_id=call.from_user.id)
    balance = round(user.balance, 2)
    text = f"{LC_TEXT}\nВаш текущий баланс 🧮: {balance} руб.\n\nВаша текущая модель ИИ 🤖: {user.current_mode}"

    menu_markup = InlineKeyboardMarkup()
    for element in settings.MENU_LIST:
        button = InlineKeyboardButton(
            text=element[0],
            callback_data=element[1]
        )
        menu_markup.add(button)

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.id,
        text=f"{MENU_TEXT}\n{text}",
        reply_markup=menu_markup,
    )
