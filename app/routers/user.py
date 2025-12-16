from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserDTO, UserLogin, ProductTypeDTO
from app.services.auth_service import AuthService
from datetime import timedelta
from app.models import User

app = APIRouter()


@app.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = AuthService.register_user(db=db, user_data=user_data)
        return {"message": "Пользователь создан"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/login", summary="User Login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.user_login == user_data.user_login).first()

    if not user or not AuthService.verify_password(user_data.password, user.user_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неправильный логин или пароль",
        )

    # access token
    access_token = AuthService.create_access_token(
        data={"user_id": str(user.user_id), "user_login": user.user_login}
    )

    # refresh token
    refresh_token = AuthService.create_refresh_token(
        data={"user_id": str(user.user_id)}
    )

    return {
        "user_id": user.user_id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@app.post("/refresh", summary="Update access token")
def refresh_token(refresh_token: str):
    payload = AuthService.verify_refresh_token(refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный или просроченный refresh токен",
        )

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(status_code=400, detail="Некорректный токен")

    new_access = AuthService.create_access_token(
        data={"user_id": user_id}
    )

    return {
        "access_token": new_access,
        "token_type": "bearer"
    }
