from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from deva7km.settings import BOT_TOKEN
from tg_bot.FSM.fsm import InventoryStates
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_modifications, \
    create_inline_kb_numbers, create_main_menu_kb
from tg_bot.services.inventory import create_inventory
from tg_bot.services.products import get_large_image_url_input_file
from tg_bot.services.users import admin_access_control_decorator, get_or_create_telegram_user

router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# Обработчик команды /sell
@router.message(Command('inventory'))
@admin_access_control_decorator(access='admin')
async def command_sell_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(InventoryStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='inventory')
    await message.answer('Выберите товар для оприходования 👇', reply_markup=kb)


# обработчик который бы отлавливал callback_query=sell
@router.callback_query(lambda callback: 'inventory' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_sell(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(InventoryStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='inventory')
    await callback.message.answer('Выберите товар для оприходования 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=sku для inventory и выводил кнопки с модификациями конкретного товара
@router.callback_query(StateFilter(InventoryStates.choosingSKU))
@admin_access_control_decorator(access='admin')
async def process_callback_query_sku(callback: CallbackQuery, state: FSMContext):
    if '_main_sku_inventory' in callback.data:
        sku = callback.data.split("_")[0]
        await state.set_state(InventoryStates.choosingModification)
        await state.update_data(choosingSKU=sku)
        user_data = await state.get_data()
        kb = await create_inline_kb_modifications(sku, callback='inventory')
        await callback.message.answer(f'Вы выбрали для оприходования модель ➡️ {hbold(user_data["choosingSKU"])}\nвыберите '
                                      f'модификацию 👇', reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('выберите основной товар или нажмите отмена! 👆')
        await callback.answer()


# обработчик который бы отлавливал callback_query=modifications для inventory и выводил количество
# товара на остатке, а также указать сколько товара нужно продать
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
                             caption=f'Вы выбрали для оприходования модификацию ➡️ {hbold(user_data["choosingModification"])}\n'
                                     f'Введите количество товара для оприходования:', reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('выберите модификацию или нажмите отмена! 👆')
        await callback.answer()


# обработчик который бы отлавливал callback_query=numbers для inventory
@router.callback_query(StateFilter(InventoryStates.enteringQuantity))
@admin_access_control_decorator(access='admin')
async def process_callback_query_numbers(callback: CallbackQuery, state: FSMContext):
    if callback.data.isdigit():
        await state.set_state(InventoryStates.finish)
        await state.update_data(enteringQuantity=callback.data)
        # данные о пользователе
        user_id = callback.from_user.id
        user_name = callback.from_user.username
        user_first_name = callback.from_user.first_name
        user_last_name = callback.from_user.last_name
        telegram_user = await get_or_create_telegram_user(user_id, user_name, user_first_name, user_last_name)
        user_data = await state.get_data()
        # Создание возврата
        inventory = await create_inventory(user_data, telegram_user)
        if inventory:
            await state.clear()
            kb = await create_main_menu_kb()
            custom_sku = user_data['choosingModification']
            thumbnail_input_file = await get_large_image_url_input_file(custom_sku)
            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=thumbnail_input_file,
                                 caption=f'✅ Оприходование успешно проведено на сумму {inventory.total_amount}\n\n'
                                         f'вы оприходовали {user_data["choosingModification"]}\n'
                                         f'в количестве {user_data["enteringQuantity"]}шт.\n', reply_markup=kb)
            await callback.answer()
        else:
            await callback.message.answer('⛔️ ProductModification не найден')
