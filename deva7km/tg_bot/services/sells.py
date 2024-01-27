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
@sync_to_async()
def get_product_modification(custom_sku):
    try:
        modification = ProductModification.objects.get(custom_sku=custom_sku)
        return modification
    except ProductModification.DoesNotExist:
        # Обработка ситуации, когда ProductModification не найден
        return None


# создание объекта Sale и его элементов
async def create_sale(user_data, telegram_user):
    products_list = user_data.get('products_list', [])

    payment = user_data.get('choosingPayment', '')
    comment = user_data.get('comment', '')

    sale = Sale(
        telegram_user=telegram_user,
        status='completed',
        payment_method=payment,
        source='telegram',
        comment=comment
    )

    # Сохранение объекта Sale
    await sync_to_async(sale.save)()

    for product_info in products_list:
        modification_sku = product_info.get('choosingModification', '')
        quantity = int(product_info.get('enteringQuantity', ''))

        product_modification = await get_product_modification(modification_sku)

        sale_item = SaleItem(
            sale=sale,
            product_modification=product_modification,
            quantity=quantity,
        )
        await sync_to_async(sale_item.save)()

    # Сохранение объекта Sale
    await sync_to_async(sale.save)()
    return sale
