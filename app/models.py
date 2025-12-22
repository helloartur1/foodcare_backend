from sqlalchemy import Column, ForeignKey, String, Date, Float, BigInteger
from sqlalchemy.orm import relationship
from .database import Base
import uuid
from sqlalchemy.dialects.postgresql import UUID


class ProductType(Base):
    __tablename__ = "T_ProductTypes"

    prodtype_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    prodtype_name = Column(String)

    product = relationship("Product", back_populates="prodtype")


class User(Base):
    __tablename__ = "T_Users"

    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_login = Column(String, nullable=False)
    user_password = Column(String, nullable=False)
    user_name = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user")



class Order(Base):
    __tablename__ = "T_Orders"

    order_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_user = Column(UUID(as_uuid=True), ForeignKey('T_Users.user_id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    order_date = Column(Date, nullable=False)

    user = relationship("User", back_populates="orders")
    order_products = relationship("OrderProduct", back_populates="orders")


class Product(Base):
    __tablename__ = "T_Products"

    product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String, nullable=False)
    product_thumbnail = Column(String, nullable=True)
    product_type = Column(UUID(as_uuid=True), ForeignKey('T_ProductTypes.prodtype_id', ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    product_desc = Column(String, nullable=True)
    product_rating = Column(Float, nullable=True)
    product_barcode = Column(BigInteger, nullable=False)

    prodtype = relationship("ProductType", back_populates="product")
    order_product = relationship("OrderProduct", back_populates="products")


class OrderProduct(Base):
    __tablename__ = "T_OrdersProducts"

    order_product_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    id_order = Column(UUID(as_uuid=True), ForeignKey('T_Orders.order_id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    id_product = Column(UUID(as_uuid=True), ForeignKey('T_Products.product_id', ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    product_date_start = Column(Date, nullable=True)
    product_date_end = Column(Date, nullable=False)

    orders = relationship("Order", back_populates="order_products")
    products = relationship("Product", back_populates="order_product")

