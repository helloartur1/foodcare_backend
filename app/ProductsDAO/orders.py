from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select, insert, update, delete
from app.database import SessionLocal
from app.decorator import handle_db_exceptions
from app.models import Order, User
from datetime import date
class OrdersDAO:
    
    @staticmethod
    def testtest():
        with SessionLocal() as session:
            query = select(User)
            return session.execute(query).scalars().all()
    @staticmethod
    @handle_db_exceptions
    def create_new_order(user_id: UUID4, order_date: date):
        with SessionLocal() as session:
            query = insert(Order).values(id_user=user_id,order_date = order_date)
            result = session.execute(query)
            session.commit()
            return{
                "status":"success",
                "message":f"Order for user '{user_id}' created"
            }
    @staticmethod
    @handle_db_exceptions
    def select_all_orders():
        with SessionLocal() as session:
            query = select(Order)
            result = session.execute(query).scalars().all()
            return result
    
    @staticmethod
    @handle_db_exceptions
    def select_all_orders_by_user_id(user_id:UUID4):
        with SessionLocal() as session:
            query = select(Order).where(Order.id_user==user_id)
            result = session.execute(query).scalars().one()
            return result
    
    @staticmethod
    @handle_db_exceptions
    def update_order_by_id(order_id: UUID4,date_order: date):
        with SessionLocal() as session:
            existing_order = session.execute(
                select(Order).where(Order.order_id == order_id)
            ).scalar_one_or_none()

            if not existing_order:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Order with UUID '{order_id}' not found"
                )
            
            query = update(Order).where(Order.order_id==order_id).values(order_date=date_order)
            result = session.execute(query)
            session.commit()
            return{
                "status" : "success",
                "message" : f"Order '{order_id}' changed"
            }
        
    @staticmethod
    @handle_db_exceptions
    def delete_order_by_id(order_id: UUID4):
        with SessionLocal() as session:
            existing_type = session.execute(
                select(Order).where(Order.order_id == order_id)
            ).scalar_one_or_none()
            
            if not existing_type:
                raise HTTPException(
                    status_code=404, 
                    detail=f"Order with UUID '{order_id}' not found"
                )
            
            query = delete(Order).where(Order.order_id == order_id)
            result = session.execute(query)
            session.commit()

            return {
                "status": "success",
                "message": f"Order with UUID '{order_id}' deleted successfully",
            }