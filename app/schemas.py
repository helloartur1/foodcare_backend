from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import date, timedelta
from uuid import UUID
import re


class ProductTypeDTO(BaseModel):
    prodtype_id: UUID
    prodtype_name: str = Field(min_length=1, max_length=100, description="Название типа продукта от 1 до 100 символов")
    
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
    password: str = Field(min_length=6, max_length=100, description="Пароль от 6 до 100 символов + валидация")
    user_name: str = Field(default=..., min_length=1, max_length=50, description="Имя пользователя, от 1 до 50 символов")

    @field_validator("password")
    @classmethod
    def password_validation(cls, value:str) -> str:
        if not re.match(r'^[A-Z][a-zA-Z0-9]*$', value):
            raise ValueError("Пароль должен содержать только латинские символы, цифры и начинаться с заглавной буквы")
        return value

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
    product_name: str = Field(min_length=1, max_length=100)
    product_thumbnail: Optional[str] = Field(None, max_length=255)
    product_type: Optional[UUID] = None
    product_desc: Optional[str] = Field(None, max_length=255)
    product_rating: Optional[float] = None
    product_barcode: int

    model_config = {"from_attributes": True}


class OrderProductDTO(BaseModel):
    order_product_id: UUID
    product_date_start: Optional[date]
    product_date_end: date

    model_config = {"from_attributes": True}

class OrderProductCreate(BaseModel):
    id_order: UUID
    id_product: UUID
    product_date_start: Optional[date]
    product_date_end: date

    @field_validator("product_date_end")
    @classmethod
    def validate_date_end(cls, value: date, info):

        values = info.data
        product_date_start = values.get("product_date_start")
        print(product_date_start, value)
        if product_date_start is not None and value <= product_date_start:
            raise ValueError("product_date_end должен быть больше product_date_start")

        if value < date.today():
            raise ValueError("product_date_end должна иметь хотя бы сегодняшнюю дату")
        
        return value

class UserFridgeItemDTO(BaseModel):
    order_product: OrderProductDTO
    product: ProductDTO