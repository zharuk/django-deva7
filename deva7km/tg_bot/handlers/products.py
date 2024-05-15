from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, URLInputFile
from deva7km.settings import BOT_TOKEN
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_return
from tg_bot.services.products import get_modifications_info, get_collage_image_for_product
from tg_bot.services.users import admin_access_control_decorator
import re

router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# Обработчик команды /products
@router.message(Command('products'))
@admin_access_control_decorator(access='seller')
async def command_products_handler(message: Message) -> None:
    kb = await create_inline_kb_main_sku(callback='products')
    await message.answer('Выберите товар для просмотра 👇', reply_markup=kb)


# обработчик который бы отлавливал callback_query=products
@router.callback_query(lambda callback: 'products' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_products(callback: CallbackQuery):
    kb = await create_inline_kb_main_sku(callback='products')
    await callback.message.answer('Выберите товар для просмотра 👇', reply_markup=kb)
    await callback.answer()


# Хендлер для кнопки Назад
@router.callback_query(lambda callback: callback.data.startswith('prev_'))
@admin_access_control_decorator(access='seller')
async def process_callback_query_prev(callback: CallbackQuery):
    match = re.match(r'prev_(\w+)_([0-9]+)', callback.data)
    if match:
        callback_name, page = match.groups()
        page = int(page) - 1 if int(page) > 1 else 1
        kb = await create_inline_kb_main_sku(callback_name, page)
        await callback.message.edit_reply_markup(reply_markup=kb)
        await callback.answer()
    else:
        # Обработка ситуации, когда формат не соответствует ожидаемому
        print(f"Некорректный формат данных в callback.data: {callback.data}")


# Хендлер для кнопки Вперед
@router.callback_query(lambda callback: callback.data.startswith('next_'))
@admin_access_control_decorator(access='seller')
async def process_callback_query_next(callback: CallbackQuery):
    match = re.match(r'next_(\w+)_([0-9]+)', callback.data)
    if match:
        callback_name, page = match.groups()
        page = int(page) + 1
        kb = await create_inline_kb_main_sku(callback_name, page)
        await callback.message.edit_reply_markup(reply_markup=kb)
        await callback.answer()
    else:
        # Обработка ситуации, когда формат не соответствует ожидаемому
        print(f"Некорректный формат данных в callback.data: {callback.data}")


# обработчик который бы отлавливал callback_query=sku для products
@router.callback_query(lambda callback: '_main_sku_products' in callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_sku(callback: CallbackQuery):
    kb = await create_inline_kb_return('products')
    # получаем sku из callback_data обрезанием _main_sku
    sku = callback.data.split("_")[0]
    # вызываем функцию для отображения модификаций товара
    string = await get_modifications_info(sku)
    # Отправляем изображение коллажа в чат
    collage_image_url = await get_collage_image_for_product(sku)
    if collage_image_url:
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=URLInputFile(collage_image_url),
                             caption=string, reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer(string, reply_markup=kb)
        await callback.answer()
