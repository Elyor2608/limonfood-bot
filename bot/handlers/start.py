from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from bot.states.register import Register
from bot.keyboards.main_kb import telefon_keyboard, main_menu
from db.database import pool

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
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
        await state.set_state(Register.telefon)

@router.message(Register.telefon, F.contact)
async def get_telefon(message: Message, state: FSMContext):
    telefon = message.contact.phone_number
    await state.update_data(telefon=telefon)
    await message.answer(
        "Ismingizni kiriting:",
        reply_markup=None
    )
    await state.set_state(Register.ism)

@router.message(Register.ism)
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

    await state.clear()
    await message.answer(
        f"Rahmat, {ism}! Ro'yxatdan o'tdingiz ✅\n\nNima buyurtma qilamiz?",
        reply_markup=main_menu()
    )
