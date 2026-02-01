from handlers.dispatcher import set_up_dispatcher
from database.database import create_pool
from dependencies.deps import AppResources, get_resources
from mids.basic import ResourcesMiddleware
from redis.asyncio import Redis
import logging
import asyncio
import sys
import os
from aiogram import Bot, Dispatcher

logger = logging.getLogger(__name__)

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def polling():
    dp: Dispatcher = set_up_dispatcher()
    bot: Bot = Bot(token=os.getenv("BOT_TOKEN"))
    pool = await create_pool()
    redis_client = Redis.from_url(os.getenv("REDIS_URL"))
    resources = AppResources(pool=pool, redis=redis_client)
    dp.message.middleware(ResourcesMiddleware(resources=resources))
    # удаляем webhook, если он был установлен
    await bot.delete_webhook(drop_pending_updates=True)
    # запускаем polling
    try:
        await dp.start_polling(bot, db_pool=pool)
    except Exception as e:
        logger.exception(e)
    finally:
        await pool.close()
        logger.info("Connection to Postgres closed")


if __name__ == "__main__":
    asyncio.run(polling())
