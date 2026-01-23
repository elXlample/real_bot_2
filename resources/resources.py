from fastapi import Depends
from fastapi import FastAPI
from resources import AppResources


def get_resources(app: FastAPI = Depends()) -> AppResources:
    return AppResources(pool=app.state.pool, redis=app.state.redis_client)
