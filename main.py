from contextlib import asynccontextmanager
from dependencies.deps import AppResources
from database.database import create_pool
from database.database import test_connection, create_table_users
from handlers.dispatcher import set_up_dispatcher
from aiogram import Bot, Dispatcher
import os
import redis
from redis.asyncio import Redis
from fastapi import FastAPI, Request
from webhook.webhook import router as tg_router
import logging
import asyncio
from dataclasses import dataclass
from psycopg_pool import AsyncConnectionPool


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
    await create_table_users(app=app)
    redis_client = Redis.from_url(os.getenv("REDIS_URL"))
    app.state.redis_client = redis_client
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")
    await bot.set_webhook(WEBHOOK_URL)
    logger.info("starting")
    yield
    await bot.delete_webhook()
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
app.include_router(tg_router)


app.state.resources = AppResources(pool=app.state.pool, redis=app.state.redis_client, )


async def table():
    await create_table_users(app=app)


def get_redis(request: Request) -> Redis:
    return request.app.state.redis_client
