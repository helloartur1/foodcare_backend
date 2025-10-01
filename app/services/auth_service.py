import uuid
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate  # Pydantic-схема для регистрации

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:

    @staticmethod
    def hash_password(password: str) -> str:
        truncated = password.encode('utf-8')[:72].decode('utf-8', 'ignore')
        return pwd_context.hash(truncated)
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
