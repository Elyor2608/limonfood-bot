import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

pool = None

async def create_pool():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL)
    return pool

async def get_pool():
    return pool

async def create_tables():
    async with pool.acquire() as conn:
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                ism TEXT,
                telefon TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
                           
            CREATE TABLE IF NOT EXISTS restaurants (
                id SERIAL PRIMARY KEY,
                nomi TEXT NOT NULL,
                tur TEXT NOT NULL,
                telefon TEXT,
                latitude FLOAT,
                longitude FLOAT,
                logo_url TEXT,
                ochilish_vaqti TEXT,
                yopilish_vaqti TEXT,
                bugun_yopiq BOOLEAN DEFAULT FALSE,
                faolmi BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS categories (
                id SERIAL PRIMARY KEY,
                restaurant_id INT REFERENCES restaurants(id),
                nomi TEXT NOT NULL,
                tartib INT DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS products (
                id SERIAL PRIMARY KEY,
                category_id INT REFERENCES categories(id),
                nomi TEXT NOT NULL,
                narxi FLOAT NOT NULL,
                rasm_url TEXT,
                mavjudmi BOOLEAN DEFAULT TRUE,
                tasdiqlangan BOOLEAN DEFAULT FALSE
            );

            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                restaurant_id INT REFERENCES restaurants(id),
                courier_id INT,
                holat TEXT DEFAULT 'draft',
                jami_narx FLOAT DEFAULT 0,
                tolav_turi TEXT,
                yetkazish_lat FLOAT,
                yetkazish_lng FLOAT,
                yetkazish_tel TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS order_items (
                id SERIAL PRIMARY KEY,
                order_id INT REFERENCES orders(id),
                product_id INT REFERENCES products(id),
                miqdor INT DEFAULT 1,
                narxi FLOAT
            );

            CREATE TABLE IF NOT EXISTS staff (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT UNIQUE NOT NULL,
                ism TEXT,
                rol TEXT,
                restaurant_id INT REFERENCES restaurants(id),
                avtomobil TEXT,
                telefon TEXT,
                holat TEXT DEFAULT 'bosh',
                faolmi BOOLEAN DEFAULT TRUE
            );

            CREATE TABLE IF NOT EXISTS deliveries (
                id SERIAL PRIMARY KEY,
                order_id INT REFERENCES orders(id),
                courier_id INT REFERENCES staff(id),
                pickup_photo_url TEXT,
                pickup_lat FLOAT,
                pickup_lng FLOAT,
                yetkazish_lat FLOAT,
                yetkazish_lng FLOAT,
                olingan_vaqt TIMESTAMP,
                yetkazilgan_vaqt TIMESTAMP
            );
        """)
