from typing import Union, List
from urllib.parse import urljoin

from aiogram import Bot
from aiogram.types import URLInputFile
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async
from catalog.models import Product, ProductModification
from deva7km.settings import BOT_TOKEN

bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# функция для получения информации о модификациях товара
@sync_to_async
def get_modifications_info(sku):
    try:
        # Находим основной товар по артикулу
        product = Product.objects.get(sku=sku)
    except Product.DoesNotExist:
        return "Товар с данным артикулом не найден."

    # Создаем строку, в которой будем собирать информацию о модификациях
    result = ""

    result += hbold(f"📦 Товар: {product.title}\n")
    result += hbold(f"🧾 Артикул: {product.sku}\n")
    result += hbold(f"💵 Цена: {product.price} ({product.currency})\n\n")
    result += hbold(f"📒 Модификации:\n")

    # Перебираем все модификации этого товара
    for modification in product.modifications.all():
        # Формируем информацию о модификации
        modification_info = (
            f"➡️️ Цвет: {modification.color.name}\n"
            f"➡️️ Размер: {modification.size.name}\n"
            f"➡️️ На складе: {modification.stock} шт.\n"
        )
        result += modification_info + "\n"

    return result


# функция для передачи миниатюр изображения товара
@sync_to_async
def get_thumbnail_url_input_file(custom_sku):
    # Получаем объект модификации товара по custom_sku
    product_modification = ProductModification.objects.get(custom_sku=custom_sku)

    # Получаем URL миниатюры изображения модификации товара
    thumbnail_image_url = product_modification.thumbnail_image_modification_url()

    # Базовый URL вашего веб-сайта
    base_url = 'http://127.0.0.1:8000'

    # Полный URL изображения
    full_url = urljoin(base_url, thumbnail_image_url)

    # Создаем объект URLInputFile
    image = URLInputFile(full_url)

    return image


# функция для передачи большого изображения товара
@sync_to_async
def get_large_image_url_input_file(custom_sku):
    # Получаем объект модификации товара по custom_sku
    product_modification = ProductModification.objects.get(custom_sku=custom_sku)

    # Получаем URL изображения большого размера модификации товара
    large_image_url = product_modification.large_image_modification_url()

    # Базовый URL вашего веб-сайта
    base_url = 'http://127.0.0.1:8000'

    # Полный URL изображения
    full_url = urljoin(base_url, large_image_url)

    # Создаем объект URLInputFile
    image = URLInputFile(full_url)

    return image


# функция для отправки всех миниатюр изображения основного товара
async def thumbnail_image_send_modification_photos(chat_id, sku):
    try:
        # Находим основной товар по артикулу
        product = await sync_to_async(Product.objects.get)(sku=sku)

        # Перебираем все модификации этого товара
        modifications = await sync_to_async(list)(product.modifications.all())

        # Словарь для отслеживания цветов, для которых уже было отправлено фото
        sent_colors = {}

        for modification in modifications:
            # Получаем URL миниатюры изображения модификации товара
            thumbnail_image_url = await sync_to_async(
                modification.thumbnail_image_modification_url
            )()
            if thumbnail_image_url:
                # Получаем цвет модификации
                color = await sync_to_async(lambda: modification.color)()

                # Проверяем, было ли уже отправлено фото для этого цвета
                if color not in sent_colors:
                    # Базовый URL вашего веб-сайта
                    base_url = 'http://127.0.0.1:8000'

                    # Полный URL изображения
                    full_url = urljoin(base_url, thumbnail_image_url)

                    # Создаем объект URLInputFile
                    image = URLInputFile(full_url)

                    # Отправляем фото
                    await bot.send_photo(chat_id=chat_id, photo=image)

                    # Отмечаем цвет как отправленный
                    sent_colors[color] = True

    except Product.DoesNotExist:
        print("Товар с данным артикулом не найден.")


# функция для отправки всех больших изображения основного товара
async def large_image_send_modification_photos(chat_id, sku):
    try:
        # Находим основной товар по артикулу
        product = await sync_to_async(Product.objects.get)(sku=sku)

        # Перебираем все модификации этого товара
        modifications = await sync_to_async(list)(product.modifications.all())

        # Словарь для отслеживания цветов, для которых уже было отправлено фото
        sent_colors = {}

        for modification in modifications:
            # Получаем URL изображения большого размера модификации товара
            large_image_url = await sync_to_async(
                modification.large_image_modification_url
            )()
            if large_image_url:
                # Получаем цвет модификации
                color = await sync_to_async(lambda: modification.color)()

                # Проверяем, было ли уже отправлено фото для этого цвета
                if color not in sent_colors:
                    # Базовый URL вашего веб-сайта
                    base_url = 'http://127.0.0.1:8000'

                    # Полный URL изображения
                    full_url = urljoin(base_url, large_image_url)

                    # Создаем объект URLInputFile
                    image = URLInputFile(full_url)

                    # Отправляем фото
                    await bot.send_photo(chat_id=chat_id, photo=image)

                    # Отмечаем цвет как отправленный
                    sent_colors[color] = True

    except Product.DoesNotExist:
        print("Товар с данным артикулом не найден.")