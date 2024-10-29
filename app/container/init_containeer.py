from functools import lru_cache
from punq import Container, Scope

from db.database import Database
from repositories.user import SQLUserRepository
from services.user import UserService
from core.config import settings



@lru_cache(1)
def init_container() -> Container:
    return _init_container()



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
    container.register(SQLUserRepository)
    
    container.register(UserService)
    return container