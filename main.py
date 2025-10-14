from pydantic import UUID4
from app.ProductsDAO.typesproducts import ProductsTypesDAO
from app.routers import orders, products, products_types, user
from fastapi import FastAPI

app = FastAPI()

app.include_router(user.app, tags=["User"])

app.include_router(products_types.app, tags=["ProductTypes"])

app.include_router(products.app, tags=["Products"])

app.include_router(orders.app, tags=["Orders"])