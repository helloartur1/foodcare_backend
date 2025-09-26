from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
from app.database import SessionLocal
from app.models import ProductType

class ProductsTypesDAO:

    @staticmethod
    def get_all_products_types():
        with SessionLocal() as session:
            query = select(ProductType)
            result = session.execute(query).scalars().all()
            return result