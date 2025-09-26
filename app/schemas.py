from pydantic import BaseModel
from typing import Optional

class ProductTypeDTO(BaseModel):
    prodtype_id: int
    prodtype_name: Optional[str]
    

    class Config:
        orm_mode = True 