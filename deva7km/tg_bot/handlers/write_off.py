from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from deva7km.settings import BOT_TOKEN
from tg_bot.FSM.fsm import WriteOffStates
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_modifications, \
    create_inline_kb_numbers, create_main_menu_kb
from tg_bot.services.products import get_large_image_url_input_file
from tg_bot.services.sells import get_product_modification
from tg_bot.services.users import admin_access_control_decorator, get_or_create_telegram_user
from tg_bot.services.write_off import create_write_off

router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# Обработчик команды /write_off
@router.message(Command('write_off'))
@admin_access_control_decorator(access='admin')
async def command_sell_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(WriteOffStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='write_off')
    await message.answer('Выберите товар для списания 👇', reply_markup=kb)


# обработчик который бы отлавливал callback_query=write_off
@router.callback_query(lambda callback: 'write_off' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_sell(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(WriteOffStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='write_off')
    await callback.message.answer('Выберите товар для списания 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=sku для write_off и выводил кнопки с модификациями конкретного товара
@router.callback_query(StateFilter(WriteOffStates.choosingSKU))
@admin_access_control_decorator(access='admin')
async def process_callback_query_sku(callback: CallbackQuery, state: FSMContext):
    if '_main_sku_write_off' in callback.data:
        sku = callback.data.split("_")[0]
        await state.set_state(WriteOffStates.choosingModification)
        await state.update_data(choosingSKU=sku)
        user_data = await state.get_data()
        kb = await create_inline_kb_modifications(sku, callback='write_off')
        await callback.message.answer(f'Вы выбрали для списания модель ➡️ {hbold(user_data["choosingSKU"])}\nвыберите '
                                      f'модификацию 👇', reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('выберите основной товар или нажмите отмена! 👆')
        await callback.answer()


# обработчик который бы отлавливал callback_query=modifications для write_off и выводил количество
# товара на остатке, а также указать сколько товара нужно списать
@router.callback_query(StateFilter(WriteOffStates.choosingModification))
@admin_access_control_decorator(access='admin')
async def process_callback_query_modifications(callback: CallbackQuery, state: FSMContext):
    if '_modification_write_off' in callback.data:
        custom_sku = callback.data.split("_")[0]
        await state.set_state(WriteOffStates.enteringQuantity)
        await state.update_data(choosingModification=custom_sku)
        user_data = await state.get_data()
        custom_sku = user_data['choosingModification']
        thumbnail_input_file = await get_large_image_url_input_file(custom_sku)
        kb = await create_inline_kb_numbers(quantity=10)
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=thumbnail_input_file,
                             caption=f'Вы выбрали для списания модификацию ➡️ {hbold(user_data["choosingModification"])}\n'
                                     f'Введите количество товара для списания:', reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('выберите модификацию или нажмите отмена! 👆')
        await callback.answer()


# обработчик который бы отлавливал callback_query=numbers для write_off и проверял бы на введенное количество
# пользователем
@router.callback_query(StateFilter(WriteOffStates.enteringQuantity))
@admin_access_control_decorator(access='admin')
async def process_callback_query_numbers(callback: CallbackQuery, state: FSMContext):
    if callback.data.isdigit():
        user_data = await state.get_data()
        modification = await get_product_modification(user_data['choosingModification'])
        stock = modification.stock
        kb = await create_main_menu_kb()
        if stock >= int(callback.data):
            await state.set_state(WriteOffStates.finish)
            await state.update_data(enteringQuantity=callback.data)
            # данные о пользователе
            user_id = callback.from_user.id
            user_name = callback.from_user.username
            user_first_name = callback.from_user.first_name
            user_last_name = callback.from_user.last_name
            telegram_user = await get_or_create_telegram_user(user_id, user_name, user_first_name, user_last_name)
            user_data = await state.get_data()
            write_off = await create_write_off(user_data, telegram_user)
            if write_off:
                await state.clear()
                custom_sku = user_data['choosingModification']
                thumbnail_input_file = await get_large_image_url_input_file(custom_sku)
                await bot.send_photo(chat_id=callback.from_user.id,
                                     photo=thumbnail_input_file,
                                     caption=f'✅ Списание успешно проведено на сумму {write_off.total_amount}\n\n'
                                             f'вы списали {user_data["choosingModification"]}\n'
                                             f'в количестве {user_data["enteringQuantity"]}шт.\n', reply_markup=kb)
                await callback.answer()
        else:
            await callback.message.answer(f'⛔️ В наличии только {stock}шт. вы хотите списать {callback.data}шт.')
            await callback.answer()

