import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'imagekit',
    "catalog.apps.CatalogConfig",
    'admin_reorder',
]

ADMIN_REORDER = (
    # First group
    {'app': 'catalog', 'label': 'Товары',
     'models': ('catalog.Product',
                'catalog.ProductModification',
                'catalog.Category',
                'catalog.Color',
                'catalog.Size',
                'catalog.Image',
                'catalog.Inventory',
                'catalog.WriteOff')
     },

    # Second group: same app, but different label
    {'app': 'catalog', 'label': 'Продажи и возвраты',
     'models': ('catalog.Sale',
                'catalog.Return',)
     },

    {'app': 'auth', 'models': ('auth.User', 'auth.Group', 'catalog.TelegramUser')}

    ,)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'admin_reorder.middleware.ModelAdminReorder',
]

ROOT_URLCONF = 'deva7km.urls'

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

WSGI_APPLICATION = 'deva7km.wsgi.application'

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

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Kiev'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки для imagekit
IMAGEKIT_SPEC_CACHEFILE_NAMER = 'imagekit.cachefiles.namers.source_name_dot_hash'
IMAGEKIT_CACHEFILE_DIR = 'CACHE/'  # Папка для хранения кешированных изображений

# Настройки для imagekit: применение процессоров и формата для thumbnail
IMAGEKIT_DEFAULT_CACHEFILE_STRATEGY = 'imagekit.cachefiles.strategies.Optimistic'
IMAGEKIT_DEFAULT_CACHEFILE_BACKEND = 'imagekit.cachefiles.backends.Simple'
IMAGEKIT_DEFAULT_CACHEFILE_TIMEOUT = 60 * 60 * 24 * 7  # Неделя


# логирование
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)

# bot logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
            'datefmt': '\033[94m[%d.%m.%Y | %H:%M:%S]\033[0m',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'django_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'encoding': 'utf-8',
            'filename': os.path.join(LOGGING_DIR, 'django.log'),
            'formatter': 'verbose',
        },
        'aiogram_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'encoding': 'utf-8',
            'filename': os.path.join(LOGGING_DIR, 'aiogram.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'django_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'aiogram': {
            'handlers': ['console', 'aiogram_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}


try:
    from .local_settings import *
except ImportError:
    from .prod_settings import *
