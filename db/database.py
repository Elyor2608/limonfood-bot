import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,
            ism TEXT,
            telefon TEXT,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

async def get_user(telegram_id):
    import asyncio
    loop = asyncio.get_event_loop()
    def _get():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    return await loop.run_in_executor(None, _get)

async def add_user(telegram_id, ism, telefon):
    import asyncio
    loop = asyncio.get_event_loop()
    def _add():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (telegram_id, ism, telefon) VALUES (%s, %s, %s) ON CONFLICT (telegram_id) DO NOTHING",
                    (telegram_id, ism, telefon))
        conn.commit()
        cur.close()
        conn.close()
    return await loop.run_in_executor(None, _add)
