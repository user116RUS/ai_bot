from functools import wraps

from datetime import datetime

from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from bot import bot, logger
from django.conf import settings
from bot.models import User, Transaction
from bot.states import GetPaymentStates
from bot.texts import ADMIN_PANEL_TEXT


def admin_permission(func):
    """
    Checking user for admin permission to access the function.
    """

    @wraps(func)
    def wrapped(message: Message) -> None:
        user_id = message.from_user.id
        user = User.objects.get(telegram_id=user_id)
        if not user.is_admin:
            bot.send_message(user_id, '⛔ У вас нет администраторского доступа')
            logger.warning(f'Попытка доступа к админ панели от {user_id}')
            return
        return func(message)

    return wrapped


def share_with_admin(msg_id: str, user_id: str):
    bot.forward_message(settings.OWNER_ID, user_id, msg_id)

    kb = InlineKeyboardMarkup()
    btn_accept = InlineKeyboardButton(text='Одобрить ✅', callback_data=f'accept_{user_id}')
    btn_reject = InlineKeyboardButton(text='Отказать ❌', callback_data=f'reject_{user_id}')

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
        customer.save_balance(comment="Пополнение", type="debit")
        customer.save()

        bot.reset_data(user_id)
        bot.send_message(message.chat.id, 'Сумма успешно начислена.')
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректное число.")
    except User.DoesNotExist:
        bot.send_message(message.chat.id, "Пользователь не найден.")


def reject_payment(callback: CallbackQuery):
    _, customer_id = callback.data.split('_')
    bot.edit_message_text(chat_id=customer_id, message_id=callback.message.id,
                          text='Вам отказано в пополнии счета. \n Узнать причину отказа можно в чате поддежки по ссылке https://t.me/+hNOJ9VWB_1k2ZjI6')
    bot.send_message(chat_id=settings.OWNER_ID,
                     text=f'Пользователю с id {customer_id} отправлено сообщение об отказе в пополнении счета.')


@admin_permission
def admin_panel(message: Message):
    """if not Transaction.objects.filter(is_addition=False).exists():
        bot.send_message(chat_id=message.chat.id, text="К сожалению статистика отсутствует")
        return"""
    now_month = datetime.now().month
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
              "Ноябрь",
              "Декабрь"
              ]

    month_markup = InlineKeyboardMarkup()
    for x in range(0, 11, 3):
        # button = InlineKeyboardButton(text=month, callback_data=f"month_{months.index(month)}")

        month_markup.add(InlineKeyboardButton(text=months[x], callback_data=f"month_{x}"),
                         InlineKeyboardButton(text=months[x + 1], callback_data=f"month_{x + 1}"),
                         InlineKeyboardButton(text=months[x + 2], callback_data=f"month_{x + 2}"))

    """transactions = Transaction.objects.filter(is_addition=False)
    total_sum = float()
    no_margin_price = float()
    for transaction in transactions:
        total_sum += transaction.cash
        no_margin_price += transaction.no_margin_cost
    no_margin_price = round(no_margin_price, 5)
    total_sum = round(total_sum, 5)
    difference = total_sum - no_margin_price
  """
    user = message.from_user.first_name

    bot.send_message(chat_id=message.chat.id,
                     text=f"{ADMIN_PANEL_TEXT}, *{user}*\n\nПожалуйста, выберите месяц для просмотра статистики",
                     parse_mode="Markdown",
                     reply_markup=month_markup
                     )


def month_statistic(call: CallbackQuery):
    _, month_number = call.data.split("_")
    now_month = datetime.now().month
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь",
              "Ноябрь",
              "Декабрь"
              ]
    month_markup = InlineKeyboardMarkup()
    transactions = Transaction.objects.filter(is_addition=False)
    transactions_bonus = Transaction.objects.filter(comment="bonus")
    print(transactions_bonus)

    for x in range(0, 11, 3):
        month_markup.add(InlineKeyboardButton(text=months[x], callback_data=f"month_{x}"),
                         InlineKeyboardButton(text=months[x + 1], callback_data=f"month_{x + 1}"),
                         InlineKeyboardButton(text=months[x + 2], callback_data=f"month_{x + 2}"))

    total_sum = float(0.0)
    wasted_on_bonus = float(0.0)
    no_margin_price = float(0.0)
    difference = float(0.0)

    for transaction in transactions:
        time = str(transaction.adding_time)
        if int(time[5:7]) == int(month_number) + 1:
            for transaction_bonus in transactions_bonus:
                if transaction_bonus is not None:
                    wasted_on_bonus += transaction_bonus.cash
            if transaction is not None:
                total_sum += transaction.cash
                no_margin_price += transaction.no_margin_cost

                no_margin_price = float(round(no_margin_price, 5))
                total_sum = round(total_sum, 5)
                difference = total_sum - no_margin_price - wasted_on_bonus
                user = call.from_user.first_name

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.id,
                          text=f"Вот статистика за __*{months[int(month_number)]}*__:\n\nПотрачено "
                               f"денег на запросы/на бонусы 👨‍🦰: {no_margin_price}/{wasted_on_bonus}\n\nВыручка 💰: {total_sum}\n\nПрибыль 📈: {difference}",
                          parse_mode="Markdown",
                          reply_markup=month_markup
                          )
