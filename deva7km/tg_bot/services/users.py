import random
import string
from functools import wraps

from aiogram import types
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User

from catalog.models import TelegramUser

# Функция получения или создания пользователя
async def get_or_create_telegram_user(telegram_id, user_name, first_name=None, last_name=None, password=None):
    # Устанавливаем пустые строки по умолчанию, если данные отсутствуют
    first_name = first_name or ''
    last_name = last_name or ''

    # Пытаемся получить TelegramUser
    user = await sync_to_async(TelegramUser.objects.filter)(telegram_id=telegram_id)
    user = await sync_to_async(user.first)()

    if user is None:
        # Если TelegramUser не найден, создаем новую запись
        user = TelegramUser(
            telegram_id=telegram_id,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            role='unauthorized'  # Установим роль по умолчанию
        )
        await sync_to_async(user.save)()

        # Получаем существующего Django пользователя, связанного с TelegramUser
        django_user_query = await sync_to_async(User.objects.filter)(telegram_user__telegram_id=telegram_id)
        django_user = await sync_to_async(django_user_query.first)()

        if django_user is None:
            # Создаем нового пользователя Django, если он не существует
            username = user.user_name or f"{user.first_name}_{user.telegram_id}"

            if password is None:
                # Генерация случайного пароля, если не предоставлен
                password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            django_user, created = await sync_to_async(User.objects.get_or_create)(
                username=username,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'password': password  # Устанавливаем пароль при создании
                }
            )

            if created:
                # Устанавливаем пароль после создания пользователя
                django_user.set_password(password)
                await sync_to_async(django_user.save)()

            # Связываем стандартного пользователя с TelegramUser
            user.user = django_user
            await sync_to_async(user.save)()
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
