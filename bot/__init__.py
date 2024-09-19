import logging

import telebot

from django.conf import settings

bot = telebot.TeleBot(
    settings.BOT_TOKEN,
    parse_mode="Markdown",
    threaded=False
)

logging.info(f'@{bot.get_me().username} started')

logger = telebot.logger
logger.setLevel(logging.INFO)
