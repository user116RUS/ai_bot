import logging
import os

import telebot
from django.conf import settings

import dotenv
import openai

logger = telebot.logger
logger.setLevel(logging.INFO)

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = "https://api.vsegpt.ru/v1/"

giga = GigaChat(credentials=os.getenv("GIGACHAT_API_KEY"), verify_ssl_certs=False, model="GigaChat-Pro")

ERROR = 'Ошибка'