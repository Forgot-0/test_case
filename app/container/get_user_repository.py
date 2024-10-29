

from container.init_containeer import init_container
from repositories.user import SQLUserRepository



def get_user_repository() -> SQLUserRepository:
    container = init_container()
    return container.resolve(SQLUserRepository)