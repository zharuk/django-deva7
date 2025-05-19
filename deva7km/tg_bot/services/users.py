from functools import wraps
from django.db import connection
import random
import string

from aiogram import types
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

from catalog.models import TelegramUser

@sync_to_async
def _safe_fetch_telegram_user(telegram_id):
    # Безопасно переподключаемся к базе, если нужно
    connection.close_if_unusable_or_obsolete()

    return TelegramUser.objects.filter(telegram_id=telegram_id).first()

@sync_to_async
def _safe_create_telegram_user(telegram_id, user_name, first_name, last_name):
    connection.close_if_unusable_or_obsolete()

    user = TelegramUser.objects.create(
        telegram_id=telegram_id,
        user_name=user_name,
        first_name=first_name,
        last_name=last_name,
        role='unauthorized'
    )
    return user

@sync_to_async
def _safe_get_or_create_django_user(username, first_name, last_name, password):
    connection.close_if_unusable_or_obsolete()

    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': first_name,
            'last_name': last_name,
            'password': password,
        }
    )
    return user, created

@sync_to_async
def _safe_save_user(user):
    connection.close_if_unusable_or_obsolete()
    user.save()


# Асинхронная оболочка
async def get_or_create_telegram_user(telegram_id, user_name, first_name=None, last_name=None, password=None):
    first_name = first_name or ''
    last_name = last_name or ''

    user = await _safe_fetch_telegram_user(telegram_id)

    if user is None:
        user = await _safe_create_telegram_user(telegram_id, user_name, first_name, last_name)

        username = user.user_name or f"{user.first_name}_{user.telegram_id}"

        if password is None:
            password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        django_user, created = await _safe_get_or_create_django_user(username, first_name, last_name, password)

        if created:
            django_user.set_password(password)
            await _safe_save_user(django_user)

        user.user = django_user
        await _safe_save_user(user)

    return user


def admin_or_seller_required(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        # Получаем Telegram ID пользователя
        telegram_id = message.from_user.id

        # Получаем или создаем пользователя Telegram
        user = await get_or_create_telegram_user(
            telegram_id=telegram_id,
            user_name=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name
        )

        # Проверяем роль пользователя
        if user and (user.role == 'admin' or user.role == 'seller'):
            # Если пользователь администратор или продавец, вызываем функцию
            return await func(message, *args, **kwargs)
        else:
            # Если не администратор и не продавец, возвращаем ошибку
            return await message.answer("У вас нет прав для выполнения этой команды.")

    return wrapper
