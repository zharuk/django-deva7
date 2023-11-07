from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

from catalog.models import Product


async def inline_keyboard_main_sku():
    products = await sync_to_async(list)(Product.objects.all())  # Получаем все товары

    keyboard = InlineKeyboardMarkup(row_width=2)  # Создаем клавиатуру с двумя кнопками в ряду

    for product in products:
        button_text = product.sku  # Используем артикул товара в качестве текста кнопки
        callback_data = f"product_{product.id}"  # Уникальные данные обратного вызова для каждого товара

        # Создаем кнопку с текстом и данными обратного вызова
        button = InlineKeyboardButton(text=button_text, callback_data=callback_data)

        # Добавляем кнопку к клавиатуре
        keyboard.add(button)

    return keyboard

