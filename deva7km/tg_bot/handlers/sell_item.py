from aiogram import Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from asgiref.sync import sync_to_async

from deva7km.settings import BOT_TOKEN
from tg_bot.FSM.fsm import SellStates
from tg_bot.keyboards.keyboards import create_inline_kb_main_sku, create_inline_kb_modifications, \
    create_inline_kb_numbers, create_payment_type_keyboard, create_main_menu_kb, create_inline_kb_add_more, \
    create_inline_kb_yes_no
from tg_bot.lexicon.lexicon import LEXICON_PAYMENT_TYPE
from tg_bot.services.products import get_large_image_url_input_file
from tg_bot.services.sells import check_stock_status, create_sale, get_product_modification, get_stock
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
    await state.clear()
    await state.set_state(SellStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='sell')
    await callback.message.answer('Выберите товар для продажи 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=sku для sell и выводил кнопки с модификациями конкретного товара
@router.callback_query(StateFilter(SellStates.choosingSKU))
@admin_access_control_decorator(access='seller')
async def process_callback_query_sku(callback: CallbackQuery, state: FSMContext):
    if '_main_sku_sell' in callback.data:
        sku = callback.data.split("_")[0]
        await state.set_state(SellStates.choosingModification)
        await state.update_data(choosingSKU=sku)
        user_data = await state.get_data()
        kb = await create_inline_kb_modifications(sku, callback='sell')
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
            stock = await get_stock(custom_sku)
            custom_sku = user_data['choosingModification']
            thumbnail_input_file = await get_large_image_url_input_file(custom_sku)
            kb = await create_inline_kb_numbers(stock)
            await bot.send_photo(chat_id=callback.from_user.id,
                                 photo=thumbnail_input_file,
                                 caption=f'Вы выбрали для продажи модификацию ➡️ {hbold(user_data["choosingModification"])}\n'
                                         f'Введите количество товара для продажи:', reply_markup=kb)
            await callback.answer()
        else:
            await callback.message.answer('⛔️ Товара на складе нет!')
            await callback.answer()
    else:
        await callback.message.answer('выберите модификацию или нажмите отмена! 👆')
        await callback.answer()


# обработчик который бы предлагал добавить еще товар для оприходования после ввода количества товара
@router.callback_query(StateFilter(SellStates.enteringQuantity),
                       lambda callback: callback.data not in ['add_more', 'finish'])
@admin_access_control_decorator(access='seller')
async def process_callback_query_quantity(callback: CallbackQuery, state: FSMContext):
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

    # Создание строки с товарами
    products_text = ""
    for product in user_data['products_list']:
        custom_sku = product['choosingModification']
        quantity = product['enteringQuantity']
        products_text += f'{custom_sku} - {quantity}шт.\n'
    kb = await create_inline_kb_add_more()

    await callback.message.answer(f'Вы выбрали для продажи ➡️\n\n{products_text}\n выберите еще товар '
                                  f'или завершите продажу', reply_markup=kb)
    await callback.answer()


# обработчик который бы отлавливал callback_query=add_more для sell
@router.callback_query(StateFilter(SellStates.enteringQuantity), lambda callback: 'add_more' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_add_more(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SellStates.choosingSKU)
    kb = await create_inline_kb_main_sku(callback='sell')
    await callback.message.answer('Выберите товар для продажи 👇', reply_markup=kb)
    await callback.answer()


# обработчик который бы реагировал на кнопку "Завершить"
@router.callback_query(StateFilter(SellStates.enteringQuantity), lambda callback: 'finish' == callback.data)
@admin_access_control_decorator(access='admin')
async def process_callback_query_finish(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SellStates.choosingPayment)
    await process_callback_query_payment(callback, state)


# обработчик который бы выводил клавиатуру с кнопками "нал" или "безнал"
@router.callback_query(StateFilter(SellStates.choosingPayment), lambda callback: callback.data not in ['cash', 'non_cash', 'yes', 'no'])
@admin_access_control_decorator(access='seller')
async def process_callback_query_payment(callback: CallbackQuery, state: FSMContext):
    kb = await create_payment_type_keyboard()
    await callback.message.answer('Выберите метод оплаты 👇', reply_markup=kb)
    await callback.answer()


# обработчик спрашивал бы ввести комментарий
@router.callback_query(StateFilter(SellStates.choosingPayment), lambda callback: callback.data not in ['yes', 'no'])
@admin_access_control_decorator(access='seller')
async def process_callback_query_comment(callback: CallbackQuery, state: FSMContext):
    kb = await create_inline_kb_yes_no()
    await state.update_data(choosingPayment=callback.data)
    await callback.message.answer('Добавить комментарий?', reply_markup=kb)
    await callback.answer()


# обработчик который бы реагировал на callback "yes" и выводил "введите ваш комментарий"
@router.callback_query(StateFilter(SellStates.choosingPayment), lambda callback: callback.data == 'yes')
@admin_access_control_decorator(access='seller')
async def process_callback_query_comment_yes(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SellStates.enteringComment)
    await callback.message.answer('Введите ваш комментарий перед завершением')
    await callback.answer()


# обработчик который бы сохранял введенный комментарий пользователем
@router.message(StateFilter(SellStates.enteringComment))
@admin_access_control_decorator(access='seller')
async def process_message_comment(message: Message, state: FSMContext):
    await state.update_data(enteringComment=message.text)
    await state.set_state(SellStates.finish)
    user_data = await state.get_data()

    # данные о пользователе
    user_id = message.from_user.id
    user_name = message.from_user.username
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    telegram_user = await get_or_create_telegram_user(user_id, user_name, user_first_name, user_last_name)

    # Создание строки с товарами
    products_text = ""
    for product in user_data['products_list']:
        custom_sku = product['choosingModification']
        quantity = product['enteringQuantity']
        products_text += f'{custom_sku} - {quantity}шт.\n'

    payment = LEXICON_PAYMENT_TYPE[user_data['choosingPayment']]
    comment = user_data['enteringComment'] if 'enteringComment' in user_data else 'без комментария'

    # Создание продажи
    try:
        sale = await create_sale(user_data, telegram_user)
    except Exception as e:
        print(e)
        await message.answer(f'Ошибка при создании продажи {e}')
        await state.clear()
        return

    kb = await create_main_menu_kb()

    await message.answer(
        f'✅ Продажа успешно проведена на сумму {hbold(await sync_to_async(sale.calculate_total_amount)())}грн.\n\n'
        f'вы продали:\n{products_text}\n'
        f'тип продажи - {hbold(payment)}\n'
        f'комментарий - {hbold(comment)}\n',
        reply_markup=kb)
    await state.clear()


# обработчик который бы реагировал на callback "no" и выводил "введите ваш комментарий"
@router.callback_query(StateFilter(SellStates.choosingPayment), lambda callback: callback.data == 'no')
@admin_access_control_decorator(access='seller')
async def process_callback_query_comment_no(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SellStates.enteringComment)
    await process_callback_query_finish_sell(callback, state)


# заключительный обработчик который бы создавал продажу и очищал данные из состояния
@router.callback_query(StateFilter(SellStates.finish))
@admin_access_control_decorator(access='seller')
async def process_callback_query_finish_sell(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()

    # данные о пользователе
    user_id = callback.from_user.id
    user_name = callback.from_user.username
    user_first_name = callback.from_user.first_name
    user_last_name = callback.from_user.last_name
    telegram_user = await get_or_create_telegram_user(user_id, user_name, user_first_name, user_last_name)

    # Создание строки с товарами
    products_text = ""
    for product in user_data['products_list']:
        custom_sku = product['choosingModification']
        quantity = product['enteringQuantity']
        products_text += f'{custom_sku} - {quantity}шт.\n'

    payment = LEXICON_PAYMENT_TYPE[user_data['choosingPayment']]
    comment = user_data['enteringComment'] if 'enteringComment' in user_data else 'без комментария'

    # Создание продажи
    try:
        sale = await create_sale(user_data, telegram_user)
    except Exception as e:
        print(e)
        await callback.message.answer(f'Ошибка при создании продажи {e}')
        await state.clear()
        return

    kb = await create_main_menu_kb()

    await callback.message.answer(
        f'✅ Продажа успешно проведена на сумму {hbold(await sync_to_async(sale.calculate_total_amount)())}грн.\n\n'
        f'вы продали:\n{products_text}\n'
        f'тип продажи - {hbold(payment)}\n'
        f'комментарий - {hbold(comment)}\n',
        reply_markup=kb)
    await state.clear()
    await callback.answer()
