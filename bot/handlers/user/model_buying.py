from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from bot.keyboards import back, UNIVERSAL_BUTTONS
from bot import bot, texts
from bot.models import Mode
from bot.handlers.common import start
from bot.handlers.admin import share_with_admin


def purchase_handler(call: CallbackQuery) -> None:
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
    keyboard.add(button).add(back)
    bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=message_id,
        reply_markup=keyboard,
    )


def top_up_balance(call: CallbackQuery) -> None:
    user_id = call.from_user.id

    msg = bot.edit_message_text(text=texts.PAY_INFO,
                                chat_id=user_id,
                                reply_markup=UNIVERSAL_BUTTONS,
                                message_id=call.message.id,)
    bot.register_next_step_handler(call.message, confirmation_to_send_admin)


def confirmation_to_send_admin(message: Message) -> None:
    user_id = message.from_user.id
    keyboard = InlineKeyboardMarkup(row_width=2)
    yes_btn = InlineKeyboardButton(text="Да", callback_data=f"confirm_y_{message.id}")
    no_btn = InlineKeyboardButton(text="Нет", callback_data=f"confirm_n_{message.id}")
    keyboard.add(yes_btn, no_btn)
    msg = bot.send_message(
        chat_id=user_id,
        reply_markup=keyboard,
        text="Вы уверенны что вы отправили чек и мы можем его проверить",
    )


def is_sending_to_admin(call: CallbackQuery) -> None:
    _, bool_, msg_id = call.data.split("_")
    if bool_ == "y":
        share_with_admin(user_id=call.from_user.id, msg_id=msg_id)
    else:
        start(call.message)

