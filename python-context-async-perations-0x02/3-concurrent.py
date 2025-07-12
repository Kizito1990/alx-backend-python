

import asyncio
import aiosqlite


DB_PATH = "users.db"


# Helper to create a tiny sample table (run once)

async def setup_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                age  INTEGER
            )
        """)
        await db.execute("DELETE FROM users")  # clear for repeat runs
        await db.executemany(
            "INSERT INTO users (name, age) VALUES (?, ?)",
            [
                ("Ada", 25),
                ("Chioma", 35),
                ("Chinedu", 42),
                ("Daisy", 55),
            ],
        )
        await db.commit()


# Async query functions

async def async_fetch_users():
    """Fetch ALL users."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows


async def async_fetch_older_users():
    """Fetch users older than 40."""
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows



# Gather them concurrently

async def fetch_concurrently():
    
    await setup_db()

    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All users:")
    for row in all_users:
        print(row)

    print("\nUsers older than 40:")
    for row in older_users:
        print(row)



# ENTRY POINT
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
