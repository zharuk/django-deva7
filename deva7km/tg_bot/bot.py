import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage, Redis
from deva7km.settings import BOT_TOKEN
from tg_bot.handlers import start, products, sell, cancel
from tg_bot.keyboards.menu import set_main_menu


# Токен бота
TOKEN = BOT_TOKEN
# Инициализируем логгер
logger = logging.getLogger(__name__)
# Конфигурируем логирование
logging.basicConfig(
    level=logging.INFO,
    format='%(filename)s:%(lineno)d #%(levelname)-8s ''[%(asctime)s] - %(name)s - %(message)s')
# Выводим в консоль информацию о начале запуска бота
logger.info('Starting tg_bot')
# # Создаем подключение к Redis состояний и хранилищу
redis: Redis = Redis(host='localhost')
# # Инициализируем хранилище (создаем экземпляр класса RedisStorage)
storage: RedisStorage = RedisStorage(redis=redis)
# Инициализируем бот и диспетчер и сервер
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher(storage=storage, bot=bot)


# Функция конфигурирования и запуска бота
async def main():
    # Настраиваем меню
    await set_main_menu(bot)
    # Регистрируем роутеры в диспетчере
    dp.include_router(cancel.router)
    dp.include_router(start.router)
    dp.include_router(products.router)
    dp.include_router(sell.router)
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
