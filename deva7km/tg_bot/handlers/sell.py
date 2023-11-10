from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from tg_bot.FSM.sell import SellStates
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_modifications, \
    create_inline_kb_numbers, create_payment_type_keyboard, create_inline_kb_cancel, create_main_menu_kb
from tg_bot.services.sells import check_stock_status, create_sale, get_product_modification
from tg_bot.services.users import access_control_decorator, get_or_create_telegram_user

router: Router = Router()


# Обработчик команды /sell
@router.message(Command('sell'))
@access_control_decorator
async def command_sell_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(SellStates.choosingSKU)
    kb = await create_inline_kb_main_sku('sell')
    await message.answer('Выберите товар для продажи 👇', reply_markup=kb)


# обработчик который бы отлавливал callback_query=sell
@router.callback_query(lambda callback: 'sell' == callback.data)
@access_control_decorator
async def process_callback_query_sell(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(SellStates.choosingSKU)
    kb = await create_inline_kb_main_sku('sell')
    await callback.message.answer('Выберите товар для продажи 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=sku для sell и выводил кнопки с модификациями конкретного товара
@router.callback_query(StateFilter(SellStates.choosingSKU))
@access_control_decorator
async def process_callback_query_sku(callback: CallbackQuery, state: FSMContext):
    if '_main_sku_sell' in callback.data:
        sku = callback.data.split("_")[0]
        await state.set_state(SellStates.choosingModification)
        await state.update_data(choosingSKU=sku)
        kb = await create_inline_kb_modifications(sku, 'sell')
        await callback.message.answer('выберите модификацию 👇', reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('выберите основной товар или нажмите отмена! 👆')
        await callback.answer()


# обработчик который бы отлавливал callback_query=modifications для sell и выводил количество
# товара на остатке, а также указать сколько товара нужно продать
@router.callback_query(StateFilter(SellStates.choosingModification))
@access_control_decorator
async def process_callback_query_modifications(callback: CallbackQuery, state: FSMContext):
    if '_modification_sell' in callback.data:
        custom_sku = callback.data.split("_")[0]
        if await check_stock_status(custom_sku):
            await state.set_state(SellStates.enteringQuantity)
            await state.update_data(choosingModification=custom_sku)
            kb = await create_inline_kb_numbers()
            await callback.message.answer(f"Введите количество товара для продажи:", reply_markup=kb)
            await callback.answer()
        else:
            await callback.message.answer('⛔️ Товара на складе нет!')
            await callback.answer()
    else:
        await callback.message.answer('выберите модификацию или нажмите отмена! 👆')
        await callback.answer()


# обработчик который бы отлавливал callback_query=numbers для sell и выводил клавиатуру с кнопками "нал" или
# "безнал"
@router.callback_query(StateFilter(SellStates.enteringQuantity))
@access_control_decorator
async def process_callback_query_numbers(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    modification = await get_product_modification(user_data['choosingModification'])
    stock = modification.stock
    print(stock)
    print(modification)
    if callback.data.isdigit():
        if stock >= int(callback.data):
            await state.set_state(SellStates.choosingPayment)
            await state.update_data(enteringQuantity=callback.data[0])
            kb = await create_payment_type_keyboard()
            await callback.message.answer('Выберите способ оплаты 👇', reply_markup=kb)
            await callback.answer()
        else:
            await callback.message.answer(f'⛔️ В наличии только {stock}шт. вы хотите продать {callback.data}шт.')
            await callback.answer()
    else:
        await callback.message.answer('Выберите количество товара или нажмите отмена! 👆')
        await callback.answer()


@router.callback_query(StateFilter(SellStates.choosingPayment))
@access_control_decorator
async def process_callback_query_finish(callback: CallbackQuery, state: FSMContext):
    if callback.data in ['cash', 'non_cash']:
        # данные о пользователе
        user_id = callback.from_user.id
        user_name = callback.from_user.username
        user_first_name = callback.from_user.first_name
        user_last_name = callback.from_user.last_name
        telegram_user = await get_or_create_telegram_user(user_id, user_name, user_first_name, user_last_name)
        await state.set_state(SellStates.finish)
        await state.update_data(choosingPayment=callback.data)
        user_data = await state.get_data()
        # Создание продажи
        sale = await create_sale(user_data, telegram_user)
        # Создание клавиатуры для ответа
        kb = await create_main_menu_kb()
        if sale:
            await state.clear()
            payment_types = {
                'cash': 'наличная 💵',
                'non_cash': 'безналичная 💳',
            }
            await callback.message.answer(f'✅ Продажа успешно проведена на сумму {sale.total_amount}\n\n'
                                          f'вы продали {user_data["choosingModification"]}\n'
                                          f'в количестве {user_data["enteringQuantity"]}шт.\n'
                                          f'тип оплаты - {payment_types[user_data["choosingPayment"]]}', reply_markup=kb)
            await callback.answer()
        else:
            await callback.message.answer('⛔️ ProductModification не найден')
    else:
        await callback.message.answer('Выберите тип продажи или нажмите отмена! 👆')
