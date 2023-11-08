from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku
from catalog.models import Product

router: Router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    kb = await create_inline_kb_main_sku()
    await message.answer("Вот ваша клавиатура:", reply_markup=kb)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message(Command(commands='show'))
async def show_products(message: types.Message):
    products = await sync_to_async(list)(Product.objects.all())
    product_list = "\n".join([f"{product.title} {product.sku} ({await sync_to_async(product.get_total_stock)()} шт.): "
                              f"{product.price} {product.currency}" for product in products])
    await message.answer(product_list)
