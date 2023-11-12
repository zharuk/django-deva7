from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from deva7km.settings import BOT_TOKEN
from tg_bot.FSM.fsm import SellStates, ReturnStates
from tg_bot.keyboards.keyboards import create_report_kb
from tg_bot.services.reports import generate_sales_report_by_day

from tg_bot.services.users import access_control_decorator

router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# Обработчик команды /report
@router.message(Command('report'))
@access_control_decorator
async def command_report_handler(message: Message, state: FSMContext):
    await state.clear()
    kb = await create_report_kb()
    await message.answer('Выберите за какой период отчет 👇', reply_markup=kb)


# обработчик который бы отлавливал callback_query=report
@router.callback_query(lambda callback: 'report' == callback.data)
@access_control_decorator
async def process_callback_query_sell(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    kb = await create_report_kb()
    await callback.message.answer('Выберите за какой период отчет 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=today
@router.callback_query(lambda callback: 'today' == callback.data)
@access_control_decorator
async def process_callback_query_sell(callback: CallbackQuery):
    report = await generate_sales_report_by_day()
    await callback.message.answer(report)
    await callback.answer()


# обработчик который бы отлавливал callback_query=yesterday
@router.callback_query(lambda callback: 'yesterday' == callback.data)
@access_control_decorator
async def process_callback_query_sell(callback: CallbackQuery):
    await callback.message.answer('в разработке')
    await callback.answer()


# обработчик который бы отлавливал callback_query=week
@router.callback_query(lambda callback: 'week' == callback.data)
@access_control_decorator
async def process_callback_query_sell(callback: CallbackQuery):
    await callback.message.answer('в разработке')
    await callback.answer()


# обработчик который бы отлавливал callback_query=month
@router.callback_query(lambda callback: 'month' == callback.data)
@access_control_decorator
async def process_callback_query_sell(callback: CallbackQuery):
    await callback.message.answer('в разработке')
    await callback.answer()


# обработчик который бы отлавливал callback_query=year
@router.callback_query(lambda callback: 'year' == callback.data)
@access_control_decorator
async def process_callback_query_sell(callback: CallbackQuery):
    await callback.message.answer('в разработке')
    await callback.answer()