from pydantic import UUID4
from app.ProductsDAO.typesproducts import ProductsTypesDAO
from app.ProductsDAO.products import ProductsDAO
from typing import List
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.decorator import handle_api_exceptions
from app.schemas import UserCreate, UserDTO, UserLogin, ProductTypeDTO
from app.services.auth_service import AuthService
from datetime import timedelta
from typing import Optional
from app.models import User


app = FastAPI()


@app.get("/getallproductstypes", response_model=List[ProductTypeDTO])
@handle_api_exceptions
def get_all_products_types():
    return ProductsTypesDAO.select_all_products_types()


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

##CRUD FOR TABLE T_PRODUCTSTYPE
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

##CRUD FOR TABLE T_PRODUCTS
@app.get("/getallproducts")
@handle_api_exceptions
def get_all_products():
    return ProductsDAO.select_all_products()

@app.get("/getproductbyid")
@handle_api_exceptions
def get_product_by_id(UUID:UUID4):
    return ProductsDAO.select_product_by_id(UUID)

@app.post("/create_new_product")
@handle_api_exceptions
def create_product(product_name: str, product_barcode: int, product_thumbnail: Optional[str] = None, product_type: Optional[UUID4] = None, product_desc: Optional[str] = None, product_rating: Optional[float] = None):
    return ProductsDAO.create_new_product(product_name, product_thumbnail, product_type, product_desc, product_rating, product_barcode)

@app.patch("/updateproduct")
@handle_api_exceptions
def update_product(product_id:UUID4, product_name: str, product_barcode: int, product_thumbnail: Optional[str] = None, product_type: Optional[UUID4] = None, product_desc: Optional[str] = None, product_rating: Optional[float] = None):
    return ProductsDAO.update_product_by_id(product_id, product_name, product_thumbnail, product_type, product_desc, product_rating, product_barcode)

@app.delete("/deleteproductbyid")
@handle_api_exceptions
def delete_product_by_id(UUID:UUID4):
    return ProductsDAO.delete_product_by_id(UUID)