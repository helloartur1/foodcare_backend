from pydantic import UUID4
from fastapi.middleware.cors import CORSMiddleware
from app.gpt import generate_recipes
from app.ProductsDAO.typesproducts import ProductsTypesDAO
from app.routers import orders, products, products_types, user, order_product
from fastapi import FastAPI

app = FastAPI()

app.include_router(user.app, tags=["User"])

app.include_router(products_types.app, tags=["ProductTypes"])

app.include_router(products.app, tags=["Products"])

app.include_router(orders.app, tags=["Orders"])

app.include_router(order_product.app, tags=["OrderProducts"])

app.include_router(generate_recipes.app, tags = ["GPT"])