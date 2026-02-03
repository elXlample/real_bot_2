import os
from dependencies.deps import AppResources
import asyncpg
from urllib.parse import urlparse
import logging
from psycopg_pool import AsyncConnectionPool
from urllib.parse import quote

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


async def add_user(resources: AppResources, user_id: int, username: str) -> str:
    async with resources.pool.connection() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute(
                query="""
                    SELECT tg_id
                    FROM users_alembic
                    WHERE tg_id = %s;
                """,
                params=(user_id,),
            )
        result = await cursor.fetchall()

    if result is None:
        async with resources.pool.connection() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    query="""
                        INSERT INTO users_alembic(tg_id, username)
                        VALUES(
                            %(tg_id)s, 
                            %(username)s   
                             
                            
                        ) ON CONFLICT DO NOTHING;
                    """,
                    params={
                        "tg_id": user_id,
                        "username": username,
                    },
                )
        logger.info(f"user {username} inserted into users_alembic")
        return f"user {username} added to users_alembic"
    else:
        logger.info(f"user {username} already in users_alembic! ")
        return f"user {username} already in users_alembic! "
