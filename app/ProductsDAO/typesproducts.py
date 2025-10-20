from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, insert, update, delete
from app.database import SessionLocal
from app.decorator import handle_db_exceptions
from app.models import ProductType


class ProductsTypesDAO:
    @staticmethod
    @handle_db_exceptions
    def select_all_products_types():
        with SessionLocal() as session:
            query = select(ProductType)
            result = session.execute(query).scalars().all()
            return result
    
    @staticmethod
    @handle_db_exceptions
    def create_new_product_type(type_name: str):
        with SessionLocal() as session:
            # Нормализуем регистр: первая буква заглавная, остальные строчные
            normalized_name = type_name.capitalize()
            
            # Проверяем, существует ли уже такой тип продукта
            existing_type = session.execute(
                select(ProductType).where(ProductType.prodtype_name == normalized_name)
            ).first()
            
            if existing_type:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Product type '{normalized_name}' already exists"
                )
            
            # Создаем новый тип продукта
            query = insert(ProductType).values(prodtype_name=normalized_name)
            result = session.execute(query)
            session.commit()
            
            return {
                "status": "success",
                "message": f"Product type '{normalized_name}' created successfully",
            }
    
    @staticmethod
    @handle_db_exceptions
    def update_producttype_by_id(UUID: UUID4, new_prodtype: str):
        with SessionLocal() as session:
            # Нормализуем новое название
            normalized_name = new_prodtype.capitalize()
            
            # Проверяем, не существует ли уже типа с таким названием
            existing_type = session.execute(
                select(ProductType).where(
                    ProductType.prodtype_name == normalized_name,
                    ProductType.prodtype_id != UUID
                )
            ).scalar_one_or_none()
            
            if existing_type:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Product type '{normalized_name}' already exists"
                )
            
            query = update(ProductType).where(
                ProductType.prodtype_id == UUID
            ).values(prodtype_name=normalized_name)
            
            result = session.execute(query)
            
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=404, 
                    detail="Product type not found"
                )
            
            session.commit()
            return {
                "status": "success",
                "message": f"Product type updated to '{normalized_name}' successfully",
            }
    
    @staticmethod
    @handle_db_exceptions
    def delete_producttype_by_id(UUID: UUID4):
        with SessionLocal() as session:
            # Проверяем существование типа продукта
            existing_type = session.execute(
                select(ProductType).where(ProductType.prodtype_id == UUID)
            ).scalar_one_or_none()
            
            if not existing_type:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Product type with UUID '{UUID}' not found"
                )
            
            query = delete(ProductType).where(ProductType.prodtype_id == UUID)
            result = session.execute(query)
            session.commit()
            
            return {
                "status": "success",
                "message": f"Product type with UUID '{UUID}' deleted successfully",
            }


    @staticmethod
    @handle_db_exceptions
    def select_producttype_by_id(UUID: UUID4):
        with SessionLocal() as session:
            query = select(ProductType).where(ProductType.prodtype_id==UUID)
            result = session.execute(query).scalars().one()
            return result
