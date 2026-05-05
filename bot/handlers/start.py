from aiogram import Dispatcher
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from bot.keyboards.main_kb import telefon_keyboard, main_menu
from db.database import get_user, add_user


class Register:
    telefon = "telefon_state"
    ism = "ism_state"


async def start(message: Message, state: FSMContext):
    await state.finish()
    user = await get_user(message.from_user.id)
    
    if user:
        await message.answer(
            f"Xush kelibsiz, {user[2]}! 🍋\nNima buyurtma qilamiz?",
            reply_markup=main_menu()
        )
    else:
        await message.answer(
            "Assalomu alaykum! LimonFood ga xush kelibsiz! 🍋\n\n"
            "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring:",
            reply_markup=telefon_keyboard()
        )
        await state.set_state(Register.telefon)


async def get_telefon(message: Message, state: FSMContext):
    if not message.contact:
        await message.answer("Iltimos, tugmani bosing 👇", reply_markup=telefon_keyboard())
        return
    await state.update_data(telefon=message.contact.phone_number)
    await message.answer("Ismingizni kiriting:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(Register.ism)


async def get_ism(message: Message, state: FSMContext):
    ism = message.text
    data = await state.get_data()
    telefon = data.get("telefon")

    await add_user(message.from_user.id, ism, telefon)
    
    await state.finish()
    await message.answer(
        f"Rahmat, {ism}! Ro'yxatdan o'tdingiz ✅\n\nNima buyurtma qilamiz?",
        reply_markup=main_menu()
    )


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(get_telefon, content_types=["contact"])
    dp.register_message_handler(get_ism)
