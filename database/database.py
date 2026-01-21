import os
import asyncpg
import asyncio
from urllib.parse import urlparse
import logging
from psycopg_pool import AsyncConnectionPool
from urllib.parse import quote
from fastapi import FastAPI

logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv("LOG_LEVEL"), format=os.getenv("LOG_FORMAT"))


async def create_conn():
    database_url = os.getenv("DATABASE_URL")

    # Парсим строку подключения
    parsed = urlparse(database_url)
    logger.debug("this is parsed:")
    logger.info(parsed)

    conn = await asyncpg.connect(
        user=parsed.username,
        password=parsed.password,
        database=parsed.path[1:],  # убираем первый слэш
        host=parsed.hostname,
        port=parsed.port or 5432,
        ssl="require",
    )
    return conn


async def test_connection():
    try:
        conn = await create_conn()
        logger.info("✅ Подключение к Neon.tech успешно!")

        # Проверяем версию PostgreSQL
        version = await conn.fetchval("SELECT version()")
        logger.debug(f"Версия PostgreSQL: {version.split(',')[0]}")

        await conn.close()
    except Exception as e:
        logger.error(f"❌ Ошибка подключения: {e}")


def build_pg_conninfo(
    db_name: str,
    host: str,
    port: int,
    user: str,
    password: str,
) -> str:
    conninfo = (
        f"postgresql://{quote(user, safe='')}:{quote(password, safe='')}"
        f"@{host}:{port}/{db_name}"
    )
    logger.debug(
        f"Building PostgreSQL connection string (password omitted): "
        f"postgresql://{quote(user, safe='')}@{host}:{port}/{db_name}"
    )
    return conninfo


async def create_pool() -> AsyncConnectionPool:
    pool = AsyncConnectionPool(
        conninfo=os.getenv("DATABASE_URL"),
        min_size=1,
        max_size=10,
    )
    return pool


async def create_table_users(app: FastAPI):
    from main import app

    pool: AsyncConnectionPool = app.state.pool
    try:
        async with pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query="""
                            CREATE TABLE IF NOT EXISTS users(
                                id SERIAL PRIMARY KEY,
                                user_id BIGINT NOT NULL UNIQUE,
                                username VARCHAR(50),
                                created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
                                language VARCHAR(10) NOT NULL,
                                role VARCHAR(30) NOT NULL,
                                is_alive BOOLEAN NOT NULL 
                            ); 
                        """
                )
                logger.info("DB users CREATED")
    finally:
        if conn:
            logger.debug("Connection returned to pool")
