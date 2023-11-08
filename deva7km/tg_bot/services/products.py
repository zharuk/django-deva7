from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async

from catalog.models import Product


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
