from catalog.models import Sale, Return, ProductModification
from asgiref.sync import sync_to_async
from collections import defaultdict
from datetime import datetime, timedelta


# отчет за сегодня
@sync_to_async
def generate_sales_report_by_day() -> str:
    # Получаем текущую дату
    today = datetime.now().date()

    # Форматируем дату сегодняшнего дня
    formatted_today = today.strftime("%d.%m.%Y")

    # Получаем все продажи и возвраты за сегодня
    sales = Sale.objects.filter(created_at__date=today)
    returns = Return.objects.filter(created_at__date=today)

    # Словарь для хранения количества проданных товаров
    sold_quantity_by_product = defaultdict(int)

    # Обработка продаж для подсчета количества проданных товаров
    for sale in sales:
        for item in sale.items.all():
            product = item.product_modification.product
            sold_quantity_by_product[product] += item.quantity

    # Сортировка продаж по количеству товаров и общей сумме
    top_sales = sorted(sold_quantity_by_product.items(), key=lambda x: (x[1], x[0].title, x[0].sku), reverse=True)[:3]

    # Инициализируем суммы и словари для хранения продаж и возвратов по товарам
    total_sales_amount = 0
    total_returns_amount = 0
    total_cash_sales_amount = 0
    total_non_cash_sales_amount = 0
    sales_by_items = defaultdict(list)
    returns_by_items = defaultdict(list)

    # Обработка продаж
    for sale in sales:
        sale_amount = float(str(sale.calculate_total_amount()).split()[0])
        total_sales_amount += sale_amount

        if sale.payment_method == 'cash':
            total_cash_sales_amount += sale_amount
        elif sale.payment_method == 'non_cash':
            total_non_cash_sales_amount += sale_amount

        for item in sale.items.all():
            sales_by_items[item.product_modification.product].append(item)

    # Обработка возвратов
    for ret in returns:
        return_amount = float(str(ret.calculate_total_amount()).split()[0])
        total_returns_amount += return_amount

        for item in ret.items.all():
            returns_by_items[item.product_modification.product].append(item)

    # Выводим заголовки с отформатированной датой сегодняшнего дня
    report_str = f"Продажи за {formatted_today}\n"

    # Обработка продаж по товарам с сортировкой по артикулу
    for product, items in sorted(sales_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount}грн.)\n"

    # Выводим заголовок для возвратов
    report_str += f"\nВозвраты за {formatted_today}\n"

    # Обработка возвратов по товарам с сортировкой по артикулу
    for product, items in sorted(returns_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount}грн.)\n"

    # Выводим общие суммы
    report_str += (f"\n{'Общая сумма продаж'}: {total_sales_amount:.2f} грн. (нал.: {total_cash_sales_amount:.2f}"
                   f" грн., безнал.: {total_non_cash_sales_amount:.2f} грн.)\n")
    report_str += f"{'Общая сумма возвратов'}: {total_returns_amount:.2f} грн.\n\n"
    report_str += f"{'💵 Чистая касса'}: {(total_cash_sales_amount + total_non_cash_sales_amount) - total_returns_amount:.2f} грн.\n"

    # Выводим ТОП 3 продаж
    report_str += "\nТОП 3 продаж за сегодня\n"
    for rank, (product, quantity) in enumerate(top_sales, start=1):
        total_amount = product.sale_price * quantity if product.sale_price > 0 else product.price * quantity
        report_str += f"{rank}. {product.title} - {product.sku} - {quantity} шт. (на сумму {total_amount:.2f} грн.)\n"

    return report_str


