from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍔 Fastfood"), KeyboardButton(text="🍲 Milliy taomlar")],
            [KeyboardButton(text="📍 Yaqin atrofdagilar")],
            [KeyboardButton(text="📋 Buyurtmalar tarixi")]
        ],
        resize_keyboard=True
    )
    return keyboard

def telefon_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def lokatsiya_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Lokatsiyamni yuborish", request_location=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def manzil_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📍 Mening lokatsiyam", request_location=True)],
            [KeyboardButton(text="✏️ Manzilni yozib kiriting")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def qabul_telefon_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Mening raqamim")],
            [KeyboardButton(text="✏️ Boshqa raqam kiriting")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def tolav_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💳 Click"), KeyboardButton(text="💳 Payme")],
            [KeyboardButton(text="💵 Naqd")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def buyurtma_keyboard(buyurtma_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Keltirish", callback_data=f"keltirish_{buyurtma_id}"),
                InlineKeyboardButton(text="❌ Bekor qilish", callback_data=f"bekor_{buyurtma_id}")
            ]
        ]
    )
    return keyboard

def bekor_tasdiqlash_keyboard(buyurtma_id: int):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Ha, bekor qilaman", callback_data=f"bekor_ha_{buyurtma_id}"),
                InlineKeyboardButton(text="Yo'q, qaytaman", callback_data=f"bekor_yoq_{buyurtma_id}")
            ]
        ]
    )
    return keyboard
