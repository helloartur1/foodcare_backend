import uuid
import os
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

from app.models import User
from app.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    # ---------- PASSWORD ----------
    @staticmethod
    def hash_password(password: str) -> str:
        truncated = password.encode("utf-8")[:72].decode("utf-8", "ignore")
        return pwd_context.hash(truncated)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    # ---------- TOKEN GENERATION ----------
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        if expires_delta is None:
            expires_delta = timedelta(
                minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
            )

        expire = datetime.now(timezone.utc) + expires_delta

        to_encode = data.copy()
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            os.getenv("ACCESS_TOKEN_SECRET"),
            algorithm=os.getenv("ALGORITHM")
        )

        return encoded_jwt

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: timedelta | None = None) -> str:
        if expires_delta is None:
            expires_delta = timedelta(
                days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 30))
            )

        expire = datetime.now(timezone.utc) + expires_delta

        to_encode = data.copy()
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(
            to_encode,
            os.getenv("REFRESH_TOKEN_SECRET"),
            algorithm=os.getenv("ALGORITHM")
        )

        return encoded_jwt

    # ---------- TOKEN VERIFICATION ----------
    @staticmethod
    def verify_access_token(token: str):
        try:
            payload = jwt.decode(
                token,
                os.getenv("ACCESS_TOKEN_SECRET"),
                algorithms=[os.getenv("ALGORITHM")]
            )
            return payload
        except JWTError:
            return None

    @staticmethod
    def verify_refresh_token(token: str):
        try:
            payload = jwt.decode(
                token,
                os.getenv("REFRESH_TOKEN_SECRET"),
                algorithms=[os.getenv("ALGORITHM")]
            )
            return payload
        except JWTError:
            return None

    # ---------- USER REGISTRATION ----------
    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        existing_user = db.query(User).filter(
            User.user_login == user_data.user_login
        ).first()

        if existing_user:
            raise ValueError("Пользователь с таким логином уже существует")

        hashed_password = AuthService.hash_password(user_data.password)

        new_user = User(
            user_login=user_data.user_login,
            user_password=hashed_password,
            user_name=user_data.user_name
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return new_user
