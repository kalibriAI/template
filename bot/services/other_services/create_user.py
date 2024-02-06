from asyncpg import Pool


async def register_user(pool: Pool, uid: int, key: str) -> None:
    async with pool.acquire() as con:
        await con.execute('insert into users (id, key) values ($1, $2)', uid, key)
