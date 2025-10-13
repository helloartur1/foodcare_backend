from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, insert, update, delete
from app.database import SessionLocal
from app.decorator import handle_db_exceptions
from app.models import Product, ProductType

class ProductsDAO:
    @staticmethod
    @handle_db_exceptions
    def select_all_products():
        with SessionLocal() as Session:
            query = select(Product)
            result = Session.execute(query).scalars().all()
            return result

    @staticmethod
    @handle_db_exceptions
    def select_product_by_id(UUID:UUID4):
        with SessionLocal() as Session:
            query = select(Product).where(Product.product_id == UUID)
            result = Session.execute(query).scalars().one()
            return result

    @staticmethod
    @handle_db_exceptions
    def create_new_product(product_name: str,
                           product_thumbnail: str, 
                           product_type: UUID4,
                           product_desc: str,
                           product_rating: float,
                           product_barcode: int):
        with SessionLocal() as Session:
            #Нормализация названия и описания продукта, если они были переданы
            normalized_name = product_name.capitalize()
            if(product_desc):
                normalized_desc = product_desc.capitalize()
            else:
                normalized_desc = product_desc
            
            #Две проверки - первая на существование типа продукта, если есть, а вторая - на существование самого продукта по названию и баркоду
            if (product_type):
                existing_product_type = Session.execute(
                    select(ProductType).where(
                        ProductType.prodtype_id == product_type
                    )   
                ).scalar_one_or_none()
                if (not existing_product_type):
                    raise HTTPException(
                        status_code=400,
                        detail=f"ProductTypeID in '{normalized_name}' does not exist"
                    )
            existing_product = Session.execute(
                select(Product).where(
                    Product.product_name == normalized_name or Product.product_barcode == product_barcode
                )
            ).scalar_one_or_none()
            
            if(existing_product):
                raise HTTPException(
                    status_code=400, 
                    detail=f"Product '{normalized_name}' already exists"
                )
            #Вставка нового продукта в таблицу T_Products
            query = insert(Product).values(product_name = normalized_name,
                                           product_thumbnail = product_thumbnail,
                                           product_type = product_type,
                                           product_desc = normalized_desc,
                                           product_rating = product_rating,
                                           product_barcode = product_barcode)
            result = Session.execute(query)
            Session.commit()
            return {
                "status": "success",
                "message": f"Product '{normalized_name}' created successfully",
            }
        
    @staticmethod
    @handle_db_exceptions
    def update_product_by_id(UUID:UUID4,
                             product_name: str,
                             product_thumbnail: str, 
                             product_type: UUID4,
                             product_desc: str,
                             product_rating: float,
                             product_barcode: int):
        with SessionLocal() as Session:
            #Нормализация названия и описания продукта, если они были переданы
            normalized_name = product_name.capitalize()
            if(product_desc):
                normalized_desc = product_desc.capitalize()
            else:
                normalized_desc = product_desc

            #Проверка на существование типа продукта
            if (product_type):
                existing_product_type = Session.execute(
                    select(ProductType).where(
                        ProductType.prodtype_id == product_type
                    )   
                ).scalar_one_or_none()
                if (not existing_product_type):
                    raise HTTPException(
                        status_code=400,
                        detail=f"ProductTypeID in '{normalized_name}' does not exist"
                    )
            #Обновление продукта в таблице T_Products
            query = update(Product).where(Product.product_id == UUID).values(product_name = normalized_name,
                                                                             product_barcode = product_barcode,
                                                                             product_thumbnail = product_thumbnail,
                                                                             product_type = product_type,
                                                                             product_desc = normalized_desc,
                                                                             product_rating = product_rating)
            result = Session.execute(query)
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=404, 
                    detail="Product not found"
                )
            Session.commit()
            return {
                "status": "success",
                "message": f"Product '{normalized_name}' updated successfully",
            }
        
    @staticmethod
    @handle_db_exceptions
    def delete_product_by_id(UUID:UUID4):
        with SessionLocal() as Session:
            existing_product = Session.execute(
                select(Product).where(Product.product_id == UUID)
            ).scalar_one_or_none()

            if (not existing_product):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Product with ID '{UUID}' does not exist"
                    )
            
            query = delete(Product).where(Product.product_id == UUID)
            result = Session.execute(query)
            Session.commit()
            
            return {
                "status": "success",
                "message": f"Product with UUID '{UUID}' deleted successfully",
            }