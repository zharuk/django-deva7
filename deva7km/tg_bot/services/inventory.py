from asgiref.sync import sync_to_async
from catalog.models import Inventory, InventoryItem
from tg_bot.services.sells import get_product_modification


# создание объекта Inventory и его элементов
async def create_inventory(user_data, telegram_user):
    modification_sku = user_data.get('choosingModification', '')
    quantity = int(user_data.get('enteringQuantity', ''))

    product_modification = await get_product_modification(modification_sku)

    if product_modification:
        # Создание объекта inventory
        inventory_instance = Inventory(
            telegram_user=telegram_user,
            source='telegram',
        )

        # Сохранение объекта inventory
        await sync_to_async(inventory_instance.save)()

        # Добавление элементов оприходования
        await sync_to_async(InventoryItem.objects.create)(
            inventory=inventory_instance,
            product_modification=product_modification,
            quantity=quantity,
        )
        # Сохранение объекта inventory
        await sync_to_async(inventory_instance.save)()

        return inventory_instance
    else:
        return None
