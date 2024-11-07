from bot import bot, logger, AI_ASSISTANT
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from bot.keyboards import back_hub
from bot.models import User, Mode, UserMode
from .user.registration import start_registration
from bot.texts import CHOICE_TEXT, BUY_TEXT, FAQ


def start(message: Message) -> None:
    """Обработчик команды /start."""
    start_registration(message)


def help_(message: Message) -> None:
    """Обработчик команды /help."""
    bot.send_message(message.chat.id, FAQ)


def choice(message: Message) -> None:
    """Обработчик команды /choice."""
    user_id = message.from_user.id

    try:
        user = User.objects.get(telegram_id=user_id)
        user_modes = UserMode.objects.filter(user=user)

        if not user_modes.exists():
            bot.send_message(chat_id=user_id, text="У вас нет доступных режимов.")
            return

        choice_markup = InlineKeyboardMarkup()
        for user_mode in user_modes:
            button = InlineKeyboardButton(
                text=f'{user_mode.mode.name}\nостаток: {user_mode.requests_amount} {"✅" if user_mode.is_actual else ""}',
                callback_data=f'choice_{user_mode.pk}'
            )
            choice_markup.add(button)
        button3 = InlineKeyboardButton(text='получить рефссылку', callback_data='generate_ref_link')
        choice_markup.add(button3)
        bot.send_message(chat_id=user_id, text=CHOICE_TEXT, reply_markup=choice_markup)
        logger.info(f'{user_id}, attempt /choice')
    except User.DoesNotExist:
        logger.warning(f'Пользователь с ID {user_id} не найден.')
        bot.send_message(chat_id=user_id, text="Пользователь не найден.")
    except Exception as e:
        logger.error(f'Ошибка при обработке команды /choice: {e}')


def hub(message: Message) -> None:
    """Обработчик команды /hub."""
    choose_model_menu = InlineKeyboardMarkup()
    modes = Mode.objects.all()

    if not modes.exists():
        bot.send_message(message.chat.id, text="Нет доступных моделей.")
        return

    for mode in modes:
        btn = InlineKeyboardButton(
            text=f'Название: {mode.name}\nМодель ИИ: {mode.model}',
            callback_data=f'model_{mode.pk}'
        )
        choose_model_menu.add(btn)

    bot.send_message(message.chat.id, text=BUY_TEXT, reply_markup=choose_model_menu)


def choice_handler(callback: CallbackQuery) -> None:
    """Обработчик callback /choice."""
    _, pk = callback.data.split("_")
    user_id = callback.from_user.id

    try:
        user_modes = UserMode.objects.filter(user__telegram_id=int(user_id))

        if not user_modes.exists():
            logger.warning(f'Пользователь с ID {user_id} не имеет режимов.')
            return

        for user_mode in user_modes:
            user_mode.is_actual = (user_mode.pk == int(pk))
            user_mode.save()

        choice_markup = InlineKeyboardMarkup()
        for user_mode in user_modes:
            button = InlineKeyboardButton(
                text=f'{user_mode.mode.name}\nостаток: {user_mode.requests_amount} {"✅" if user_mode.is_actual else ""}',
                callback_data=f'choice_{user_mode.pk}'
            )
            choice_markup.add(button)

        bot.edit_message_text(
            text=CHOICE_TEXT,
            chat_id=user_id,
            message_id=callback.message.message_id,
            reply_markup=choice_markup
        )
    except Exception as e:
        logger.error(f'Ошибка при обработке callback /choice: {e}')


def back_hub_handler(call: CallbackQuery):
    CHOOSE_MODEL_MENU = InlineKeyboardMarkup()
    modes = Mode.objects.all()
    for mode in modes:
        btn = InlineKeyboardButton(text=f'Название: {mode.name}\nМодель ИИ: {mode.model}',
                                   callback_data=f'model_{mode.pk}'
                                   )
        CHOOSE_MODEL_MENU.add(btn)
    bot.edit_message_text(
        text=BUY_TEXT,
        chat_id=call.from_user.id,
        message_id=call.message.message_id,
        reply_markup=CHOOSE_MODEL_MENU,

    )


def clear_chat_history(message: Message) -> None:
    chat_id = message.chat.id

    AI_ASSISTANT.clear_chat_history(chat_id)
    bot.send_message(chat_id, 'Очистил контекст 🧽')
