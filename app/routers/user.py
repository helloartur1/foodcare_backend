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
            detail="Неправильный email или пароль",
        )

    access_token_expires = timedelta(minutes=30)
    access_token = AuthService.create_access_token(
        data={"user_id": str(user.user_id), "user_login": user.user_login},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}