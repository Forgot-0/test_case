from dataclasses import dataclass

from repositories.matсh import SQLMathcRepository
from repositories.user import SQLUserRepository


@dataclass
class MatchService:
    user_repository: SQLUserRepository
    mathc_repositpry: SQLMathcRepository

