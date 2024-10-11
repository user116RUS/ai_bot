from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from bot.models import Mode, UserMode, User
from bot import bot, logger
from bot.texts import HELP_TEXT, GREETING_TEXT, MODEL_TEXT


def hub_handler(call: CallbackQuery) -> None:
    _, pk = call.data.split("_")
    user_id = call.from_user.id
    message_id = call.message.message_id

    mode = Mode.objects.filter(pk=pk)

    keyboard = InlineKeyboardMarkup()
    text = f"Название плана: {mode.name}\nНазвание модели ИИ: {mode.model}"
    button = InlineKeyboardButton(
        text=f"Купить план:\n{mode.price} руб",
        callback_data=f"pay_{mode.pk}"
    )
    keyboard.add(button)

    bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=message_id,
        reply_markup=button,
    )