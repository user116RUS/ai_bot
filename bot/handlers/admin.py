from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

from bot import bot
from django.conf import settings
from bot.models import User
from bot.states import GetPaymentStates


def share_with_admin(message: Message):
    user_id = message.from_user.id

    bot.forward_message(settings.OWNER_ID, user_id, message.id)
    kb = InlineKeyboardMarkup()
    btn_accept = InlineKeyboardButton(text='Одобрить ✅', callback_data=f'accept_{user_id}')
    btn_reject = InlineKeyboardButton(text='Отказать ❌', callback_data=f'reject{user_id}')

    kb.add(btn_accept).add(btn_reject)

    bot.send_message(text=f'Новая оплата!', chat_id=settings.OWNER_ID, reply_markup=kb)


def get_sum(callback: CallbackQuery):
    user_id = callback.from_user.id

    _, customer_id = callback.data.split('_')

    bot.set_state(user_id, GetPaymentStates.init)
    bot.reset_data(user_id)

    with bot.retrieve_data(user_id) as data:
        data['customer_id'] = customer_id

    msg = bot.send_message(chat_id=settings.OWNER_ID, text=f'Напишите сумму, которою начислим {customer_id}')

    bot.register_next_step_handler(msg, accept_payment)


def accept_payment(message: Message):
    user_id = message.from_user.id  # Use message.from_user.id instead of message.id

    with bot.retrieve_data(user_id) as d:
        if 'customer_id' not in d:
            bot.send_message(message.chat.id, "Ошибка: customer_id не найден. Пожалуйста, попробуйте снова.")
            return
        customer_id = d['customer_id']

    try:
        customer = User.objects.get(telegram_id=customer_id)

        amount = int(message.text)

        customer.balance += amount
        customer.save()
        bot.reset_data(user_id)
        bot.send_message(message.chat.id, 'Сумма успешно начислена.')
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
    except User.DoesNotExist:
        bot.send_message(message.chat.id, "Пользователь не найден.")
