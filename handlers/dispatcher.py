from aiogram import Dispatcher
from .handlers import basic_router as msg_router
from aiogram.fsm.storage.memory import MemoryStorage


def set_up_dispatcher():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(msg_router)
    return dp
