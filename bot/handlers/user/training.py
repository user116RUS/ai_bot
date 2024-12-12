import os

import requests
from telebot.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from django.conf import settings
from bot import AI_ASSISTANT, CONVERTING_DOCUMENTS, bot, logger
from bot.core import check_registration
from bot.models import User, TrainingMaterial
from bot.keyboards import UNIVERSAL_BUTTONS


NEXT_MATERIAL_STEP: int = 1


def get_material(callback: CallbackQuery):
    user_id = callback.from_user.id
    _, material_pk = callback.data.split('_')

    try:
        material: TrainingMaterial = TrainingMaterial.objects.get(pk=int(material_pk))
    except TrainingMaterial.DoesNotExist:
        bot.edit_message_text(
            message_id=callback.message.message_id,
            chat_id=user_id,
            text='Поздравляю, вы прошли обучение! Вы молодец 🤩',
            reply_markup=UNIVERSAL_BUTTONS
        )
        user = User.objects.get(telegram_id=user_id)
        user.is_trained = True
        user.save()
        return

    markup = InlineKeyboardMarkup()
    btn_agree = InlineKeyboardButton(
        text=material.agree_text,
        callback_data=f'train_{int(material_pk) + NEXT_MATERIAL_STEP}'
    )
    markup.add(btn_agree)

    if material.photo:
        bot.delete_message(chat_id=user_id, message_id=callback.message.message_id)
        bot.send_photo(
            chat_id=user_id,
            photo=open(material.photo.url, 'rb'),
            caption=material.description,
            reply_markup=markup
        )
    else:
        bot.edit_message_text(
            message_id=callback.message.message_id,
            chat_id=user_id,
            text=material.description,
            reply_markup=markup,
        )
