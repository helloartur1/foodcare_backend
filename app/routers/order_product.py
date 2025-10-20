from pydantic import UUID4
from datetime import date

from app.ProductsDAO.ordersproducts import OrdersProductsDAO
from fastapi import APIRouter
from app.decorator import handle_api_exceptions
from typing import Optional

app = APIRouter()


@app.get("/get_all_orders_products")
@handle_api_exceptions
def get_all_order_products():
    return OrdersProductsDAO.select_all_orders_products()


@app.get("/get_order_product_by_id")
@handle_api_exceptions
def get_order_product_by_id(UUID: UUID4):
    return OrdersProductsDAO.select_order_product_by_id(UUID)


@app.post("/create_new_order_product")
@handle_api_exceptions
def create_order_product(id_order: UUID4, id_product: UUID4, product_date_end: date,
                         product_date_start: Optional[date] = None):
    return OrdersProductsDAO.create_new_order_product(id_order, id_product, product_date_start, product_date_end)


@app.patch("/update_order_product")
@handle_api_exceptions
def update_order_product(order_product_id: UUID4, id_order: UUID4, id_product: UUID4, product_date_end: date,
                         product_date_start: Optional[date] = None):
    return OrdersProductsDAO.update_order_product_by_id(order_product_id, id_order, id_product,
                                                        product_date_end, product_date_start)


@app.delete("/delete_order_product_by_id")
@handle_api_exceptions
def delete_order_product_by_id(UUID: UUID4):
    return OrdersProductsDAO.delete_order_product_by_id(UUID)
