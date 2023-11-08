import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async

from bot.keyboards.keyboards import create_inline_kb_main_sku
from bot.keyboards.menu import set_main_menu
from catalog.models import Product
from aiogram.fsm.storage.redis import RedisStorage, Redis
from deva7km.settings import BOT_TOKEN

# Bot token can be obtained via https://t.me/BotFather
TOKEN = BOT_TOKEN

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    kb = await create_inline_kb_main_sku()
    await message.answer("Вот ваша клавиатура:", reply_markup=kb)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message(Command(commands='show'))
async def show_products(message: types.Message):
    products = await sync_to_async(list)(Product.objects.all())
    product_list = "\n".join([f"{product.title} {product.sku} ({await sync_to_async(product.get_total_stock)()} шт.): "
                              f"{product.price} {product.currency}" for product in products])
    await message.answer(product_list)



@dp.message()
async def echo_handler(message: types.Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")


# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')
    # # Создаем подключение к Redis состояний и хранилищу
    redis: Redis = Redis(host='localhost')
    # # Инициализируем хранилище (создаем экземпляр класса RedisStorage)
    storage: RedisStorage = RedisStorage(redis=redis)

    # Инициализируем бот и диспетчер и сервер
    bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage, bot=bot)

    # Настраиваем меню
    await set_main_menu(bot)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())