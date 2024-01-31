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

    # Сохранение объекта Sale
    await sync_to_async(inventory.save)()

    for product_info in products_list:
        modification_sku = product_info.get('choosingModification', '')
        quantity = int(product_info.get('enteringQuantity', ''))

        product_modification = await get_product_modification(modification_sku)

        inventory_item = InventoryItem(
            inventory=inventory,
            product_modification=product_modification,
            quantity=quantity,
        )
        await sync_to_async(inventory_item.save)()

    # Сохранение объекта Sale
    await sync_to_async(inventory.save)()
    return inventory
