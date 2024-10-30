from dataclasses import dataclass

from exeptions.base import ApplicationException


@dataclass(eq=False)
class MutuallyAlreadyException(ApplicationException):
    error_code = 409

    @property
    def message(self):
        return f'Вы уже оценили друг друга'


@dataclass(eq=False)
class MutuallySelfExeption(ApplicationException):
    error_code = 403

    @property
    def message(self):
        return f'Нельзя оценить самого себя'


@dataclass(eq=False)
class LimitMatchExeption(ApplicationException):
    error_code = 403

    @property
    def message(self):
        return f'Вы привысили лимит оценки'


@dataclass(eq=False)
class MatchAlreadyExeption(ApplicationException):
    error_code = 409

    @property
    def message(self):
        return f'Вы уже оценивали этого пользователя'

