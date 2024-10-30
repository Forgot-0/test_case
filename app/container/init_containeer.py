from functools import lru_cache

from redis.asyncio import Redis, from_url
from punq import Container, Scope

from db.database import Database
from repositories.matсh import SQLMathcRepository
from repositories.user import SQLUserRepository
from services.email import EmailService
from services.match import LimitMatchService, MatchService
from services.user import CacheUserService, UserService
from core.config import settings



@lru_cache(1)
def init_container() -> Container:
    return _init_container()

def init_redis():
    redis = from_url(f"redis://{settings.redis.host}:{settings.redis.port}", decode_responses=True)
    return redis


def init_email_service():
    return EmailService(
        smtp_server=settings.email.server,
        smtp_port=settings.email.port,
        email=settings.email.username,
        password=settings.email.password
    )

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
    container.register(CacheUserService)


    container.register(EmailService, factory=init_email_service, scope=Scope.singleton)

    container.register(SQLUserRepository)
    container.register(UserService)

    container.register(SQLMathcRepository)
    container.register(MatchService)
    return container