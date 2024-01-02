from asgiref.sync import sync_to_async
from catalog.models import Return, ReturnItem
from tg_bot.services.sells import get_product_modification


# создание объекта Return и его элементов
async def create_return(user_data, telegram_user):
    modification_sku = user_data.get('choosingModification', '')
    quantity = int(user_data.get('enteringQuantity', ''))

    product_modification = await get_product_modification(modification_sku)

    if product_modification:
        # Создание объекта Return
        return_instance = Return(
            telegram_user=telegram_user,
            source='telegram',
        )

        # Создание объекта ReturnItem
        return_item = ReturnItem(
            return_sale=return_instance,
            product_modification=product_modification,
            quantity=quantity,
        )

        # Сохранение объекта Return
        await sync_to_async(return_instance.save)()
        # Сохранение объекта ReturnItem
        await sync_to_async(return_item.save)()

        return return_instance
    else:
        return None

