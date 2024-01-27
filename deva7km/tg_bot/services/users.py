from functools import wraps
from aiogram import types
from asgiref.sync import sync_to_async
from catalog.models import TelegramUser


# Функция получения или создания пользователя
async def get_or_create_telegram_user(user_id, user_name, first_name, last_name=None):
    try:
        user = await sync_to_async(TelegramUser.objects.get)(user_id=user_id)
        # Если пользователь найден, можешь обновить его данные, если необходимо
        user.username = user_name
        user.first_name = first_name
        if last_name:
            user.last_name = last_name
        await sync_to_async(user.save)()
    except TelegramUser.DoesNotExist:
        # Если пользователь не найден, создадим новую запись
        user = TelegramUser(
            user_id=user_id,
            user_name=user_name,
            first_name=first_name,
            last_name=last_name,
            role='unauthorized'  # Установим роль по умолчанию
        )
        await sync_to_async(user.save)()

    return user


# Декоратор для проверки доступа к разделу
def admin_access_control_decorator(access):
    def decorator(func):
        @wraps(func)
        async def wrapper(message: types.Message, *args, **kwargs):
            # данные о пользователе
            user_id = message.from_user.id
            user_name = message.from_user.username
            first_name = message.from_user.first_name
            last_name = message.from_user.last_name

            try:
                # создаем пользователя или получаем его
                user = await get_or_create_telegram_user(user_id=user_id, user_name=user_name, first_name=first_name,
                                                  last_name=last_name)
            except TelegramUser.DoesNotExist:
                await message.answer("Пользователь не найден. Для начала работы наберите /start")
                return

            if access in ['seller'] and user.role in ['seller', 'admin']:
                return await func(message, *args, **kwargs)

            if access in ['admin'] and user.role in 'admin':
                return await func(message, *args, **kwargs)

            else:
                await message.answer("Доступ запрещен.")

        return wrapper

    return decorator
