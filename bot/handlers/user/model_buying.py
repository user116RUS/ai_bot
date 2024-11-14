from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from bot.keyboards import back_hub
from bot import bot, texts
from bot.models import Mode
from bot.handlers.admin import share_with_admin


def hub_handler(call: CallbackQuery) -> None:
    _, pk = call.data.split("_")
    user_id = call.from_user.id
    message_id = call.message.message_id

    mode = Mode.objects.get(pk=pk)

    keyboard = InlineKeyboardMarkup()
    text = f"Сколько хотите зачислить на баланс?"
    button = InlineKeyboardButton(
        text=f"49 руб",
        callback_data=f"pay_49"
    )
    keyboard.add(button).add(back_hub)
    bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=message_id,
        reply_markup=keyboard,
    )


def top_up_balance(message: CallbackQuery) -> None:
    user_id = message.from_user.id

    msg = bot.send_message(text=texts.PAY_INFO, chat_id=user_id)

    bot.register_next_step_handler(msg, share_with_admin)
