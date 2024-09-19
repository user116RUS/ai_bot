import os

import telebot

import dotenv
import openai


dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.base_url = "https://api.vsegpt.ru/v1/"


ERROR = 'Ошибка'