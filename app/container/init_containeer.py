from functools import lru_cache

from redis.asyncio import Redis, from_url
from punq import Container, Scope

from db.database import Database
from repositories.matсh import SQLMathcRepository
from repositories.user import SQLUserRepository
from services.match import LimitMatchService, MatchService
from services.user import UserService
from core.config import settings



@lru_cache(1)
def init_container() -> Container:
    return _init_container()

def init_redis():
    redis = from_url("redis://redis:6379", decode_responses=True)
    return redis

def _init_container() -> Container:
    container = Container()
    container.register(
        Database,
        scope=Scope.singleton,
        factory=lambda: Database(
            url=settings.db.url,
            ro_url=settings.db.url,
        ),
    )

    container.register(Redis, factory=init_redis, scope=Scope.singleton)
    container.register(LimitMatchService)


    container.register(SQLUserRepository)
    container.register(UserService)

    container.register(SQLMathcRepository)
    container.register(MatchService)
    return container