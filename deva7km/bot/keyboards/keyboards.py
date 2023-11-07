from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

from catalog.models import Product


async def inline_keyboard_main_sku():
    products = await sync_to_async(list)(Product.objects.all())  # Получаем все товары

    buttons = []

    # Создаем кнопки на основе ключей из data_user > products
    for product in products:
        # Преобразуем ключ из байтов в строку
        sku = product.sku
        # Пропускаем ключ с названием 'reports'
        buttons.append(InlineKeyboardButton(text=sku, callback_data=sku + '_main_sku'))
    # Сортируем кнопки по возрастанию
    buttons.sort(key=lambda x: int(x.text))

    return InlineKeyboardMarkup(inline_keyboard=[buttons])

# async def create_sku_kb(user_id):
#     # получаем данные из Redis по id пользователя
#     data_user = await get_data_from_redis(user_id)
#     # Инициализируем список для кнопок
#     buttons = []
#     # Создаем кнопки на основе ключей из data_user > products
#     for key in data_user['products']:
#         # Преобразуем ключ из байтов в строку
#         key_sku = list(key.keys())[0]
#         # Пропускаем ключ с названием 'reports'
#         buttons.append(InlineKeyboardButton(text=key_sku, callback_data=key_sku + '_main_sku'))
#     # Сортируем кнопки по возрастанию
#     buttons.sort(key=lambda x: int(x.text))
#
#     # Задаем количество кнопок в каждом ряду (здесь используется 8)
#     buttons_per_row = 8
#     # Разбиваем список кнопок на ряды
#     rows = [buttons[i:i + buttons_per_row] for i in range(0, len(buttons), buttons_per_row)]
#
#     # Добавляем кнопку "Добавить товар" с callback_data='add' в отдельный ряд
#     buttons_add = InlineKeyboardButton(text='📁 Создать товар', callback_data='add')
#     rows.append([buttons_add])
#
#     # Добавляем кнопку "Вернутся в меню" с callback_data='start' в отдельный ряд
#     buttons_back = InlineKeyboardButton(text='↩️ Вернуться в меню', callback_data='start')
#     rows.append([buttons_back])
#
#     # Возвращаем объект инлайн-клавиатуры
#     return InlineKeyboardMarkup(inline_keyboard=rows)



