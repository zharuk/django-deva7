import datetime
import locale
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from tg_bot.keyboards.keyboards import create_main_menu_kb
from tg_bot.services.users import get_or_create_telegram_user, access_control_decorator

router: Router = Router()


# Обработчик команды /start с приветствием
@router.message(CommandStart())
@access_control_decorator
async def command_start_handler(message: Message) -> None:
    # данные о пользователе
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    # проверка наличия пользователя в бд и если нет то создать
    await get_or_create_telegram_user(user_id, user_name, user_first_name, user_last_name)
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
@access_control_decorator
async def process_callback_query_start(callback: CallbackQuery):
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
