from pydantic import BaseModel
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
    user_login: str
    password: str
    user_name: str



class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username :Optional[str] = None