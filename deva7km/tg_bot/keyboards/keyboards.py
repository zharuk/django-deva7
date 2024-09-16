from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from deva7km import settings


# клавиатура основного меню
async def create_main_menu_kb(telegram_id=None) -> ReplyKeyboardMarkup:
    # Создаем базовые URL
    base_url = f'{settings.BASE_URL}/seller_cabinet'

    # Обновляем URL для Web App, если telegram_id предоставлен
    def create_url(path):
        url = f'{base_url}{path}'
        if telegram_id:
            url += f'?telegram_id={telegram_id}'
        return url

    # Создаем кнопки с обновленными URL
    main_page_button = KeyboardButton(
        text='🏠 Открыть кабинет продавца 👈',
        web_app=WebAppInfo(url=create_url('/'))
    )

    # Создаем список кнопок
    keyboard = [
        [main_page_button],
    ]

    # Возвращаем объект инлайн-клавиатуры
    return ReplyKeyboardMarkup(keyboard=keyboard)

