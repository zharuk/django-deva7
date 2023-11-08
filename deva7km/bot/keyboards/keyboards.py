from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from catalog.models import Product


# клавиатура списка всех товаров, где каждая кнопка это основной артикул товара
async def create_inline_kb_main_sku():
    products = await sync_to_async(list)(Product.objects.all())  # Получаем все товары
    buttons = []

    # Создаем кнопки на основе ключей из всех товаров
    for product in products:
        # Преобразуем ключ из байтов в строку
        sku = product.sku
        # Пропускаем ключ с названием 'reports'
        buttons.append(InlineKeyboardButton(text=sku, callback_data=sku + '_main_sku'))
    # Сортируем кнопки по возрастанию
    buttons.sort(key=lambda x: int(x.text))
    # Задаем количество кнопок в каждом ряду (здесь используется 8)
    buttons_per_row = 8
    # Разбиваем список кнопок на ряды
    rows = [buttons[i:i + buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]

    return InlineKeyboardMarkup(inline_keyboard=rows)


# клавиатура основного меню
async def create_main_menu_kb():
    # Создаем кнопки "Список товаров", "Добавить товар", "Добавить товар одной строкой", "Статистика"
    products_button = InlineKeyboardButton(text='📋 Список товаров', callback_data='products')
    sale_button = InlineKeyboardButton(text='📈 Продать', callback_data='sale')
    return_button = InlineKeyboardButton(text='🔙 Вернуть', callback_data='return')
    report_button = InlineKeyboardButton(text='📊 Статистика', callback_data='report')
    # Создаем список кнопок
    inline_keyboard = [[products_button], [sale_button], [return_button], [report_button]]

    # Возвращаем объект инлайн-клавиатуры
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
