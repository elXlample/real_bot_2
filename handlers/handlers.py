from aiogram.types import Message, BotCommand
from aiogram import Router


basic_router = Router()


@basic_router.message(BotCommand(command="start"))
async def start_comm(message: Message):
    from main import app

    storage = app.state.redis_client
    content = message.text
    storage.set("user_msg", content)
    value_str = storage.get("user_msg").decode("utf-8")
    await message.answer(text=f"Saved value:{value_str}!")


@basic_router.message()
async def basic_message(message: Message):
    from main import app

    storage = app.state.redis_client
    content = message.text
    storage.set("user_msg", content)
    value_str = storage.get("user_msg").decode("utf-8")
    await message.answer(text=f"Saved value:{value_str}!")
