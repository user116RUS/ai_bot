from bot import bot, logger
from telebot.types import (
    Message,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
)

from bot.models import User, Mode, UserMode
from .user.registration import start_registration
from bot.texts import HELP_TEXT, GREETING_TEXT, MODEL_TEXT, CHOICE_TEXT, BUY_TEXT, FAQ


def start(message: Message) -> None:
    """Обработчик команды /start  """
    start_registration(message)


def help_(message: Message) -> None:
    """Handler command /help."""
    bot.send_message(message.chat.id, FAQ)


def choice(message: Message) -> None:
    """Обработчик команды /choice  """
    user_id = message.from_user.id

    try:
        user = User.objects.get(telegram_id=user_id)
        user_modes = UserMode.objects.filter(user=user)
        choice = InlineKeyboardMarkup()
        for user_mode in user_modes:
            button = InlineKeyboardButton(
                text=f'{user_mode.mode.name}\nостаток: {user_mode.requests_amount} {"✅" if user_mode.is_actual else ""}',
                callback_data=f'choice_{user_mode.pk}'
            )
            choice.add(button)
        text = CHOICE_TEXT
        bot.send_message(chat_id=user_id, text=text, reply_markup=choice)
        logger.info(f'{user_id}, attempt /choice')
        return
    except Exception as e:
        logger.info(e)

    logger.info(f"User {message.chat.id}: sent /choice command")


def hub(message: Message) -> None:
    CHOOSE_MODEL_MENU = InlineKeyboardMarkup()
    modes = Mode.objects.all()
    for mode in modes:
        btn = InlineKeyboardButton(text=f'Название: {mode.name}\nМодель ИИ: {mode.model}',
                                   callback_data=f'model_{mode.pk}'
                                   )
        CHOOSE_MODEL_MENU.add(btn)
    bot.send_message(message.chat.id,
                     text=BUY_TEXT,
                     reply_markup=CHOOSE_MODEL_MENU
                     )


def choice_handler(callback: CallbackQuery) -> None:
    """Обработчик callback /choice """
    _, pk = callback.data.split("_")
    user_id = callback.from_user.id
    try:
        user_modes = UserMode.objects.filter(user__telegram_id=int(user_id))

        for user_mode in user_modes:
            if user_mode.pk == int(pk):
                user_mode.is_actual = True
            else:
                user_mode.is_actual = False
            user_mode.save()

        choice = InlineKeyboardMarkup()
        for user_mode in user_modes:
            button = InlineKeyboardButton(
                text=f'{user_mode.mode.name}\nостаток: {user_mode.requests_amount} {"✅" if user_mode.is_actual else ""}',
                callback_data=f'choice_{user_mode.pk}'
            )
            choice.add(button)
        text = CHOICE_TEXT
        bot.edit_message_text(
            text=text,
            chat_id=user_id,
            message_id=callback.message.message_id,
            reply_markup=choice
        )
    except Exception as e:
        logger.error(e)
