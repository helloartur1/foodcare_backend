from pydantic import UUID4
from app.ProductsDAO.products import ProductsDAO
from typing import List
from fastapi import APIRouter

from app.decorator import handle_api_exceptions

from typing import Optional


app = APIRouter()


@app.get("/getallproducts")
@handle_api_exceptions
def get_all_products():
    return ProductsDAO.select_all_products()


@app.get("/getproductbyid")
@handle_api_exceptions
def get_product_by_id(UUID:UUID4):
    return ProductsDAO.select_product_by_id(UUID)


@app.post("/create_new_product")
@handle_api_exceptions
def create_product(product_name: str, product_barcode: int, product_thumbnail: Optional[str] = None,
                   product_type: Optional[UUID4] = None, product_desc: Optional[str] = None, product_rating: Optional[float] = None):
    return ProductsDAO.create_new_product(product_name, product_thumbnail, product_type, product_desc, product_rating, product_barcode)


@app.patch("/updateproduct")
@handle_api_exceptions
def update_product(product_id:UUID4, product_name: str, product_barcode: int, product_thumbnail: Optional[str] = None,
                   product_type: Optional[UUID4] = None, product_desc: Optional[str] = None, product_rating: Optional[float] = None):
    return ProductsDAO.update_product_by_id(product_id, product_name, product_thumbnail, product_type, product_desc, product_rating, product_barcode)


@app.delete("/deleteproductbyid")
@handle_api_exceptions
def delete_product_by_id(UUID:UUID4):
    return ProductsDAO.delete_product_by_id(UUID)
