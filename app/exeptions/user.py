from dataclasses import dataclass

from exeptions.base import ApplicationException


@dataclass(eq=False)
class NotFoundUserExeption(ApplicationException):
    user_id: int
    error_code = 404

    @property
    def message(self):
        return f'User not found by id {self.user_id}'


@dataclass(eq=False)
class EmailAlreadyExistExeption(ApplicationException):
    email: str
    error_code = 409

    @property
    def message(self):
        return f'A user with the "{self.email}" email already exists'


@dataclass(eq=False)
class WrongPasswordExeption(ApplicationException):
    error_code = 401

    @property
    def message(self):
        return 'Wrong password'