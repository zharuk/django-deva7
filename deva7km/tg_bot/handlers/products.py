from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_return
from tg_bot.services.products import get_modifications_info, send_modification_photos
from tg_bot.services.users import access_control_decorator

router: Router = Router()


# Обработчик команды /products
@router.message(Command('products'))
@access_control_decorator
async def command_products_handler(message: Message) -> None:
    kb = await create_inline_kb_main_sku('products')
    await message.answer('Выберите товар для просмотра 👇', reply_markup=kb)


# обработчик который бы отлавливал callback_query=products
@router.callback_query(lambda callback: 'products' == callback.data)
@access_control_decorator
async def process_callback_query_products(callback: CallbackQuery):
    kb = await create_inline_kb_main_sku('products')
    await callback.message.answer('Выберите товар для просмотра 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=sku для products
@router.callback_query(lambda callback: '_main_sku_products' in callback.data)
@access_control_decorator
async def process_callback_query_sku(callback: CallbackQuery):
    kb = await create_inline_kb_return('products')
    # получаем sku из callback_data обрезанием _main_sku
    sku = callback.data.split("_")[0]
    # вызываем функцию для отображения модификаций товара
    string = await get_modifications_info(sku)
    # Отправляем фотографии модификаций в чат
    await send_modification_photos(callback.from_user.id, sku)
    await callback.message.answer(string, reply_markup=kb)
    await callback.answer()
