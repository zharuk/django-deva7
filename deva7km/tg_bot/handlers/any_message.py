from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from tg_bot.lexicon.lexicon import LEXICON_COMMANDS_MENU

router: Router = Router()


# Обработчик любого сообщения от пользователя
@router.message()
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    # Формируем текст сообщения на основе словаря
    commands_menu_text = '\n'.join(
        [f'{command}: {description}' for command, description in LEXICON_COMMANDS_MENU.items()])

    # Отправляем ответ
    await message.answer(f'Моя твоя не понимать😲\n\nДоступные команды:\n\n{commands_menu_text}')
