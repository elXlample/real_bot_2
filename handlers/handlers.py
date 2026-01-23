from database.database import add_user, check_user
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from fastapi import Depends
from resources.resources import get_resources
from resources import AppResources

basic_router = Router()


@basic_router.message(Command(commands="start"))
async def start_comm(
    message: Message, resources: AppResources = Depends(get_resources)
):
    if check_user():
        await message.answer("hello!")
    else:
        await add_user(resources=resources)


@basic_router.message()
async def basic_message(message: Message):
    from main import app

    storage = app.state.redis_client
    content = message.text
    await storage.set("user_msg", content)
    value_str = await storage.get("user_msg")
    value_str = value_str.decode()

    await message.answer(text=f"Saved value:{value_str}!")


# npx neonctl@latest init
