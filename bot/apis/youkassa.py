import dotenv
from telebot.types import (
    CallbackQuery,
    Chat,
    LabeledPrice,
    Message,
    PreCheckoutQuery,
)
from yookassa import Configuration

import os

from bot import bot, keyboards
from bot.models import Mode

dotenv.load_dotenv()

COP_TO_RUB = 100
TOKEN = os.getenv('SHOP_ID')
API = os.getenv('PAYMENT_TOKEN')

Configuration.account_id = TOKEN
Configuration.secret_key = API


def pay_for_mode(call: CallbackQuery) -> None:
    chat_id = call.message.chat.id
    _, mode_pk = call.data.split("_")
    mode_info = Mode.objects.get(pk=mode_pk)
    try:
        command_pay(chat_id, mode_info)
    except Exception as e:
        bot.send_message(chat_id, e)


@bot.pre_checkout_query_handler(func=lambda query: True)
def handle_pre_checkout(pre_checkout_query: PreCheckoutQuery) -> None:
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@bot.message_handler(content_types=['successful_payment'])
def handle_successful_payment(message: Message) -> None:
    chat_id = message.chat.id

    if not message.successful_payment:
        bot.send_message(chat_id, 'Что то пошло не так, пoпробуйте нажать /start')
        return
    bot.send_message(chat_id, f'Спасибо вам за покупку! Мы открыли доступ к ии\n')


def command_pay(chat_id: Chat, mode_info: dict) -> None:
    bot.send_invoice(
        chat_id=chat_id,
        title='Покупка',
        description='После оплаты у вас появится доступ к ии',
        invoice_payload=f'successfulPayment_{mode_info.pk}',
        provider_token=API,
        currency='RUB',
        prices=[LabeledPrice(label=mode_info.name, amount=mode_info.price * COP_TO_RUB), ],
        photo_url=mode_info.photo,
        photo_height=1280,
        photo_width=724,
        photo_size=20000,
        is_flexible=False,
        start_parameter='start_parameter',
        reply_markup=keyboards.PAY_BUTTONS,
    )
