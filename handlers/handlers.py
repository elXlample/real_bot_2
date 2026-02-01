from database.database import add_user
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from fastapi import Depends
from dependencies.deps import AppResources, get_resources


basic_router = Router()


@basic_router.message(Command(commands="start"))
async def start_comm(
    message: Message, resources: AppResources = Depends(get_resources)
):
    id = message.from_user.id
    username = message.from_user.username
    is_alive = True
    result = await add_user(
        resources=resources, user_id=id, username=username, is_alive=is_alive
    )
    await message.answer(text=result)


@basic_router.message()
async def basic_message(
    message: Message, resources: AppResources = Depends(get_resources)
):
    from main import app

    storage = resources.redis
    content = message.text
    await storage.set("user_msg", content)
    value_str = await storage.get("user_msg")
    value_str = value_str.decode()

    await message.answer(text=f"Saved value:{value_str}!")


# npx neonctl@latest init
