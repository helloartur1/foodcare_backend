from sqlalchemy import Column, Integer, String, Date
from .database import Base

class ProductType(Base):
    __tablename__= "T_ProductTypes"
    prodtype_id = Column(Integer, primary_key= True, index=True)
    prodtype_name = Column(String)

class User(Base):
    __tablename__="T_Users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_login = Column(String,nullable=False)
    user_password = Column(String,nullable=False)
    user_name = Column(String,nullable=False)
    user_surname = Column(String,nullable=True)
    user_patronymic = Column(String, nullable=True)
    user_birthday = Column(Date,nullable=True)
    user_sex = Column(String, nullable=True)