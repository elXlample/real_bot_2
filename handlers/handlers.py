from aiogram.types import Router, Message


basic_router = Router()


@basic_router.message()
async def basic_message(message: Message):
    from main import app

    storage = app.state.redis_client
    content = message.text
    storage.set("user_msg", content)
    value_str = storage.get("user_msg").decode("utf-8")
    await message.answer(text=f"Saved value:{value_str}!")
