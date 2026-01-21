from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router


basic_router = Router()


@basic_router.message(Command(commands="start"))
async def start_comm(message: Message):
    await message.answer("hello!")


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
