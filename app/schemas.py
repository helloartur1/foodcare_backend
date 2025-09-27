from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductTypeDTO(BaseModel):
    prodtype_id: int
    prodtype_name: Optional[str]
    
    class Config:
        orm_mode = True 

class UserDTO(BaseModel):
    user_id: int
    user_login: str
    user_name: str
    user_surname: Optional[str] = None
    user_patronymic: Optional[str] = None
    user_birthday: Optional[date] = None
    user_sex: Optional[str] = None

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    user_login: str
    password: str
    user_name: str
    user_surname: Optional[str] = None
    user_patronymic: Optional[str] = None
    user_birthday: Optional[date] = None
    user_sex: Optional[str] = None


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username :Optional[str] = None