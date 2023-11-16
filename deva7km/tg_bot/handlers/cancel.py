from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from tg_bot.keyboards.keyboards import create_main_menu_kb
from tg_bot.services.users import admin_access_control_decorator

router: Router = Router()


# Обработчик команды /start с приветствием
@router.message(Command('cancel'))
@admin_access_control_decorator(access='seller')
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    kb = await create_main_menu_kb()
    await state.clear()
    await message.answer(f"Вы отменили операцию!что делаем?", reply_markup=kb)


# Обработчик callback start с приветствием
@router.callback_query(lambda callback: 'cancel' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_cancel(callback: CallbackQuery, state: FSMContext):
    kb = await create_main_menu_kb()
    await state.clear()
    await callback.message.answer(f"Вы отменили операцию!что делаем?", reply_markup=kb)
    await callback.answer()
