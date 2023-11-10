from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from catalog.models import Product, ProductModification


# клавиатура основного меню
async def create_main_menu_kb():
    # Создаем кнопки "Список товаров", "Добавить товар", "Добавить товар одной строкой", "Статистика"
    products_button = InlineKeyboardButton(text='📋 Список товаров', callback_data='products')
    sell_button = InlineKeyboardButton(text='📈 Продать', callback_data='sell')
    return_button = InlineKeyboardButton(text='🔙 Вернуть', callback_data='return')
    report_button = InlineKeyboardButton(text='📊 Статистика', callback_data='report')
    # Создаем список кнопок
    inline_keyboard = [[products_button], [sell_button], [return_button], [report_button]]

    # Возвращаем объект инлайн-клавиатуры
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# клавиатура списка всех товаров, где каждая кнопка это основной артикул товара
async def create_inline_kb_main_sku(callback):
    products = await sync_to_async(list)(Product.objects.all())  # Получаем все товары
    buttons = []

    for product in products:
        sku = product.sku
        buttons.append(InlineKeyboardButton(text=sku, callback_data=f'{sku}_main_sku_{callback}'))

    # Сортируем кнопки по возрастанию
    buttons.sort(key=lambda x: int(x.text))
    # Задаем количество кнопок в каждом ряду (здесь используется 8)
    buttons_per_row = 7
    # Разбиваем список кнопок на ряды
    rows = [buttons[i:i + buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]
    # добавим кнопку 'Назад'
    rows.append([InlineKeyboardButton(text='❌️ Отмена операции', callback_data='cancel')])

    return InlineKeyboardMarkup(inline_keyboard=rows)


# клавиатура с одной кнопкой 'Назад' c callback data 'products'
async def create_inline_kb_return(callback):
    button = [InlineKeyboardButton(text='❌️ Отмена операции', callback_data='cancel')]
    return InlineKeyboardMarkup(inline_keyboard=[button])


#  клавиатура с кнопками артикулов товаров модификаций товара
async def create_inline_kb_modifications(main_sku, callback):
    product_modifications = await sync_to_async(list)(ProductModification.objects.filter(product__sku=main_sku))
    buttons = []

    for modification in product_modifications:
        custom_sku = modification.custom_sku
        buttons.append(InlineKeyboardButton(text=custom_sku, callback_data=f'{custom_sku}_modification_{callback}'))

    buttons_per_row = 2
    rows = [buttons[i:i + buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]
    rows.append([InlineKeyboardButton(text='↩️ Назад', callback_data=callback)])
    rows.append([InlineKeyboardButton(text='❌️ Отмена операции', callback_data='cancel')])

    return InlineKeyboardMarkup(inline_keyboard=rows)


async def create_inline_kb_numbers():
    buttons = []

    for number in range(1, 11):
        buttons.append(InlineKeyboardButton(text=str(number), callback_data=f'{number}'))

    # Разбиваем список кнопок на ряды по 5 кнопок в каждом
    rows = [buttons[i:i + 5] for i in range(0, len(buttons), 5)]
    # Добавляем кнопку 'Назад'
    rows.append([InlineKeyboardButton(text='❌️ Отмена операции', callback_data='cancel')])

    return InlineKeyboardMarkup(inline_keyboard=rows)


async def create_payment_type_keyboard():
    # Создаем кнопки для наличной и безналичной оплаты
    cash_button = InlineKeyboardButton(text='Наличная', callback_data=f'cash')
    non_cash_button = InlineKeyboardButton(text='Безналичная', callback_data=f'non_cash')

    # Собираем кнопки в ряд
    row = [cash_button, non_cash_button]

    # Добавляем ряд с кнопками в клавиатуру
    keyboard = [row, [InlineKeyboardButton(text='❌️ Отмена операции', callback_data='cancel')]]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def create_inline_kb_cancel():
    button = InlineKeyboardButton(text='❌️ Отмена операции', callback_data='cancel')
    return InlineKeyboardMarkup(inline_keyboard=[[button]])
