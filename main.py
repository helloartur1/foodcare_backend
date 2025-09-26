from fastapi import FastAPI
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.database import engine, SessionLocal
from app.models import Base, ProductType
from app.ProductsDAO.typesproducts import ProductsTypesDAO
from typing import List, Optional
from app.schemas import ProductTypeDTO
app = FastAPI()

@app.get("/",response_model=List[ProductTypeDTO])
def main_test():
    types = ProductsTypesDAO.get_all_products_types()
    return types