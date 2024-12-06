from telebot.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from bot.keyboards import back, UNIVERSAL_BUTTONS
from bot import bot, texts, keyboards
from bot.models import Mode
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
    _, type_buy = call.data.split('_')

    if type_buy == 'balance':
        text = texts.PAY_INFO
    else:
        text = (
            'Поcле покупки *подписки* вы разблокируете возможность отправлять голосовые сообщения,'
            ' документы(doc, pdf), генерации картинок. Все обновления вы сможете испытать первыми!\n'
            'Лимиты на каждый день:\n\n'
            '\n1. 30 базовых запросов'
            '\n2. 20 средних запросов'
            '\n3. 10 умных запросов\n\n' + texts.PAY_INFO_PLAN
        )

    msg = bot.edit_message_text(
        text=text,
        chat_id=user_id,
        reply_markup=UNIVERSAL_BUTTONS,
        message_id=call.message.id,
    )

    bot.register_next_step_handler(msg, share_with_admin)


def choice_pay(callback: CallbackQuery) -> None:
    user_id = callback.from_user.id

    markup = InlineKeyboardMarkup()
    plan_buy_btn = InlineKeyboardButton(text='Купить подписку 🔥', callback_data='buy_plan')
    top_up_btn = InlineKeyboardButton(text='Пополнить баланс 💸', callback_data='buy_balance')
    markup.add(plan_buy_btn).add(top_up_btn).add(keyboards.back)

    bot.edit_message_text(
        message_id=callback.message.message_id,
        chat_id=user_id,
        text='Напомню, что мы поддерживаем 2 вида тарификации:\n\n'
             '*1. Подписка.*\n'
             'Покупая подписку вы получаете доступ ко всем моделям, возможность отправлять голосовые сообщения,'
             ' документы(doc, pdf), генерации картинок\n'
             '\n\n*2. Прямая оплата запросов (Студенческая)*'
             '\nВы пополняете баланс из которого вычитается стоимость запросов  в зависимости от'
             ' сложности модели(чем "умнее" модель тем дороже запрос)',
        parse_mode='Markdown',
        reply_markup=markup,
    )
