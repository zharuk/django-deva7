from datetime import datetime
from aiogram.utils.markdown import hbold
from catalog.models import Sale, Return
from asgiref.sync import sync_to_async
from collections import defaultdict


#  Генерация отчета по продажам за день
@sync_to_async
def generate_sales_report_by_day():
    # Получаем текущую дату
    today = datetime.now().date()

    # Получаем все продажи и возвраты за сегодня
    sales = Sale.objects.filter(created_at__date=today)
    returns = Return.objects.filter(created_at__date=today)

    # Инициализируем суммы
    total_sales_amount = 0
    total_returns_amount = 0
    total_cash_sales_amount = 0
    total_non_cash_sales_amount = 0

    # Словари для хранения продаж и возвратов по товарам
    sales_by_items = defaultdict(list)
    returns_by_items = defaultdict(list)

    # Обработка продаж
    for sale in sales:
        sale_amount = float(sale.calculate_total_amount().split()[0])
        total_sales_amount += sale_amount

        if sale.payment_method == 'cash':
            total_cash_sales_amount += sale_amount
        elif sale.payment_method == 'non_cash':
            total_non_cash_sales_amount += sale_amount

        for item in sale.items.all():
            sales_by_items[item.product_modification].append(item)

    # Обработка возвратов
    for ret in returns:
        return_amount = float(ret.calculate_total_amount().split()[0])
        total_returns_amount += return_amount

        for item in ret.items.all():
            returns_by_items[item.product_modification].append(item)

    # Выводим заголовки
    report_str = hbold("✅ Продажи за сегодня\n")

    # Обработка продаж по товарам
    for product_modification, items in sales_by_items.items():
        report_str += f"➡️ {product_modification.product.title}-{product_modification.custom_sku} ({sum(item.quantity for item in items)} шт.)\n"

    # Выводим заголовок для возвратов
    report_str += hbold("\nВозвраты за сегодня\n")

    # Обработка возвратов по товарам
    for product_modification, items in returns_by_items.items():
        report_str += f"⬅️ {product_modification.product.title}-{product_modification.custom_sku} ({sum(item.quantity for item in items)} шт.)\n"

    # Выводим общие суммы
    report_str += (f"\n{hbold('Общая сумма продаж')}: {total_sales_amount:.2f} UAH (нал.: {total_cash_sales_amount:.2f}"
                   f" UAH, безнал.: {total_non_cash_sales_amount:.2f} UAH)\n")
    report_str += f"{hbold('Общая сумма возвратов')}: {total_returns_amount:.2f} UAH\n\n"
    report_str += f"{hbold('💵 Чистая касса')}: {total_cash_sales_amount - total_returns_amount:.2f} UAH"

    return report_str
