from aiogram.fsm.state import StatesGroup, State


class SellStates(StatesGroup):
    choosingSKU = State()
    choosingModification = State()
    enteringQuantity = State()
    choosingPayment = State()
    enteringComment = State()
    finish = State()


class ReturnStates(StatesGroup):
    choosingSKU = State()
    choosingModification = State()
    enteringQuantity = State()
    askingForComment = State()  # Добавляем новое состояние
    enteringComment = State()
    finish = State()


class InventoryStates(StatesGroup):
    choosingSKU = State()
    choosingModification = State()
    enteringQuantity = State()
    finish = State()


class WriteOffStates(StatesGroup):
    choosingSKU = State()
    choosingModification = State()
    enteringQuantity = State()
    finish = State()