from aiogram.fsm.state import State, StatesGroup

class Register(StatesGroup):
    telefon = State()
    ism = State()

class Order(StatesGroup):
    restoran_tanlash = State()
    mahsulot_tanlash = State()
    manzil = State()
    telefon = State()
    tolav = State()

class Location(StatesGroup):
    yuborish = State()
