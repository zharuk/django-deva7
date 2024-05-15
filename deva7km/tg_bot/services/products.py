import logging
from urllib.parse import urljoin
from aiogram import Bot
from aiogram.types import URLInputFile
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async
from catalog.models import Product, ProductModification
try:
    from deva7km.local_settings import BOT_TOKEN, BASE_URL
except ImportError:
    from deva7km.prod_settings import BOT_TOKEN, BASE_URL


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
    if product.sale_price:
        result += hbold(f"💰 Цена распродажи: {product.sale_price} ({product.currency})\n\n")
    result += hbold(f"📒 Модификации:\n\n")

    # Перебираем все модификации этого товара
    for modification in product.modifications.all().order_by('color__name'):
        # Формируем информацию о модификации
        modification_info = (
            f"➡️️ Цвет: {modification.color.name}\n"
            f"➡️️ Размер: {modification.size.name}\n"
        )
        modification_info += f"✅️️ На складе: {modification.stock} шт.\n" if modification.stock > 0 else "⛔️ Нет в наличии\n"
        result += modification_info + "\n"

    return result


# функция для передачи большого изображения модификации товара
@sync_to_async
def get_large_image_url_input_file(custom_sku):
    # Получаем объект модификации товара по custom_sku
    product_modification = ProductModification.objects.get(custom_sku=custom_sku)

    # Получаем URL изображения большого размера модификации товара
    large_image_url = product_modification.get_first_large_image_modification_url()

    # Создаем объект URLInputFile
    image = URLInputFile(large_image_url)

    return image


@sync_to_async
def get_collage_image_for_product(sku):
    try:
        # Получаем основной товар по артикулу
        product = Product.objects.get(sku=sku)

        # Получаем URL изображения коллажа
        collage_image_url = product.collage_image_url()

        return collage_image_url

    except Product.DoesNotExist:
        logging.error("Основной товар с данным артикулом не найден.")
        return None
    except Exception as e:
        logging.exception(f"Произошла ошибка: {str(e)}")
        return None