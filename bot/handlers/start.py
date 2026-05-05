from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from bot.keyboards.main_kb import telefon_keyboard, main_menu
from db.database import pool


class Register(StatesGroup):
    telefon = State()
    ism = State()


async def start(message: Message, state: FSMContext):
    await state.finish()
    async with pool.acquire() as conn:
        user = await conn.fetchrow(
            "SELECT * FROM users WHERE telegram_id = $1",
            message.from_user.id
        )
    if user:
        await message.answer(
            f"Xush kelibsiz, {user['ism']}! 🍋\nNima buyurtma qilamiz?",
            reply_markup=main_menu()
        )
    else:
        await message.answer(
            "Assalomu alaykum! LimonFood ga xush kelibsiz! 🍋\n\n"
            "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring:",
            reply_markup=telefon_keyboard()
        )
        await Register.telefon.set()


async def get_telefon(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Iltimos, tugmani bosing 👇", reply_markup=telefon_keyboard())
        return
    await state.update_data(telefon=message.contact.phone_number)
    await message.answer("Ismingizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await Register.ism.set()


async def get_ism(message: Message, state: FSMContext):
    ism = message.text
    data = await state.get_data()
    telefon = data.get("telefon")

    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO users (telegram_id, ism, telefon) VALUES ($1, $2, $3) "
            "ON CONFLICT (telegram_id) DO NOTHING",
            message.from_user.id, ism, telefon
        )

    await state.finish()
    await message.answer(
        f"Rahmat, {ism}! Ro'yxatdan o'tdingiz ✅\n\nNima buyurtma qilamiz?",
        reply_markup=main_menu()
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(get_telefon, content_types=["contact"], state=Register.telefon)
    dp.register_message_handler(get_ism, state=Register.ism)
