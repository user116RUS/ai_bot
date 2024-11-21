import logging
import telebot

from bot.apis.ai import OpenAIAPI
from bot.apis.voice_recognition import BaseVoiceRecognition
from bot.apis.files_converting import DocumentConverter
from bot.apis.image_gen import ImageGenAPI
from django.conf import settings

AI_ASSISTANT = OpenAIAPI()
WHISPER_RECOGNITION = BaseVoiceRecognition()
CONVERTING_DOCUMENTS = DocumentConverter()
IMAGE_GEN = ImageGenAPI()


commands = settings.BOT_COMMANDS

bot = telebot.TeleBot(
    settings.BOT_TOKEN,
    threaded=False,
)

bot.set_my_commands(commands)

logging.info(f'@{bot.get_me().username} started')

logger = telebot.logger
logger.setLevel(logging.INFO)
