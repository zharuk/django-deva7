from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from deva7km import settings


# клавиатура основного меню
async def create_main_menu_kb(telegram_id=None) -> InlineKeyboardMarkup:
    # Создаем базовые URL
    base_url = f'{settings.BASE_URL}/seller_cabinet'

    # Обновляем URL для Web App, если telegram_id предоставлен
    def create_url(path):
        url = f'{base_url}{path}'
        if telegram_id:
            url += f'?telegram_id={telegram_id}'
        return url

    # Создаем кнопки с обновленными URL
    main_page_button = InlineKeyboardButton(
        text='🏠 Главная',
        web_app=WebAppInfo(url=create_url('/'))
    )
    sales_button = InlineKeyboardButton(
        text='💸 Продажи',
        web_app=WebAppInfo(url=create_url('/sales/'))
    )
    returns_button = InlineKeyboardButton(
        text='🔄 Возвраты',
        web_app=WebAppInfo(url=create_url('/returns/'))
    )
    inventory_button = InlineKeyboardButton(
        text='📈 Оприходование',
        web_app=WebAppInfo(url=create_url('/inventory/'))
    )
    write_off_button = InlineKeyboardButton(
        text='📉 Списание товара',
        web_app=WebAppInfo(url=create_url('/write-offs/'))
    )
    preorders_button = InlineKeyboardButton(
        text='📋 Предзаказы',
        web_app=WebAppInfo(url=create_url('/preorders/'))
    )
    reports_button = InlineKeyboardButton(
        text='📊 Отчеты',
        web_app=WebAppInfo(url=create_url('/reports/'))
    )

    # Создаем список кнопок
    inline_keyboard = [
        [main_page_button],
        [sales_button],
        [returns_button],
        [inventory_button],
        [write_off_button],
        [preorders_button],
        [reports_button]
    ]

    # Возвращаем объект инлайн-клавиатуры
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

