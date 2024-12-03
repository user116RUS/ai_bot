import os

import dotenv

from os import getenv

from pathlib import Path
from telebot.types import BotCommand

import sentry_sdk

dotenv.load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-c=xzqr!7cf*q$o%kzmv07e&!qs#1uo2_#a#c=pz@7m*m)xjis4'

ASSISTANT_PROMPT = (
    "Ты ассистент помощник в телеграмм боте разаботанный учениками J-GET. Будь вежлив. Форматирование текста Markdown()"
    "*жирный*, _курсив_, и тд."
)
ANALYTIC_PROMPT = ()

PROVIDER_NAME = "vsegpt"
# PROVIDER_NAME = "openai"
PROVIDER = "https://api.vsegpt.ru/v1"
# PROVIDER = "https://api.openai.com/v1"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

BOT_TOKEN = getenv("BOT_TOKEN")
HOOK = getenv("HOOK")
OWNER_ID = getenv("OWNER_ID")
WHISPER_MODEL = getenv("WHISPER_MODEL")
GROUP_ID = getenv("GROUP_ID")

REQUESTS_AMOUNT_BASE = 10

MENU_LIST = [
    ["Выбор модели ИИ 🤖", "choice"],
    ["Пополнить баланс 💸", "buy"],
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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
