from asgiref.sync import sync_to_async

from catalog.models import ProductModification, Sale, SaleItem


# Чек остатка на складе
@sync_to_async()
def check_stock_status(custom_sku):
    try:
        modification = ProductModification.objects.get(custom_sku=custom_sku)
        stock = modification.stock
        return True if stock > 0 else False
    except ProductModification.DoesNotExist:
        return False


#  Получение объекта ProductModification по custom_sku
async def get_product_modification(custom_sku):
    try:
        modification = await sync_to_async(ProductModification.objects.get)(custom_sku=custom_sku)
        return modification
    except ProductModification.DoesNotExist:
        # Обработка ситуации, когда ProductModification не найден
        return None


# создание объекта Sale и его элементов
async def create_sale(user_data, telegram_user):
    modification_sku = user_data.get('choosingModification', '')
    quantity = int(user_data.get('enteringQuantity', ''))
    payment = user_data.get('choosingPayment', '')

    product_modification = await get_product_modification(modification_sku)

    if product_modification:
        sale = Sale(
            telegram_user=telegram_user,
            status='completed',
            payment_method=payment,
            source='telegram',
        )

        # Сохранение объекта Sale
        await sync_to_async(sale.save)()

        # Добавление элементов продажи
        await sync_to_async(SaleItem.objects.create)(
            sale=sale,
            product_modification=product_modification,
            quantity=quantity,
        )

        # Сохранение объекта Sale
        await sync_to_async(sale.save)()

        return sale
    else:
        return None