# отчет за вчера
@sync_to_async
def generate_sales_report_by_yesterday() -> str:
    # Получаем вчерашнюю дату
    yesterday = datetime.now().date() - timedelta(days=1)

    # Форматируем дату вчерашнего дня
    formatted_yesterday = yesterday.strftime("%d.%m.%Y")

    # Получаем все продажи и возвраты за вчера
    sales = Sale.objects.filter(created_at__date=yesterday)
    returns = Return.objects.filter(created_at__date=yesterday)

    # Словарь для хранения количества проданных товаров
    sold_quantity_by_product = defaultdict(int)

    # Обработка продаж для подсчета количества проданных товаров
    for sale in sales:
        for item in sale.items.all():
            product = item.product_modification.product
            sold_quantity_by_product[product] += item.quantity

    # Сортировка продаж по количеству товаров и общей сумме
    top_sales = sorted(sold_quantity_by_product.items(), key=lambda x: (x[1], x[0].title, x[0].sku), reverse=True)[:3]

    # Инициализируем суммы и словари для хранения продаж и возвратов по товарам
    total_sales_amount = 0
    total_returns_amount = 0
    total_cash_sales_amount = 0
    total_non_cash_sales_amount = 0
    sales_by_items = defaultdict(list)
    returns_by_items = defaultdict(list)

    # Обработка продаж
    for sale in sales:
        sale_amount = float(str(sale.calculate_total_amount()).split()[0])
        total_sales_amount += sale_amount

        if sale.payment_method == 'cash':
            total_cash_sales_amount += sale_amount
        elif sale.payment_method == 'non_cash':
            total_non_cash_sales_amount += sale_amount

        for item in sale.items.all():
            sales_by_items[item.product_modification.product].append(item)

    # Обработка возвратов
    for ret in returns:
        return_amount = float(str(ret.calculate_total_amount()).split()[0])
        total_returns_amount += return_amount

        for item in ret.items.all():
            returns_by_items[item.product_modification.product].append(item)

    # Выводим заголовки с отформатированной датой вчерашнего дня
    report_str = f"Продажи за вчера ({formatted_yesterday})\n"

    # Обработка продаж по товарам с сортировкой по артикулу
    for product, items in sorted(sales_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount}грн.)\n"

    # Выводим заголовок для возвратов
    report_str += "\nВозвраты за вчера\n"

    # Обработка возвратов по товарам с сортировкой по артикулу
    for product, items in sorted(returns_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount}грн.)\n"

    # Выводим общие суммы
    report_str += (f"\n{'Общая сумма продаж'}: {total_sales_amount:.2f} грн. (нал.: {total_cash_sales_amount:.2f}"
                   f" грн., безнал.: {total_non_cash_sales_amount:.2f} грн.)\n")
    report_str += f"{'Общая сумма возвратов'}: {total_returns_amount:.2f} грн.\n\n"
    report_str += f"{'💵 Чистая касса'}: {(total_cash_sales_amount + total_non_cash_sales_amount) - total_returns_amount:.2f} грн."

    # Выводим ТОП 3 продаж
    report_str += "\nТОП 3 продаж за вчера\n"
    for rank, (product, quantity) in enumerate(top_sales, start=1):
        total_amount = product.sale_price * quantity if product.sale_price > 0 else product.price * quantity
        report_str += f"{rank}. {product.title} - {product.sku} - {quantity} шт. (на сумму {total_amount:.2f} грн.)\n"

    return report_str


