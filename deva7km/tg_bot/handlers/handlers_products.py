from aiogram import Router
from aiogram.types import CallbackQuery
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_return_for_products
from tg_bot.services.products import get_modifications_info

router: Router = Router()


# обработчик который бы отлавливал callback_query=products
@router.callback_query(lambda callback: 'products' == callback.data)
async def process_callback_query_products(callback: CallbackQuery):
    kb = await create_inline_kb_main_sku()
    await callback.message.answer('Выберите товар 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=sku
@router.callback_query(lambda callback: '_main_sku' in callback.data)
async def process_callback_query_sku(callback: CallbackQuery):
    kb = await create_inline_kb_return_for_products()
    # получаем sku из callback_data обрезанием _main_sku
    sku = callback.data.split("_")[0]
    # вызываем функцию для отображения модификаций товара
    string = await get_modifications_info(sku)
    await callback.message.answer(string, reply_markup=kb)
    await callback.answer()
