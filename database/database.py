import os
import asyncpg
import asyncio
from urllib.parse import urlparse
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=os.getenv("LOG_LEVEL"), format=os.getenv("LOG_FORMAT"))


async def create_db_pool():
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
        conn = await create_db_pool()
        logger.info("✅ Подключение к Neon.tech успешно!")

        # Проверяем версию PostgreSQL
        version = await conn.fetchval("SELECT version()")
        logger.debug(f"Версия PostgreSQL: {version.split(',')[0]}")

        await conn.close()
    except Exception as e:
        logger.error(f"❌ Ошибка подключения: {e}")