#  функция для генерации отчета по продажам за неделю
@sync_to_async
def generate_sales_report_by_week() -> str:
    # Получаем текущую дату
    today = datetime.now().date()

    # Вычисляем начало недели (понедельник) и форматируем его
    start_of_week = today - timedelta(days=today.weekday())
    formatted_start_date = start_of_week.strftime("%d.%m.%Y")

    # Форматируем текущую дату
    formatted_end_date = today.strftime("%d.%m.%Y")

    # Получаем все продажи и возвраты за текущую неделю
    sales = Sale.objects.filter(created_at__date__range=[start_of_week, today])
    returns = Return.objects.filter(created_at__date__range=[start_of_week, today])

    # Словарь для хранения количества проданных товаров
    sold_quantity_by_product = defaultdict(int)

    # Обработка продаж для подсчета количества проданных товаров
    for sale in sales:
        for item in sale.items.all():
            product = item.product_modification.product
            sold_quantity_by_product[product] += item.quantity

    # Сортировка продаж по количеству товаров и общей сумме
    top_sales = sorted(sold_quantity_by_product.items(), key=lambda x: (x[1], x[0].title, x[0].sku), reverse=True)[:3]

    # Инициализируем суммы и словари для хранения продаж и возвратов по товарам
    total_sales_amount = 0
    total_returns_amount = 0
    total_cash_sales_amount = 0
    total_non_cash_sales_amount = 0
    sales_by_items = defaultdict(list)
    returns_by_items = defaultdict(list)

    # Обработка продаж
    for sale in sales:
        sale_amount = float(str(sale.calculate_total_amount()).split()[0])
        total_sales_amount += sale_amount

        if sale.payment_method == 'cash':
            total_cash_sales_amount += sale_amount
        elif sale.payment_method == 'non_cash':
            total_non_cash_sales_amount += sale_amount

        for item in sale.items.all():
            sales_by_items[item.product_modification.product].append(item)

    # Обработка возвратов
    for ret in returns:
        return_amount = float(str(ret.calculate_total_amount()).split()[0])
        total_returns_amount += return_amount

        for item in ret.items.all():
            returns_by_items[item.product_modification.product].append(item)

    # Выводим заголовки с отформатированными датами
    report_str = f"Продажи за неделю ({formatted_start_date} - {formatted_end_date})\n"

    # Обработка продаж по товарам с сортировкой по артикулу
    for product, items in sorted(sales_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount}грн.)\n"

    # Выводим заголовок для возвратов
    report_str += f"\nВозвраты за неделю ({formatted_start_date} - {formatted_end_date})\n"

    # Обработка возвратов по товарам с сортировкой по артикулу
    for product, items in sorted(returns_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount}грн.)\n"

    # Выводим общие суммы
    report_str += (f"\n{'Общая сумма продаж'}: {total_sales_amount:.2f} грн. (нал.: {total_cash_sales_amount:.2f}"
                   f" грн., безнал.: {total_non_cash_sales_amount:.2f} грн.)\n")
    report_str += f"{'Общая сумма возвратов'}: {total_returns_amount:.2f} грн.\n\n"
    report_str += f"{'💵 Чистая касса'}: {(total_cash_sales_amount + total_non_cash_sales_amount) - total_returns_amount:.2f} грн.\n"

    # Выводим ТОП 3 продаж
    report_str += "\nТОП 3 продаж за неделю\n"
    for rank, (product, quantity) in enumerate(top_sales, start=1):
        total_amount = product.sale_price * quantity if product.sale_price > 0 else product.price * quantity
        report_str += f"{rank}. {product.title} - {product.sku} - {quantity} шт. (на сумму {total_amount:.2f} грн.)\n"

    return report_str


