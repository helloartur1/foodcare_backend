from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date
from uuid import UUID


class ProductTypeDTO(BaseModel):
    prodtype_id: UUID
    prodtype_name: Optional[str]
    
    class Config:
        orm_mode = True 


class UserDTO(BaseModel):
    user_id: UUID
    user_login: str
    user_name: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    user_login: EmailStr = Field(default=..., description="Электронная почта пользователя")
    password: str
    user_name: str = Field(default=..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")


class UserLogin(BaseModel):
    user_login: EmailStr = Field(default=..., description="Электронная почта пользователя")
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[str] = None
    user_login: Optional[str] = None

class ProductDTO(BaseModel):
    product_id: UUID
    product_name: str
    product_thumbnail: Optional[str] = None
    product_type: Optional[UUID] = None
    product_desc: Optional[str] = None
    product_rating: Optional[float] = None
    product_barcode: int

    model_config = {"from_attributes": True}

class OrderProductDTO(BaseModel):
    order_product_id: UUID
    product_date_start: date
    product_date_end: Optional[date]

    model_config = {"from_attributes": True}


class UserFridgeItemDTO(BaseModel):
    order_product: OrderProductDTO
    product: ProductDTO