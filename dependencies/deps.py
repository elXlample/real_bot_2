from fastapi import Request
from dataclasses import dataclass
from psycopg_pool import AsyncConnectionPool
from redis.asyncio import Redis


@dataclass
class AppResources:
    pool: AsyncConnectionPool
    redis: Redis
    


def get_resources(request: Request) -> AppResources:
    return request.app.state.resources
