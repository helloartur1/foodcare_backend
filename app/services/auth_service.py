import uuid
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from app.database import get_auth_data

from app.models import User
from app.schemas import UserCreate  # Pydantic-схема для регистрации

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
        """Хеширует пароль"""
        truncated = password.encode('utf-8')[:72].decode('utf-8', 'ignore')
        return pwd_context.hash(truncated)

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Проверяет пароль"""
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta) -> str:
        """Создает JWT токен"""
        to_encode = data.copy()
        expires_delta = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expires_delta})
        auth_data = get_auth_data()
        encode_jwt = jwt.encode(to_encode, auth_data['secret_key'], algorithm=auth_data['algorithm'])
        return encode_jwt

    @staticmethod
    def verify_token(token: str):
        """Проверяет JWT токен"""
        auth_data = get_auth_data()
        try:
            payload = jwt.decode(token, auth_data['secret_key'], algorithms=[auth_data['algorithm']])

            # Дополнительная проверка срока действия
            exp = payload.get("exp")
            if exp and datetime.utcnow() > datetime.fromtimestamp(exp):
                return False  # Токен просрочен
            return payload

        except JWTError as e:
            print(f"Token verification failed: {e}")
            return False

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        existing_user = db.query(User).filter(User.user_login == user_data.user_login).first()
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
