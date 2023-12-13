from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from deva7km.settings import BOT_TOKEN
from tg_bot.keyboards.keyboards import create_report_kb
from tg_bot.services.reports import generate_sales_report_by_day, generate_sales_report_by_yesterday, \
    generate_sales_report_by_week, generate_sales_report_by_month, generate_sales_report_by_year, get_total_stock
from tg_bot.services.users import admin_access_control_decorator

router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# Обработчик команды /report
@router.message(Command('report'))
@admin_access_control_decorator(access='admin')
async def command_report_handler(message: Message, state: FSMContext):
    await state.clear()
    kb = await create_report_kb()
    await message.answer('Выберите за какой период отчет 👇', reply_markup=kb)


# обработчик который бы отлавливал callback_query=report
@router.callback_query(lambda callback: 'report' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_sell(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    kb = await create_report_kb()
    await callback.message.answer('Выберите за какой период отчет 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=today
@router.callback_query(lambda callback: 'today' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_sell(callback: CallbackQuery):
    report = await generate_sales_report_by_day()
    kb = await create_report_kb()
    max_length = 4096  # Максимальная длина сообщения Telegram

    # Разделение текста на части
    parts = [report[i:i + max_length] for i in range(0, len(report), max_length)]

    # Отправка каждой части поочередно
    for part in parts:
        await callback.message.answer(part)

    await callback.message.answer('\nОтчет закончен', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=yesterday
@router.callback_query(lambda callback: 'yesterday' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_sell(callback: CallbackQuery):
    report = await generate_sales_report_by_yesterday()
    kb = await create_report_kb()
    max_length = 4096  # Максимальная длина сообщения Telegram

    # Разделение текста на части
    parts = [report[i:i + max_length] for i in range(0, len(report), max_length)]

    # Отправка каждой части поочередно
    for part in parts:
        await callback.message.answer(part)

    await callback.message.answer('\nОтчет закончен', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=week
@router.callback_query(lambda callback: 'week' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_sell(callback: CallbackQuery):
    report = await generate_sales_report_by_week()
    kb = await create_report_kb()
    max_length = 4096  # Максимальная длина сообщения Telegram

    # Разделение текста на части
    parts = [report[i:i + max_length] for i in range(0, len(report), max_length)]

    # Отправка каждой части поочередно
    for part in parts:
        await callback.message.answer(part)

    await callback.message.answer('\nОтчет закончен', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=month
@router.callback_query(lambda callback: 'month' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_sell(callback: CallbackQuery):
    report = await generate_sales_report_by_month()
    kb = await create_report_kb()
    max_length = 4096  # Максимальная длина сообщения Telegram

    # Разделение текста на части
    parts = [report[i:i + max_length] for i in range(0, len(report), max_length)]

    # Отправка каждой части поочередно
    for part in parts:
        await callback.message.answer(part)

    await callback.message.answer('\nОтчет закончен', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=year
@router.callback_query(lambda callback: 'year' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_sell(callback: CallbackQuery):
    report = await generate_sales_report_by_year()
    kb = await create_report_kb()
    max_length = 4096  # Максимальная длина сообщения Telegram

    # Разделение текста на части
    parts = [report[i:i + max_length] for i in range(0, len(report), max_length)]

    # Отправка каждой части поочередно
    for part in parts:
        await callback.message.answer(part)

    await callback.message.answer('\nОтчет закончен', reply_markup=kb)
    await callback.answer()


#  обработчик который бы отлавливал callback_query=total_stock
@router.callback_query(lambda callback: 'total_stock' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query(callback: CallbackQuery):
    report = await get_total_stock()
    kb = await create_report_kb()

    max_length = 4096  # Максимальная длина сообщения Telegram

    # Разделение текста на части
    parts = [report[i:i + max_length] for i in range(0, len(report), max_length)]

    # Отправка каждой части поочередно
    for part in parts:
        await callback.message.answer(part)

    await callback.message.answer('\nОтчет закончен', reply_markup=kb)
    await callback.answer()
