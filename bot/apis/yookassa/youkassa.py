from bot import bot
import dotenv
from telebot.types import (
    CallbackQuery,
    LabeledPrice,
    Message,
    PreCheckoutQuery,

)
from yookassa import Configuration

import os

from bot import keyboards
from bot.models import Mode

dotenv.load_dotenv()

COP_TO_RUB = 100
TOKEN = os.getenv('PAYMENT_TOKEN')
API = os.getenv('PAYMENT_TOKEN')

Configuration.account_id = TOKEN
Configuration.secret_key = API


def pay_for_mode(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, mode_pk = call.data.split("_")
    mode = Mode.objects.get(pk=mode_pk)
    try:
        command_pay(chat_id, mode)
    except Exception as e:
        bot.send_message(chat_id, e)


def command_pay(chat_id, mode):
    amount = mode.price * COP_TO_RUB
    bot.send_invoice(
        chat_id=chat_id,
        title='Покупка',
        description='После оплаты у вас появится доступ к ИИ',
        invoice_payload=f'successfulPayment_{mode.pk}',
        provider_token=TOKEN,
        currency='rub',
        prices=[LabeledPrice(label=mode.name, amount=amount)],
        is_flexible=False,
        start_parameter='start_parameter',
        reply_markup=keyboards.PAY_BUTTONS,
    )


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
