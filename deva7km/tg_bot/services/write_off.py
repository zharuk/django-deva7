from asgiref.sync import sync_to_async
from catalog.models import WriteOff, WriteOffItem
from tg_bot.services.sells import get_product_modification


# создание объекта WriteOff и его элементов
async def create_write_off(user_data, telegram_user):
    modification_sku = user_data.get('choosingModification', '')
    quantity = int(user_data.get('enteringQuantity', ''))

    product_modification = await get_product_modification(modification_sku)

    if product_modification:
        # Создание объекта WriteOff
        write_off_instance = WriteOff(
            telegram_user=telegram_user,
            source='telegram',
        )

        # Создание объекта WriteOffItem
        write_off_item = WriteOffItem(
            write_off=write_off_instance,
            product_modification=product_modification,
            quantity=quantity,
        )

        # Сохранение объекта WriteOff
        await sync_to_async(write_off_instance.save)()
        # Сохранение объекта WriteOffItem
        await sync_to_async(write_off_item.save)()

        return write_off_instance
    else:
        return None

