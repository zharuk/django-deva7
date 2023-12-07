from aiogram import Router, Bot
from aiogram.enums import InputMediaType
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, InputMediaPhoto, InputFile
from aiogram.utils.media_group import MediaGroupBuilder

from deva7km.settings import BOT_TOKEN
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_return
from tg_bot.services.products import get_modifications_info, get_first_image_for_product
from tg_bot.services.users import admin_access_control_decorator

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


# обработчик который бы отлавливал callback_query=sku для products
@router.callback_query(lambda callback: '_main_sku_products' in callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_sku(callback: CallbackQuery):
    kb = await create_inline_kb_return('products')
    # получаем sku из callback_data обрезанием _main_sku
    sku = callback.data.split("_")[0]
    # вызываем функцию для отображения модификаций товара
    string = await get_modifications_info(sku)
    # Отправляем фотографии модификаций в чат
    image = await get_first_image_for_product(sku)
    if image:
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=image,
                             caption=string, reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer(string, reply_markup=kb)
        await callback.answer()
