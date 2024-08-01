from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async

from deva7km.settings import BOT_TOKEN
from tg_bot.FSM.fsm import ReturnStates
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_modifications, \
    create_inline_kb_numbers, create_main_menu_kb, create_inline_kb_yes_no
from tg_bot.services.products import get_large_image_url_input_file
from tg_bot.services.returns import create_return
from tg_bot.services.users import admin_access_control_decorator, get_or_create_telegram_user

router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# Обработчик команды /return
@router.message(Command('return'))
@admin_access_control_decorator(access='seller')
async def command_return_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(ReturnStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='return')
    await message.answer('Выберите товар для возврата 👇', reply_markup=kb)


# Обработчик callback_query=return
@router.callback_query(lambda callback: 'return' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_return(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(ReturnStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='return')
    await callback.message.answer('Выберите товар для возврата 👇', reply_markup=kb)
    await callback.answer()


# Обработчик callback_query=sku для return
@router.callback_query(StateFilter(ReturnStates.choosingSKU))
@admin_access_control_decorator(access='seller')
async def process_callback_query_sku(callback: CallbackQuery, state: FSMContext):
    if '_main_sku_return' in callback.data:
        sku = callback.data.split("_")[0]
        await state.set_state(ReturnStates.choosingModification)
        await state.update_data(choosingSKU=sku)
        user_data = await state.get_data()
        kb = await create_inline_kb_modifications(sku, callback='return')
        await callback.message.answer(f'Вы выбрали для возврата модель ➡️ {hbold(user_data["choosingSKU"])}\nвыберите '
                                      f'модификацию 👇', reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('выберите основной товар или нажмите отмена! 👆')
        await callback.answer()


# Обработчик callback_query=modifications для return
@router.callback_query(StateFilter(ReturnStates.choosingModification))
@admin_access_control_decorator(access='seller')
async def process_callback_query_modifications(callback: CallbackQuery, state: FSMContext):
    if '_modification_return' in callback.data:
        custom_sku = callback.data.split("_")[0]
        await state.set_state(ReturnStates.enteringQuantity)
        await state.update_data(choosingModification=custom_sku)
        user_data = await state.get_data()
        custom_sku = user_data['choosingModification']
        thumbnail_input_file = await get_large_image_url_input_file(custom_sku)
        kb = await create_inline_kb_numbers()
        await bot.send_photo(chat_id=callback.from_user.id,
                             photo=thumbnail_input_file,
                             caption=f'Вы выбрали для возврата модификацию ➡️ {hbold(user_data["choosingModification"])}\n'
                                     f'Введите количество товара для возврата:', reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('выберите модификацию или нажмите отмена! 👆')
        await callback.answer()


# Обработчик callback_query=numbers для return
@router.callback_query(StateFilter(ReturnStates.enteringQuantity))
@admin_access_control_decorator(access='seller')
async def process_callback_query_numbers(callback: CallbackQuery, state: FSMContext):
    if callback.data.isdigit():
        await state.set_state(ReturnStates.askingForComment)
        await state.update_data(enteringQuantity=callback.data)
        kb = await create_inline_kb_yes_no()
        await callback.message.answer('Добавить комментарий?', reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('Введите корректное количество товара!')
        await callback.answer()


# Обработчик для добавления комментария
@router.callback_query(StateFilter(ReturnStates.askingForComment), lambda callback: callback.data == 'yes')
@admin_access_control_decorator(access='seller')
async def process_callback_query_add_comment(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ReturnStates.enteringComment)
    await callback.message.answer('Введите ваш комментарий:')
    await callback.answer()


# Обработчик для отказа от комментария
@router.callback_query(StateFilter(ReturnStates.askingForComment), lambda callback: callback.data == 'no')
@admin_access_control_decorator(access='seller')
async def process_callback_query_no_comment(callback: CallbackQuery, state: FSMContext):
    await state.update_data(enteringComment='')
    await process_return(callback, state)


# Обработчик для ввода комментария
@router.message(StateFilter(ReturnStates.enteringComment))
@admin_access_control_decorator(access='seller')
async def process_message_comment(message: Message, state: FSMContext):
    await state.update_data(enteringComment=message.text)
    await process_return(message, state)


# Обработчик для завершения возврата
async def process_return(message_or_callback, state: FSMContext):
    user_data = await state.get_data()

    # данные о пользователе
    if isinstance(message_or_callback, Message):
        user_id = message_or_callback.from_user.id
        user_name = message_or_callback.from_user.username
        user_first_name = message_or_callback.from_user.first_name
        user_last_name = message_or_callback.from_user.last_name
    else:
        user_id = message_or_callback.from_user.id
        user_name = message_or_callback.from_user.username
        user_first_name = message_or_callback.from_user.first_name
        user_last_name = message_or_callback.from_user.last_name

    telegram_user = await get_or_create_telegram_user(user_id, user_name, user_first_name, user_last_name)

    # Создание возврата
    return_item = await create_return(user_data, telegram_user)
    if return_item:
        await state.clear()
        kb = await create_main_menu_kb()
        custom_sku = user_data['choosingModification']
        thumbnail_input_file = await get_large_image_url_input_file(custom_sku)
        message_text = (
            f'✅ Возврат успешно проведен на сумму {hbold(await sync_to_async(return_item.calculate_total_amount)())}грн.\n\n'
            f'вы вернули {user_data["choosingModification"]}\n'
            f'в количестве {user_data["enteringQuantity"]}шт.\n'
            f'Комментарий: {user_data["enteringComment"]}'
        )
        if isinstance(message_or_callback, Message):
            await bot.send_photo(chat_id=message_or_callback.from_user.id,
                                 photo=thumbnail_input_file,
                                 caption=message_text, reply_markup=kb)
        else:
            await bot.send_photo(chat_id=message_or_callback.from_user.id,
                                 photo=thumbnail_input_file,
                                 caption=message_text, reply_markup=kb)
            await message_or_callback.answer()
    else:
        await message_or_callback.message.answer('⛔️ ProductModification не найден')


# Заключительный обработчик возврата
@router.callback_query(StateFilter(ReturnStates.finish))
@admin_access_control_decorator(access='seller')
async def process_callback_query_finish_return(callback: CallbackQuery, state: FSMContext):
    await process_return(callback, state)
