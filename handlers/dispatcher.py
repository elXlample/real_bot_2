from aiogram import Dispatcher
from .handlers import basic_router as msg_router


def set_up_dispatcher():
    dp = Dispatcher()
    dp.include_router(msg_router)
    return dp
