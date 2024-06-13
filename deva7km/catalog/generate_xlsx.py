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
        price = product.retail_sale_price if product.retail_sale_price > 0 else product.retail_price

        # Формируем название товара с учетом украинского или русского названия цвета и размера
        if modification.color and modification.color.name_uk:
            color_name = modification.color.name_uk
        else:
            color_name = modification.color.name  # Русское название, если украинское не задано

        size_name = modification.size.name if modification.size else ''

        # Формируем уникальный код товара на основе SKU основного товара и его модификаций
        product_code = {product.sku}

        # Формируем строку данных для Excel
        row = [
            f"{product.title_uk if product.title_uk else product.title} №{product.sku} ({color_name}-{size_name})",  # Ім'я товару*
            f"{product_code}-{color_name}-{size_name}",  # Код* (уникальный код товара)
            category_name,  # Група товарів (наименование категории)
            "",  # Штрихкод
            "",  # Штрихкоди
            "",  # УКТ ЗЕД
            price,  # Ціна (в гривнях)*
            "",  # Ваговий товар
            "товар",  # Тип товару
            "З",  # Податкові ставки
            ""  # Залишок (запас товара)
        ]
        data_rows.append(row)

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
