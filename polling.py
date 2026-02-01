from handlers.dispatcher import set_up_dispatcher
from dependencies.deps import AppResources, get_resources
import logging
import asyncio
from fastapi import Depends
import os
from aiogram import Bot, Dispatcher

logger = logging.getLogger(__name__)


async def polling(resources: AppResources = Depends(get_resources)):
    dp: Dispatcher = set_up_dispatcher()
    bot: Bot = Bot(token=os.getenv("BOT_TOKEN"))
    db_pool = resources.pool

    # удаляем webhook, если он был установлен
    await bot.delete_webhook(drop_pending_updates=True)
    # запускаем polling
    try:
        await dp.start_polling(bot, db_pool=db_pool)
    except Exception as e:
        logger.exception(e)
    finally:
        await db_pool.close()
        logger.info("Connection to Postgres closed")


if __name__ == "__main__":
    asyncio.run(polling())
