from aiogram.fsm.state import StatesGroup, State


class SellStates(StatesGroup):
    choosingSKU = State()
    choosingModification = State()
    enteringQuantity = State()
    choosingPayment = State()
    finish = State()