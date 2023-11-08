
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    kb = await create_inline_kb_main_sku()
    await message.answer("Вот ваша клавиатура:", reply_markup=kb)
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")