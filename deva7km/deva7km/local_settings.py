import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ws!zd57h#w7%dg*o_7a7*!)u98mn8v6k5xghig$ax!mkp4=$&('

# BOT TOKEN
BOT_TOKEN = "5851946500:AAGi4zKsLc9WMoUXq8lizX2glxQ00fLtlws"

DEBUG = True

ALLOWED_HOSTS = []

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = 'static/'