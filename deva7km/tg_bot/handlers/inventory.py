from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async

from deva7km.settings import BOT_TOKEN
from tg_bot.FSM.fsm import InventoryStates
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_modifications, \
    create_inline_kb_numbers, create_main_menu_kb, create_inline_kb_add_more
from tg_bot.services.inventory import create_inventory
from tg_bot.services.products import get_large_image_url_input_file
from tg_bot.services.users import admin_access_control_decorator, get_or_create_telegram_user

router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# Обработчик команды /inventory
@router.message(Command('inventory'))
@admin_access_control_decorator(access='admin')
async def command_inventory_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(InventoryStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='inventory')
    await message.answer('Выберите товар для оприходования 👇', reply_markup=kb)


# обработчик callback_query=inventory
@router.callback_query(lambda callback: 'inventory' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_inventory(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(InventoryStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='inventory')
    await callback.message.answer('Выберите товар для оприходования 👇', reply_markup=kb)
    await callback.answer()


# обработчик callback_query=sku для inventory
@router.callback_query(StateFilter(InventoryStates.choosingSKU))
@admin_access_control_decorator(access='admin')
async def process_callback_query_sku(callback: CallbackQuery, state: FSMContext):
    if '_main_sku_inventory' in callback.data:
        sku = callback.data.split("_")[0]
        await state.set_state(InventoryStates.choosingModification)
        await state.update_data(choosingSKU=sku)
        user_data = await state.get_data()
        kb = await create_inline_kb_modifications(sku, callback='inventory')
        await callback.message.answer(
            f'Вы выбрали для оприходования модель ➡️ {hbold(user_data["choosingSKU"])}\nвыберите модификацию 👇',
            reply_markup=kb
        )
        await callback.answer()
    else:
        await callback.message.answer('Выберите основной товар или нажмите отмена! 👆')
        await callback.answer()


# обработчик callback_query=modifications для inventory
@router.callback_query(StateFilter(InventoryStates.choosingModification))
@admin_access_control_decorator(access='admin')
async def process_callback_query_modifications(callback: CallbackQuery, state: FSMContext):
    if '_modification_inventory' in callback.data:
        custom_sku = callback.data.split("_")[0]
        await state.set_state(InventoryStates.enteringQuantity)
        await state.update_data(choosingModification=custom_sku)
        user_data = await state.get_data()
        custom_sku = user_data['choosingModification']
        thumbnail_input_file = await get_large_image_url_input_file(custom_sku)
        kb = await create_inline_kb_numbers(quantity=50)
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=thumbnail_input_file,
                             caption=f'Вы выбрали для оприходования модификацию ➡️ {hbold(user_data["choosingModification"])}\nВведите количество товара для оприходования:',
                             reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('Выберите модификацию или нажмите отмена! 👆')
        await callback.answer()


# обработчик для добавления еще товара
@router.callback_query(StateFilter(InventoryStates.enteringQuantity),
                       lambda callback: callback.data not in ['add_more', 'finish'])
@admin_access_control_decorator(access='admin')
async def process_callback_query_numbers(callback: CallbackQuery, state: FSMContext):
    if not callback.data.isdigit():
        await callback.message.answer('Некорректное количество. Пожалуйста, выберите правильное количество товара.')
        await callback.answer()
        return

    await state.update_data(enteringQuantity=callback.data)
    user_data = await state.get_data()
    product_info = {
        'choosingSKU': user_data['choosingSKU'],
        'choosingModification': user_data['choosingModification'],
        'enteringQuantity': user_data['enteringQuantity'],
    }
    if 'products_list' in user_data:
        user_data['products_list'].append(product_info)
        await state.update_data(user_data)
    else:
        user_data['products_list'] = [product_info]
        await state.update_data(user_data)

    products_text = ""
    for product in user_data['products_list']:
        custom_sku = product['choosingModification']
        quantity = product['enteringQuantity']
        products_text += f'{custom_sku} - {quantity}шт.\n'
    kb = await create_inline_kb_add_more()

    await callback.message.answer(
        f'Вы выбрали для оприходования ➡️\n\n{products_text}\nвыберите еще товар или завершите приход', reply_markup=kb)
    await callback.answer()


# обработчик для добавления еще товара
@router.callback_query(StateFilter(InventoryStates.enteringQuantity), lambda callback: 'add_more' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_add_more(callback: CallbackQuery, state: FSMContext):
    await state.set_state(InventoryStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='inventory')
    await callback.message.answer('Выберите товар для оприходования 👇', reply_markup=kb)
    await callback.answer()


# обработчик для завершения оприходования
@router.callback_query(StateFilter(InventoryStates.enteringQuantity), lambda callback: 'finish' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_finish_button(callback: CallbackQuery, state: FSMContext):
    await state.set_state(InventoryStates.finish)
    await process_callback_query_finish_inventory(callback, state)


# обработчик завершения оприходования
@router.callback_query(StateFilter(InventoryStates.finish), lambda callback: 'finish' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_finish_inventory(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    user_id = callback.from_user.id
    user_name = callback.from_user.username
    user_first_name = callback.from_user.first_name
    user_last_name = callback.from_user.last_name
    telegram_user = await get_or_create_telegram_user(user_id, user_name, user_first_name, user_last_name)

    products_text = ""
    for product in user_data['products_list']:
        custom_sku = product['choosingModification']
        quantity = product['enteringQuantity']
        products_text += f'{custom_sku} - {quantity}шт.\n'

    inventory = await create_inventory(user_data, telegram_user)
    if inventory is None:
        await callback.message.answer(
            '❌ Произошла ошибка при проведении оприходования. Пожалуйста, попробуйте еще раз.')
        await state.clear()
        await callback.answer()
        return

    kb = await create_main_menu_kb()
    await callback.message.answer(
        f'✅ Оприходование успешно проведено на сумму {await sync_to_async(inventory.calculate_total_amount)()}грн.\n\n'
        f'Список товаров для оприходования: \n\n{products_text}', reply_markup=kb)
    await state.clear()
    await callback.answer()
