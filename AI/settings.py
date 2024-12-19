import os

import dotenv
from os import getenv

from django.utils import timezone
from pathlib import Path
from telebot.types import BotCommand

import sentry_sdk

dotenv.load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-c=xzqr!7cf*q$o%kzmv07e&!qs#1uo2_#a#c=pz@7m*m)xjis4'

ASSISTANT_PROMPT = (
    "Ты ассистент помощник в телеграмм боте разаботанный учениками J-GET. Будь вежлив. При форматирование текста:"
    "используй только *жирный*, _курсив_, три обратных апострофа для програмного code"
)
ANALYTIC_PROMPT = ()
PROVIDER_NAME = "vsegpt"
PROVIDER = "https://api.vsegpt.ru/v1"

DEBUG = True

ALLOWED_HOSTS = ['*']

BOT_TOKEN = getenv("BOT_TOKEN")
HOOK = "https://4b29-178-176-167-71.ngrok-free.app"
OWNER_ID = getenv("OWNER_ID")
WHISPER_MODEL = getenv("WHISPER_MODEL")
GETIMG_AI_KEY = getenv("GETIMG_AI_KEY")
CURRENT_MODEL = "https://api.getimg.ai/v1/stable-diffusion/text-to-image"
URL_FUSION = "https://api-key.fusionbrain.ai/"
FUSION_API_KEY = getenv("FUSION_API_KEY")
FUSION_SECRET_KEY = getenv("FUSION_SECRET_KEY")
GROUP_ID = getenv("GROUP_ID")

REQUESTS_AMOUNT_BASE = 10

MENU_LIST = [
    ["Моя подписка", "plan"],
    ["Выбор модели ИИ 🤖", "choice"],
    ["Сгененировать изображение 🖼️", "image_gen"],
    ["Оплатить 💸", "payment"],
    ["Реферальная ссылка 🔗", "referal"],

]

BOT_COMMANDS = [
    BotCommand("start", "Меню 📋 / 🔄"),
    BotCommand("balance", "История транзакций 👀"),
    BotCommand("help", "Помощь 🆘"),
    BotCommand("clear", "Очистить контекст 🧹"),
]

# Application definition

INSTALLED_APPS = [
    'bot',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'AI.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'AI.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

LOCAL = True

if LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": getenv("NAME_DB"),
            "USER": getenv("NAME_DB"),
            "PASSWORD": getenv("PASS_DB"),
            "HOST": "127.0.0.1",
        }
    }

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

sentry_sdk.init(
    dsn="https://fd7c884760eb4c081a655d11386f0606@o4505828290723840.ingest.us.sentry.io/4508366280065024",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    _experiments={
        # Set continuous_profiling_auto_start to True
        # to automatically start the profiler on when
        # possible.
        "continuous_profiling_auto_start": True,
    },
)

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

tz = timezone.get_default_timezone()
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DAYLY_AMOUNT = 10
CRONJOBS = [
    ('19 18 * * *', 'bot.cron.dayly_update'),  # Каждый день в 3:00
    #('*/10 * * * *', 'bot.cron.send_hourly_reminders'),  # Каждые 10 минут
    ('19 18 * * *', 'bot.cron.check_cron'),  # Cheking
]