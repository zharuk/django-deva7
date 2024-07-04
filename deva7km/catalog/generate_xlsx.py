import openpyxl
from django.http import HttpResponse
from .models import ProductModification
from django.utils.translation import activate


def generate_product_xlsx(request):
    # Устанавливаем язык на украинский
    activate('uk')

    # Создаем книгу и лист
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Список товарів'  # Устанавливаем название страницы в Excel

    # Добавляем заголовки
    headers = [
        "Ім'я товару*", "Код*", "Група товарів", "Штрихкод", "Штрихкоди",
        "УКТ ЗЕД", "Ціна (в гривнях)*", "Ваговий товар", "Тип товару",
        "Податкові ставки", "Залишок"
    ]
    sheet.append(headers)

    # Список для хранения строк данных
    data_rows = []

    # Добавляем данные из модели ProductModification
    for modification in ProductModification.objects.select_related('product', 'color', 'size',
                                                                   'product__category').all():
        product = modification.product
        category_name = product.category.name if product.category else ''

        # Получение названий цвета и размера
        color_name = modification.color.name if modification.color else ''
        size_name = modification.size.name if modification.size else ''

        # Формируем уникальный код товара на основе SKU основного товара и его модификаций
        product_code = product.sku

        # Получение цены для розничной и оптовой продажи
        retail_price = product.retail_sale_price if product.retail_sale_price > 0 else product.retail_price
        wholesale_price = product.sale_price if product.sale_price > 0 else product.price

        # Формируем название товара для розничной и оптовой продажи
        retail_title = f"РОЗ. {product.title} №{product_code} ({color_name}-{size_name})"
        wholesale_title = f"ОПТ. {product.title} №{product_code} ({color_name}-{size_name})"

        # Формируем строки данных для розничной и оптовой продажи
        retail_row = [
            retail_title,  # Ім'я товару*
            f"{product_code}-{color_name}-{size_name}-роз",  # Код* (уникальный код товара)
            category_name,  # Група товарів (наименование категории)
            "",  # Штрихкод
            "",  # Штрихкоди
            "",  # УКТ ЗЕД
            retail_price,  # Ціна (в гривнях)*
            "",  # Ваговий товар
            "товар",  # Тип товару
            "З",  # Податкові ставки
            ""  # Залишок (запас товара)
        ]

        wholesale_row = [
            wholesale_title,  # Ім'я товару*
            f"{product_code}-{color_name}-{size_name}-опт",  # Код* (уникальный код товара)
            category_name,  # Група товарів (наименование категории)
            "",  # Штрихкод
            "",  # Штрихкоди
            "",  # УКТ ЗЕД
            wholesale_price,  # Ціна (в гривнях)*
            "",  # Ваговий товар
            "товар",  # Тип товару
            "З",  # Податкові ставки
            ""  # Залишок (запас товара)
        ]

        data_rows.extend([retail_row, wholesale_row])

    # Сортируем список по столбцу "Код"
    data_rows.sort(key=lambda x: x[1])  # x[1] - это столбец "Код"

    # Записываем отсортированные данные в лист Excel
    for row in data_rows:
        sheet.append(row)

    # Создаем HTTP-ответ с файлом Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'
    workbook.save(response)

    return response
