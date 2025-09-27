from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import engine, SessionLocal
from app.models import Base, ProductType
from app.ProductsDAO.typesproducts import ProductsTypesDAO
from typing import List, Optional
from app.schemas import ProductTypeDTO
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate
from app.services.auth_service import AuthService



app = FastAPI()

@app.get("/",response_model=List[ProductTypeDTO])
def main_test():
    types = ProductsTypesDAO.get_all_products_types()
    return types

@app.post("/register")
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        user = AuthService.register_user(db=db, user_data=user_data)
        return {"message": "Пользователь создан"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))