# myapp/generate_xlsx.py
import openpyxl
from django.http import HttpResponse
from .models import ProductModification, Category
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

    # Добавляем данные из модели ProductModification
    for modification in ProductModification.objects.select_related('product', 'color', 'size',
                                                                   'product__category').all():
        product = modification.product
        category_name = product.category.name if product.category else ''
        price = product.retail_sale_price if product.retail_sale_price > 0 else product.retail_price

        # Формируем название товара с учетом украинского или русского названия цвета
        if modification.color and modification.color.name_uk:
            color_name = modification.color.name_uk
        else:
            color_name = modification.color.name  # Русское название, если украинское не задано

        if modification.size:
            size_name = modification.size.name
        else:
            size_name = ''

        # Формируем уникальный код товара на основе SKU основного товара и его модификаций
        product_code = f"{product.sku} - {color_name} - {size_name}"

        # Формируем строку данных для Excel
        row = [
            f"{product.title_uk if product.title_uk else product.title} №{product.sku} ({color_name} - {size_name})",  # Ім'я товару*
            product_code,  # Код* (уникальный код товара)
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
        sheet.append(row)

    # Создаем HTTP-ответ с файлом Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=products.xlsx'
    workbook.save(response)

    return response
