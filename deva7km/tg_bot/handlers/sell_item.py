from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async

from deva7km.settings import BOT_TOKEN
from tg_bot.FSM.fsm import SellStates
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_modifications, \
    create_inline_kb_numbers, create_payment_type_keyboard, create_main_menu_kb, create_inline_kb_yes_no, \
    create_inline_kb_ready_cancel
from tg_bot.services.products import get_large_image_url_input_file
from tg_bot.services.sells import check_stock_status, create_sale, get_product_modification
from tg_bot.services.users import admin_access_control_decorator, get_or_create_telegram_user

router: Router = Router()
bot: Bot = Bot(token=BOT_TOKEN, parse_mode='HTML')


# Обработчик команды /sell
@router.message(Command('sell'))
@admin_access_control_decorator(access='seller')
async def command_sell_handler(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(SellStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='sell')
    await message.answer('Выберите товар для продажи 👇', reply_markup=kb)


# обработчик который бы отлавливал callback_query=sell
@router.callback_query(lambda callback: 'sell' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_sell(callback: CallbackQuery, state: FSMContext):
    kb = await create_inline_kb_main_sku(callback='sell')
    await state.clear()
    await state.set_state(SellStates.choosingSKU)
    await callback.message.answer('Выберите товар для продажи 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=sku для sell и выводил кнопки с модификациями конкретного товара
@router.callback_query(StateFilter(SellStates.choosingSKU), lambda callback: 'product_list' not in callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_sku(callback: CallbackQuery, state: FSMContext):
    if '_main_sku_sell' in callback.data:
        sku = callback.data.split("_")[0]
        await state.set_state(SellStates.choosingModification)
        await state.update_data(choosingSKU=sku)
        user_data = await state.get_data()
        if 'products_list' not in user_data:
            kb = await create_inline_kb_modifications(sku, callback='sell')
        else:
            kb = await create_inline_kb_modifications(sku, callback='sell', product_list=True)
        await callback.message.answer(f'Вы выбрали для продажи модель ➡️ {hbold(user_data["choosingSKU"])}\nвыберите '
                                      f'модификацию 👇', reply_markup=kb)
        await callback.answer()
    else:
        await callback.message.answer('выберите основной товар или нажмите отмена! 👆')
        await callback.answer()


# обработчик который бы отлавливал callback_query=modifications для sell и выводил количество
# товара на остатке, а также указать сколько товара нужно продать
@router.callback_query(StateFilter(SellStates.choosingModification))
@admin_access_control_decorator(access='seller')
async def process_callback_query_modifications(callback: CallbackQuery, state: FSMContext):
    if '_modification_sell' in callback.data:
        custom_sku = callback.data.split("_")[0]
        if await check_stock_status(custom_sku):
            await state.set_state(SellStates.enteringQuantity)
            await state.update_data(choosingModification=custom_sku)
            user_data = await state.get_data()
            custom_sku = user_data['choosingModification']
            thumbnail_input_file = await get_large_image_url_input_file(custom_sku)
            kb = await create_inline_kb_numbers()
            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=thumbnail_input_file,
                                 caption=f'Вы выбрали для продажи модификацию ➡️ {hbold(user_data["choosingModification"])}\n'
                                         f'Введите количество товара для продажи:', reply_markup=kb)
            await callback.answer()
        else:
            await callback.message.answer('⛔️ Товара на складе нет!')
            await callback.answer()
    else:
        if callback.data == 'product_list':
            await process_callback_query_numbers(callback, state)
        else:
            await callback.message.answer('выберите модификацию или нажмите отмена! 👆')
            await callback.answer()


# обработчик который бы отлавливал callback_query=numbers для sell и выводил клавиатуру с кнопками "нал" или
# "безнал" а также возможность добавить товар еще
@router.callback_query(StateFilter(SellStates.enteringQuantity))
@admin_access_control_decorator(access='seller')
async def process_callback_query_numbers(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    modification = await get_product_modification(user_data['choosingModification'])
    stock = modification.stock
    if callback.data.isdigit():
        if stock >= int(callback.data):
            await state.set_state(SellStates.choosingPayment)
            await state.update_data(enteringQuantity=callback.data[0])
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

            # Создание строки с товарами
            products_text = ""
            for product in user_data['products_list']:
                custom_sku = product['choosingModification']
                quantity = product['enteringQuantity']
                products_text += f'{custom_sku} - {quantity}шт.\n'

            kb = await create_payment_type_keyboard()
            await callback.message.answer(f'Вы выбрали для продажи ➡️\n\n{products_text}\n выберите оплату '
                                          f'или добавьте еще товар', reply_markup=kb)
            await callback.answer()
        else:
            await callback.message.answer(f'⛔️ В наличии только {stock}шт. вы хотите продать {callback.data}шт.')
            await callback.answer()
    else:
        if callback.data == 'product_list':
            await state.set_state(SellStates.choosingPayment)
            user_data = await state.get_data()

            products_text = ""
            for product in user_data['products_list']:
                custom_sku = product['choosingModification']
                quantity = product['enteringQuantity']
                products_text += f'{custom_sku} - {quantity}шт.\n'

            kb = await create_payment_type_keyboard()
            await callback.message.answer(f'Вы выбрали для продажи ➡️\n\n{products_text}\n выберите оплату '
                                          f'или добавьте еще товар', reply_markup=kb)
            await callback.answer()

        else:
            await callback.message.answer('Выберите количество товара или нажмите отмена! 👆')
            await callback.answer()


# Обработчик, который бы срабатывал при добавлении товара еще в продажу
@router.callback_query(StateFilter(SellStates.choosingPayment), lambda callback: 'add_more' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_more(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SellStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='sell', product_list=True)
    await callback.message.answer(f'Выберите товар для продажи 👇', reply_markup=kb)
    await callback.answer()


# Обработчик который бы срабатывал на кнопку "К списку товаров" и переходил обратно к хендлеру
# process_callback_query_numbers
@router.callback_query(lambda callback: 'product_list' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_product_list(callback: CallbackQuery, state: FSMContext):
    await process_callback_query_numbers(callback, state)


# Обработчик, который просит добавить комментарий, если необходимо
@router.callback_query(StateFilter(SellStates.choosingPayment))
@admin_access_control_decorator(access='seller')
async def process_callback_query_finish(callback: CallbackQuery, state: FSMContext):
    await state.update_data(choosingPayment=callback.data)
    kb = await create_inline_kb_yes_no()
    await state.set_state(SellStates.enteringComment)
    await callback.message.answer('Добавить комментарий?', reply_markup=kb)
    await callback.answer()


# Обработчик который бы срабатывал на кнопку "да" в конце продажи и позволял добавить комментарий
@router.callback_query(StateFilter(SellStates.enteringComment), lambda callback: 'yes' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_finish(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите ваш комментарий')
    await callback.answer()


# Обработчик для ввода комментария
@router.message(StateFilter(SellStates.enteringComment), )
@admin_access_control_decorator(access='seller')
async def process_comment_input(message: Message, state: FSMContext):
    comment = message.text
    await state.update_data(comment=comment)
    await state.set_state(SellStates.finish)
    kb = await create_inline_kb_ready_cancel()
    # Вывод подтверждения или что-то еще
    await message.answer(f'Ваш комментарий : {comment}\n нажмите "готово" для продажи или отмените операцию',
                         reply_markup=kb)


# Обработчик который бы срабатывал на кнопку "нет" если комментарий не нужен
@router.callback_query(StateFilter(SellStates.enteringComment), lambda callback: 'no' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_finish_no_comment(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SellStates.finish)
    await process_callback_query_finish(callback, state)


# заключительный обработчик который бы создавал продажу и завершал FSM
@router.callback_query(StateFilter(SellStates.finish), lambda callback: 'ready' == callback.data)
@admin_access_control_decorator(access='seller')
async def process_callback_query_finish(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    # данные о пользователе
    user_id = callback.from_user.id
    user_name = callback.from_user.username
    user_first_name = callback.from_user.first_name
    user_last_name = callback.from_user.last_name
    telegram_user = await get_or_create_telegram_user(user_id, user_name, user_first_name, user_last_name)
    await state.set_state(SellStates.finish)

    # Создание строки с товарами
    products_text = ""
    for product in user_data['products_list']:
        custom_sku = product['choosingModification']
        quantity = product['enteringQuantity']
        products_text += f'{custom_sku} - {quantity}шт.\n'

    payment_types = {
        'cash': 'наличная 💵',
        'non_cash': 'безналичная 💳',
    }

    # Создание продажи
    sale = await create_sale(user_data, telegram_user)
    kb = await create_main_menu_kb()

    await callback.message.answer(
        f'✅ Продажа успешно проведена на сумму {await sync_to_async(sale.calculate_total_amount)()}грн.\n\n'
        f'вы продали:\n{products_text}\n'
        f'тип оплаты - {payment_types[user_data["choosingPayment"]]}\n'
        f'комментарий - {user_data["comment"] if "comment" in user_data.keys() else "без комментария"} ',
        reply_markup=kb)
    await state.clear()
    await callback.answer()
