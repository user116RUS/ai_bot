from telebot.handler_backends import State, StatesGroup


class GetPaymentStates(StatesGroup):
    init = State()
    name = State()
