from contextlib import asynccontextmanager
from dependencies.deps import AppResources
from database.database import create_pool
from handlers.dispatcher import set_up_dispatcher
from aiogram import Bot
import os
from redis.asyncio import Redis
from fastapi import FastAPI
from webhook.webhook import router as tg_router
import logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=os.getenv("LOG_LEVEL"), format=os.getenv("LOG_FORMAT"))
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = set_up_dispatcher()
    pool = await create_pool()
    app.state.pool = pool
    app.state.dp = dp
    app.state.bot = bot
    redis_client = Redis.from_url(os.getenv("REDIS_URL"))
    app.state.redis_client = redis_client
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    await bot.set_webhook(WEBHOOK_URL)
    app.state.resources = AppResources(
        pool=pool,
        redis=redis_client,
    )
    bot["resources"] = app.state.resources
    logger.info("starting")
    yield
    await bot.delete_webhook()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(tg_router)
