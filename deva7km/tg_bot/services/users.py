from functools import wraps
from aiogram import types
from asgiref.sync import sync_to_async
from catalog.models import TelegramUser


#  Функция получения или создания пользователя
@sync_to_async
def get_or_create_telegram_user(user_id, username, first_name, last_name=None):
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        # Если пользователь найден, можешь обновить его данные, если необходимо
        user.username = username
        user.first_name = first_name
        if last_name:
            user.last_name = last_name
        user.save()
    except TelegramUser.DoesNotExist:
        # Если пользователь не найден, создадим новую запись
        user = TelegramUser(
            user_id=user_id,
            username=username,
            first_name=first_name,
            last_name=last_name,
            role='unauthorized'  # Установим роль по умолчанию
        )
        user.save()
    return user


# Функция проверки доступа к разделу
@sync_to_async
def access_control(user_id):
    try:
        user = TelegramUser.objects.get(user_id=user_id)
        if user.role in ['admin', 'seller']:
            return True  # Пользователь с ролью админа или продавца имеет доступ
        else:
            return False  # Пользователь с другой ролью не имеет доступ
    except TelegramUser.DoesNotExist:
        return False  # Пользователь не найден, считаем его неавторизованным


# Декоратор для проверки доступа к разделу
def access_control_decorator(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        user_id = message.from_user.id
        if await access_control(user_id):
            return await func(message, *args, **kwargs)
        else:
            await message.answer("Доступ запрещен.")
    return wrapper
