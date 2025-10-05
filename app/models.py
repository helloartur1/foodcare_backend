from sqlalchemy import Column, Integer, String, Date, Boolean, text
from .database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class ProductType(Base):
    __tablename__ = "T_ProductTypes"
    prodtype_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prodtype_name = Column(String)


class User(Base):
    __tablename__ = "T_Users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_login = Column(String, nullable=False)
    user_password = Column(String, nullable=False)
    user_name = Column(String, nullable=False)