#  функция для генерации отчета по продажам за месяц
@sync_to_async
def generate_sales_report_by_month() -> str:
    # Получаем текущую дату
    today = datetime.now().date()

    # Вычисляем первый день текущего месяца и форматируем его
    first_day_of_month = today.replace(day=1)
    formatted_start_date = first_day_of_month.strftime("%d.%m.%Y")

    # Форматируем текущую дату
    formatted_end_date = today.strftime("%d.%m.%Y")

    # Получаем все продажи и возвраты за текущий месяц
    sales = Sale.objects.filter(created_at__date__range=[first_day_of_month, today])
    returns = Return.objects.filter(created_at__date__range=[first_day_of_month, today])

    # Словарь для хранения количества проданных товаров
    sold_quantity_by_product = defaultdict(int)

    # Обработка продаж для подсчета количества проданных товаров
    for sale in sales:
        for item in sale.items.all():
            product = item.product_modification.product
            sold_quantity_by_product[product] += item.quantity

    # Сортировка продаж по количеству товаров и общей сумме
    top_sales = sorted(sold_quantity_by_product.items(), key=lambda x: (x[1], x[0].title, x[0].sku), reverse=True)[:3]

    # Инициализируем суммы и словари для хранения продаж и возвратов по товарам
    total_sales_amount = 0
    total_returns_amount = 0
    total_cash_sales_amount = 0
    total_non_cash_sales_amount = 0
    sales_by_items = defaultdict(list)
    returns_by_items = defaultdict(list)

    # Обработка продаж
    for sale in sales:
        sale_amount = float(str(sale.calculate_total_amount()).split()[0])
        total_sales_amount += sale_amount

        if sale.payment_method == 'cash':
            total_cash_sales_amount += sale_amount
        elif sale.payment_method == 'non_cash':
            total_non_cash_sales_amount += sale_amount

        for item in sale.items.all():
            sales_by_items[item.product_modification.product].append(item)

    # Обработка возвратов
    for ret in returns:
        return_amount = float(str(ret.calculate_total_amount()).split()[0])
        total_returns_amount += return_amount

        for item in ret.items.all():
            returns_by_items[item.product_modification.product].append(item)

    # Выводим заголовки с отформатированными датами
    report_str = f"Продажи за месяц ({formatted_start_date} - {formatted_end_date})\n"

    # Обработка продаж по товарам с сортировкой по артикулу
    for product, items in sorted(sales_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount:.2f}грн.)\n"

    # Выводим заголовок для возвратов
    report_str += f"\nВозвраты за месяц ({formatted_start_date} - {formatted_end_date})\n"

    # Обработка возвратов по товарам с сортировкой по артикулу
    for product, items in sorted(returns_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount:.2f}грн.)\n"

    # Выводим общие суммы
    report_str += (f"\n{'Общая сумма продаж'}: {total_sales_amount:.2f} грн. (нал.: {total_cash_sales_amount:.2f}"
                   f" грн., безнал.: {total_non_cash_sales_amount:.2f} грн.)\n")
    report_str += f"{'Общая сумма возвратов'}: {total_returns_amount:.2f} грн.\n\n"
    report_str += f"{'💵 Чистая касса'}: {(total_cash_sales_amount + total_non_cash_sales_amount) - total_returns_amount:.2f} грн.\n"

    # Выводим ТОП 3 продаж
    report_str += "\nТОП 3 продаж за месяц\n"
    for rank, (product, quantity) in enumerate(top_sales, start=1):
        total_amount = product.sale_price * quantity if product.sale_price > 0 else product.price * quantity
        report_str += f"{rank}. {product.title} - {product.sku} - {quantity} шт. (на сумму {total_amount:.2f} грн.)\n"

    return report_str


