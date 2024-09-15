from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router: Router = Router()


# Обработчик любого сообщения от пользователя
@router.message()
async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    await message.answer(f'Моя твоя не понимать😲\n\nДоступные команды: /start')
