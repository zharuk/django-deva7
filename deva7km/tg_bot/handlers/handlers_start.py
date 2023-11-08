import datetime
import locale

from aiogram import types, Router
from aiogram.filters import CommandStart, Command
from aiogram.handlers import callback_query
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from tg_bot.keyboards.keyboards import create_main_menu_kb


router: Router = Router()


# Обработчик команды /start с приветствием
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    # Установите русскую локаль
    locale.setlocale(locale.LC_TIME, 'ru_RU')
    # Получить текущую дату и день недели
    current_date = datetime.datetime.now()
    date_str = current_date.strftime("%d.%m.%Y")
    day_of_week = current_date.strftime("%A")
    kb = await create_main_menu_kb()
    await message.answer(
        f"Привет {hbold(message.from_user.full_name)}!\nСегодня {date_str} {hbold(day_of_week)}, что делаем?",
        reply_markup=kb)


# Обработчик callback start с приветствием
@router.callback_query(lambda callback: 'start' == callback.data)
async def command_start_handler(callback: CallbackQuery):
    # Установите русскую локаль
    locale.setlocale(locale.LC_TIME, 'ru_RU')
    # Получить текущую дату и день недели
    current_date = datetime.datetime.now()
    date_str = current_date.strftime("%d.%m.%Y")
    day_of_week = current_date.strftime("%A")
    kb = await create_main_menu_kb()
    await callback.message.answer(
        f"Привет {hbold(callback.from_user.full_name)}!\nСегодня {date_str} {hbold(day_of_week)}, что делаем?",
        reply_markup=kb)
    await callback.answer()

