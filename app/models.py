from sqlalchemy import Column, Integer, String
from .database import Base

class ProductType(Base):
    __tablename__= "T_ProductTypes"
    prodtype_id = Column(Integer, primary_key= True, index=True)
    prodtype_name = Column(String)