from typing import List
from pydantic import UUID4
from app.ProductsDAO.typesproducts import ProductsTypesDAO
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.decorator import handle_api_exceptions
from app.schemas import UserCreate, UserDTO, UserLogin, ProductTypeDTO

app = APIRouter()


@app.get("/getallproductstypes", response_model=List[ProductTypeDTO])
@handle_api_exceptions
def get_all_products_types():
    return ProductsTypesDAO.select_all_products_types()


@app.get("/getproducttypebyid")
@handle_api_exceptions
def get_product_type_by_id(UUID: UUID4):
    return ProductsTypesDAO.select_producttype_by_id(UUID)
@app.post("/create_new_producttype")
@handle_api_exceptions
def create_producttype(new_type: str, db: Session=Depends(get_db)):
    return ProductsTypesDAO.create_new_product_type(new_type)

@app.patch("/updateproductname")
@handle_api_exceptions
def update_product_type_by_id(UUID: UUID4, new_type: str, db: Session=Depends(get_db)):
     return ProductsTypesDAO.update_producttype_by_id(UUID,new_type)
    
@app.delete("/deleteproducttype")
@handle_api_exceptions
def delete_product_type_by_id(UUID: UUID4, db: Session=Depends(get_db)):
    return ProductsTypesDAO.delete_producttype_by_id(UUID)