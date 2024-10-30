
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = timedelta(days=1)):
    to_encode = data.copy()
    expire = datetime.now() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.api.secret, algorithm=settings.api.algorithm)
    return encoded_jwt


def verify_token(token: str) -> dict:
    payload = jwt.decode(token, settings.api.secret, algorithms=[settings.api.algorithm])
    return payload


async def get_current_user(
        token: str=Depends(oauth2_scheme),
    ):
    from container.get_user_repository import get_user_repository

    payload = verify_token(token=token)
    user_id: str = payload.get("id")

    user = get_user_repository().get_by_id(user_id=user_id)
    if user: return user
    return None