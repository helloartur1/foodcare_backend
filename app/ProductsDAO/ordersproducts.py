from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy import select, insert, update, delete
from app.database import SessionLocal
from app.decorator import handle_db_exceptions
from app.models import OrderProduct, Product, Order
from datetime import date
from sqlalchemy.orm import Session


class OrdersProductsDAO:
    @staticmethod
    @handle_db_exceptions
    def select_all_orders_products():
        with SessionLocal() as Session:
            query = select(OrderProduct)
            result = Session.execute(query).scalars().all()
            return result

    @staticmethod
    @handle_db_exceptions
    def select_order_product_by_id(UUID: UUID4):
        with SessionLocal() as Session:
            query = select(OrderProduct).where(OrderProduct.order_product_id == UUID)
            result = Session.execute(query).scalars().one()
            return result

    @staticmethod
    @handle_db_exceptions
    def create_new_order_product(id_order: UUID4,
                                 id_product: UUID4,
                                 product_date_start: date,
                                 product_date_end: date):
        with SessionLocal() as Session:
            # Проверка на существование продукта
            if id_product:
                existing_product = Session.execute(
                    select(Product).where(
                        Product.product_id == id_product
                    )
                ).scalar_one_or_none()
                if not existing_product:
                    raise HTTPException(
                        status_code=400,
                        detail=f"This id_product does not exist"
                    )

            # Проверка на существование заказа
            if id_order:
                existing_order = Session.execute(
                    select(Product).where(
                        Order.order_id == id_order
                    )).scalar_one_or_none()
                if not existing_order:
                    raise HTTPException(
                        status_code=400,
                        detail=f"This id_order does not exist"
                    )
            query = insert(OrderProduct).values(id_order=id_order, id_product=id_product,
                                                product_date_start=product_date_start,
                                                product_date_end=product_date_end)
            result = Session.execute(query)
            Session.commit()
            return {
                "status": "success",
                "message": f"Order Products for order '{id_order}' created"
            }

    @staticmethod
    @handle_db_exceptions
    def update_order_product_by_id(UUID: UUID4,
                                   id_order: UUID4,
                                   id_product: UUID4,
                                   product_date_start: date,
                                   product_date_end: date):
        with SessionLocal() as Session:

            # Проверка на существование продукта
            if id_product:
                existing_product = Session.execute(
                    select(Product).where(
                        Product.product_id == id_product
                    )
                ).scalar_one_or_none()
                if not existing_product:
                    raise HTTPException(
                        status_code=400,
                        detail=f"This id_product does not exist"
                    )

            # Проверка на существование заказа
            if id_order:
                existing_order = Session.execute(
                    select(Product).where(
                        Order.order_id == id_order
                    )).scalar_one_or_none()
                if not existing_order:
                    raise HTTPException(
                        status_code=400,
                        detail=f"This id_order does not exist"
                    )

            query = update(OrderProduct).where(OrderProduct.order_product_id == UUID).values(id_order=id_product,
                                                                                             id_product=id_product,
                                                                                             product_date_start=product_date_start,
                                                                                             product_date_end=product_date_end)
            result = Session.execute(query)
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=404,
                    detail="ProductOrder not found"
                )
            Session.commit()
            return {
                "status": "success",
                "message": f"ProductOrder with UUID '{UUID}' updated successfully",
            }

    @staticmethod
    @handle_db_exceptions
    def delete_order_product_by_id(UUID: UUID4):
        with SessionLocal() as Session:
            existing_order_product = Session.execute(
                select(Product).where(OrderProduct.order_product_id == UUID)
            ).scalar_one_or_none()

            if not existing_order_product:
                raise HTTPException(
                    status_code=400,
                    detail=f"ProductOrder with ID '{UUID}' does not exist"
                )

            query = delete(Product).where(OrderProduct.order_product_id == UUID)
            result = Session.execute(query)
            Session.commit()

            return {
                "status": "success",
                "message": f"ProductOrder with UUID '{UUID}' deleted successfully",
            }
