import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-ws!zsdfw7%dg*odfffdsssu98msfig$ax!mkp4=$&('

BOT_TOKEN = "5851946500:AAGi4zKsLc9WMoUXq8lizX2glxQ00fLtlws"

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deva7km_db',
        'USER': 'postgres',
        'PASSWORD': '592014fann',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')