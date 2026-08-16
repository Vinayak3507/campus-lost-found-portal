""""Purpose:
Handle security-related utilities.

Responsibilities:
password hashing
password verification
JWT token creation
JWT token decoding

---> Keeping this separate avoids repeating security logic everywhere."""

from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from app.config.settings import (JWT_SECRET_KEY,JWT_ALGORITHM,JWT_ACCESS_TOKEN_EXPIRE_MINUTES,)
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(data: dict,expires_delta: timedelta | None = None) -> str:

    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta

    else:
        expire = (datetime.now(timezone.utc)+ timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,JWT_SECRET_KEY,algorithm=JWT_ALGORITHM)

    return encoded_jwt

def decode_access_token(token: str) -> dict:

    return jwt.decode(token,JWT_SECRET_KEY,algorithms=[JWT_ALGORITHM],)