#  функция для генерации отчета по продажам за год
@sync_to_async
def generate_sales_report_by_year() -> str:
    # Получаем текущую дату
    today = datetime.now().date()

    # Вычисляем первый день текущего года и форматируем его
    first_day_of_year = today.replace(month=1, day=1)
    formatted_start_date = first_day_of_year.strftime("%d.%m.%Y")

    # Форматируем текущую дату
    formatted_end_date = today.strftime("%d.%m.%Y")

    # Получаем все продажи и возвраты за текущий год
    sales = Sale.objects.filter(created_at__date__range=[first_day_of_year, today])
    returns = Return.objects.filter(created_at__date__range=[first_day_of_year, today])

    # Словарь для хранения количества проданных товаров
    sold_quantity_by_product = defaultdict(int)

    # Обработка продаж для подсчета количества проданных товаров
    for sale in sales:
        for item in sale.items.all():
            product = item.product_modification.product
            sold_quantity_by_product[product] += item.quantity

    # Сортировка продаж по количеству товаров и общей сумме
    top_sales = sorted(sold_quantity_by_product.items(), key=lambda x: (x[1], x[0].title, x[0].sku), reverse=True)[:3]

    # Инициализируем суммы и словари для хранения продаж и возвратов по товарам
    total_sales_amount = 0
    total_returns_amount = 0
    total_cash_sales_amount = 0
    total_non_cash_sales_amount = 0
    sales_by_items = defaultdict(list)
    returns_by_items = defaultdict(list)

    # Обработка продаж
    for sale in sales:
        sale_amount = float(str(sale.calculate_total_amount()).split()[0])
        total_sales_amount += sale_amount

        if sale.payment_method == 'cash':
            total_cash_sales_amount += sale_amount
        elif sale.payment_method == 'non_cash':
            total_non_cash_sales_amount += sale_amount

        for item in sale.items.all():
            sales_by_items[item.product_modification.product].append(item)

    # Обработка возвратов
    for ret in returns:
        return_amount = float(str(ret.calculate_total_amount()).split()[0])
        total_returns_amount += return_amount

        for item in ret.items.all():
            returns_by_items[item.product_modification.product].append(item)

    # Выводим заголовки с обновленным форматом
    report_str = f"Продажи за год ({formatted_start_date} - {formatted_end_date})\n"

    # Обработка продаж по товарам с сортировкой по артикулу
    for product, items in sorted(sales_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount:.2f}грн.)\n"

    # Выводим заголовок для возвратов
    report_str += f"\nВозвраты за год ({formatted_start_date} - {formatted_end_date})\n"

    # Обработка возвратов по товарам с сортировкой по артикулу
    for product, items in sorted(returns_by_items.items(), key=lambda x: x[0].sku):
        total_amount = product.sale_price * sum(item.quantity for item in items) if product.sale_price > 0 else product.price * sum(item.quantity for item in items)
        report_str += f"➡️ {product.sku} ({sum(item.quantity for item in items)} шт. сумма {total_amount:.2f}грн.)\n"

    # Выводим общие суммы
    report_str += (f"\n{'Общая сумма продаж'}: {total_sales_amount:.2f} грн. (нал.: {total_cash_sales_amount:.2f}"
                   f" грн., безнал.: {total_non_cash_sales_amount:.2f} грн.)\n")
    report_str += f"{'Общая сумма возвратов'}: {total_returns_amount:.2f} грн.\n\n"
    report_str += f"{'💵 Чистая касса'}: {(total_cash_sales_amount + total_non_cash_sales_amount) - total_returns_amount:.2f} грн.\n"

    # Выводим ТОП 3 продаж
    report_str += "\nТОП 3 продаж за год\n"
    for rank, (product, quantity) in enumerate(top_sales, start=1):
        total_amount = product.sale_price * quantity if product.sale_price > 0 else product.price * quantity
        report_str += f"{rank}. {product.title} - {product.sku} - {quantity} шт. (на сумму {total_amount:.2f} грн.)\n"

    return report_str


#  функция для получения отчета об остатках на складе
@sync_to_async
def get_total_stock():
    available_modifications = ProductModification.objects.filter(stock__gt=0).order_by('custom_sku')

    report_str = "Общие остатки\n\n"
    total_stock_amount = 0

    for modification in available_modifications:
        stock_quantity = modification.stock

        # Используем цену товара (sale_price), если она больше 0, иначе используем обычную цену (price)
        price = modification.product.sale_price if modification.product.sale_price > 0 else modification.product.price

        total_stock_amount += price * stock_quantity
        amount_str = "{:.2f}".format(price * stock_quantity).rstrip("0").rstrip(".")
        report_str += (
            f"➡️ {modification.custom_sku} "
            f"({stock_quantity} шт. сумма {amount_str} грн.)\n"
        )

    total_stock_amount_str = "{:.2f}".format(total_stock_amount).rstrip("0").rstrip(".")
    report_str += f"\nОбщая сумма всех остатков: {total_stock_amount_str} грн."

    return report_str


