from asgiref.sync import sync_to_async
from catalog.models import Inventory, InventoryItem
from tg_bot.services.sells import get_product_modification


# создание объекта Inventory и его элементов
async def create_inventory(user_data, telegram_user):
    products_list = user_data.get('products_list', [])
    inventory = Inventory(
        telegram_user=telegram_user,
        status='completed',
        source='telegram',
    )

    try:
        # Сохранение объекта Inventory
        await sync_to_async(inventory.save)()

        for product_info in products_list:
            modification_sku = product_info.get('choosingModification', '')
            entering_quantity = product_info.get('enteringQuantity', '')

            # Проверка корректности данных
            if not entering_quantity.isdigit():
                raise ValueError(f"Некорректное значение количества товара: {entering_quantity}")

            quantity = int(entering_quantity)

            product_modification = await get_product_modification(modification_sku)

            inventory_item = InventoryItem(
                inventory=inventory,
                product_modification=product_modification,
                quantity=quantity,
            )
            await sync_to_async(inventory_item.save)()

        # Повторное сохранение объекта Inventory
        await sync_to_async(inventory.save)()
        return inventory

    except ValueError as e:
        # Логирование ошибки
        print(f"Ошибка при создании инвентаризации: {e}")
        # Возвращаем None в случае ошибки
        return None
