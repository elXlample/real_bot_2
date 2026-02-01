from aiogram import BaseMiddleware
from aiogram.types import Message
from dependencies.deps import AppResources
import logging

logger = logging.getLogger(__name__)


class ResourcesMiddleware(BaseMiddleware):
    def __init__(self, resources: AppResources):
        self.resources = resources
        super().__init__()
        logger.info("middleware initialized")

    async def __call__(self, handler, event: Message, data: dict):
        # сюда кладём resources
        data["resources"] = self.resources
        logger.info("middleware called")

        return await handler(event, data)
