import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from deva7km.settings import BOT_TOKEN
from tg_bot.handlers import start, any_message

# Токен бота
TOKEN = BOT_TOKEN

# Инициализируем бот и диспетчер и сервер
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')
dp: Dispatcher = Dispatcher(bot=bot)


# Устанавливаем главное меню команд
async def set_main_menu(bot: Bot):
    commands = [
        BotCommand(command='/start', description='Запуск бота')
    ]
    await bot.set_my_commands(commands)


# Функция конфигурирования и запуска бота
async def main():
    # Настраиваем меню
    await set_main_menu(bot)
    # Регистрируем роутеры в диспетчере
    dp.include_router(start.router)
    dp.include_router(any_message.router)
    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
