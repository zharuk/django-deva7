from asyncio import sleep

from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from django.utils import asyncio

from deva7km.settings import BOT_TOKEN
from tg_bot.keyboards.keyboards import create_report_kb
from tg_bot.services.reports import generate_sales_report_by_day, generate_sales_report_by_yesterday, \
    generate_sales_report_by_week, generate_sales_report_by_month, generate_sales_report_by_year, get_total_stock
from tg_bot.services.users import admin_access_control_decorator

router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# Обработчик команды /report
@router.message(Command('report'))
@admin_access_control_decorator(access='seller')
async def command_report_handler(message: Message, state: FSMContext):
    await state.clear()
    kb = await create_report_kb()
    await message.answer('Выберите за какой период отчет 👇', reply_markup=kb)


# обработчик который бы отлавливал callback_query=report
@router.callback_query(lambda callback: 'report' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_sell(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    kb = await create_report_kb()
    await callback.message.answer('Выберите за какой период отчет 👇', reply_markup=kb)
    await callback.answer()


# обработка отчетов
@router.callback_query(lambda callback: callback.data in ['today', 'yesterday', 'week', 'month', 'year', 'total_stock'])
@admin_access_control_decorator(access='seller')
async def process_callback_query_sell(callback: CallbackQuery):
    query_data = callback.data

    if query_data == 'total_stock':
        report_functions = get_total_stock
    else:
        time_functions = {
            'today': generate_sales_report_by_day,
            'yesterday': generate_sales_report_by_yesterday,
            'week': generate_sales_report_by_week,
            'month': generate_sales_report_by_month,
            'year': generate_sales_report_by_year,
        }
        report_functions = time_functions.get(query_data)

    if report_functions:
        report = await report_functions()
        kb = await create_report_kb()
        max_length = 4096  # Максимальная длина сообщения Telegram

        # Разделение текста на части
        parts = [report[i:i + max_length] for i in range(0, len(report), max_length)]

        # Отправка каждой части поочередно
        for part in parts:
            await callback.message.answer(part)
            await sleep(1)  # добавляем паузу в 1 секунду

        await callback.message.answer('\nОтчет закончен', reply_markup=kb)
        await callback.answer()
