from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from catalog.models import Product, ProductModification


# клавиатура основного меню
async def create_main_menu_kb():
    # Создаем кнопки "Список товаров", "Добавить товар", "Добавить товар одной строкой", "Статистика"
    products_button = InlineKeyboardButton(text='📋 Список товаров', callback_data='products')
    sell_button = InlineKeyboardButton(text='💸 Продать', callback_data='sell')
    return_button = InlineKeyboardButton(text='🔙 Вернуть', callback_data='return')
    inventory_button = InlineKeyboardButton(text='📈 Оприходование', callback_data='inventory')
    write_off_button = InlineKeyboardButton(text='📉 Списание', callback_data='write_off')
    report_button = InlineKeyboardButton(text='📊 Статистика', callback_data='report')
    # Создаем список кнопок
    inline_keyboard = [[products_button], [sell_button], [return_button], [inventory_button], [write_off_button],
                       [report_button]]

    # Возвращаем объект инлайн-клавиатуры
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def create_inline_kb_main_sku(callback, page=1):
    def custom_sort_key(sku):
        # Вложенная функция для сортировки артикулов
        numeric_part = ''.join(filter(str.isdigit, sku))
        return int(numeric_part) if numeric_part else float('inf')

    products = await sync_to_async(list)(Product.objects.all())
    products = sorted(products, key=lambda x: custom_sort_key(x.sku), reverse=True)

    buttons = []

    # Определим количество кнопок на одной странице (например, 8)
    buttons_per_page = 49
    start_index = (page - 1) * buttons_per_page
    end_index = start_index + buttons_per_page

    for product in products[start_index:end_index]:
        sku = product.sku
        buttons.append(InlineKeyboardButton(text=sku, callback_data=f'{sku}_main_sku_{callback}_{page}'))

    # Задаем количество кнопок в каждом ряду (здесь используется 2)
    buttons_per_row = 7
    rows = [buttons[i:i + buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]

    # Добавим кнопки навигации
    navigation_buttons = []

    # Добавляем кнопку "Назад" только на страницах больше 1
    if page > 1:
        navigation_buttons.append(InlineKeyboardButton(text='◀️ Назад', callback_data=f'prev_{callback}_{page}'))

    # Добавляем кнопку "Вперед" только если есть еще товары на следующей странице
    if len(products) > end_index:
        navigation_buttons.append(InlineKeyboardButton(text='▶️ Вперед', callback_data=f'next_{callback}_{page}'))

    rows.append(navigation_buttons)
    rows.append([InlineKeyboardButton(text='↩️ Отмена', callback_data='cancel')])

    return InlineKeyboardMarkup(inline_keyboard=rows)


# клавиатура с одной кнопкой 'Назад' c callback data 'products'
async def create_inline_kb_return(callback):
    button = [InlineKeyboardButton(text='↩️ Назад', callback_data=callback)]
    return InlineKeyboardMarkup(inline_keyboard=[button])


#  клавиатура с кнопками артикулов товаров модификаций товара
async def create_inline_kb_modifications(main_sku, callback):
    product_modifications = await sync_to_async(list)(ProductModification.objects.filter(product__sku=main_sku))
    buttons = []

    for modification in product_modifications:
        custom_sku = modification.custom_sku
        stock = modification.stock
        buttons.append(InlineKeyboardButton(text=f'{custom_sku} ({stock} шт.)',
                                            callback_data=f'{custom_sku}_modification_{callback}'))

    buttons_per_row = 2
    rows = [buttons[i:i + buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]
    rows.append([InlineKeyboardButton(text='↩️ Отмена операции', callback_data='cancel')])

    return InlineKeyboardMarkup(inline_keyboard=rows)


async def create_inline_kb_numbers(quantity=10):
    buttons = []

    for number in range(1, quantity + 1):
        buttons.append(InlineKeyboardButton(text=str(number), callback_data=f'{number}'))

    # Разбиваем список кнопок на ряды по 5 кнопок в каждом
    rows = [buttons[i:i + 5] for i in range(0, len(buttons), 5)]
    # Добавляем кнопку 'Назад'
    rows.append([InlineKeyboardButton(text='↩️ Отмена операции', callback_data='cancel')])

    return InlineKeyboardMarkup(inline_keyboard=rows)


async def create_payment_type_keyboard():
    # Создаем кнопки для наличной и безналичной оплаты
    cash_button = InlineKeyboardButton(text='Наличная', callback_data=f'cash')
    non_cash_button = InlineKeyboardButton(text='Безналичная', callback_data=f'non_cash')

    # Собираем кнопки в ряд
    row = [cash_button, non_cash_button]

    # Добавляем ряд с кнопками в клавиатуру
    keyboard = [row, [InlineKeyboardButton(text='♾️ Добавить еще товар', callback_data='add_more')],
                [InlineKeyboardButton(text='↩️ Отмена операции', callback_data='cancel')]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def create_inline_kb_cancel():
    button = InlineKeyboardButton(text='↩️ Отмена операции', callback_data='cancel')
    return InlineKeyboardMarkup(inline_keyboard=[[button]])


# клавиатура для reports для отчета по продажам и возвратам будет состоять из кнопок "отчет за сегодня",
# "отчет за вчера", "отчет за неделю", "отчет за месяц", "отчет за год"
async def create_report_kb():
    today_button = InlineKeyboardButton(text='Отчет за сегодня', callback_data='today')
    yesterday_button = InlineKeyboardButton(text='Отчет за вчера', callback_data='yesterday')
    week_button = InlineKeyboardButton(text='Отчет за неделю', callback_data='week')
    month_button = InlineKeyboardButton(text='Отчет за месяц', callback_data='month')
    year_button = InlineKeyboardButton(text='Отчет за год', callback_data='year')
    total_stock = InlineKeyboardButton(text='📑 Остатки по товарам', callback_data='total_stock')
    cancel_button = InlineKeyboardButton(text='↩️ Отмена операции', callback_data='cancel')
    return InlineKeyboardMarkup(
        inline_keyboard=[[today_button, yesterday_button], [week_button, month_button], [year_button], [total_stock],
                         [cancel_button]])
