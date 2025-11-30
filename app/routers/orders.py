from pydantic import UUID4
from app.ProductsDAO.orders import OrdersDAO
from fastapi import APIRouter
from app.decorator import handle_api_exceptions
from datetime import date
import traceback
from app.schemas import ProductDTO, UserFridgeItemDTO

app = APIRouter(prefix="/order")

@app.get("/fsdfsdfsdgsdrweerqrww")
def test():
    try:
        result = OrdersDAO.testtest()
        return result
    except UnicodeDecodeError as e:
        print("UnicodeDecodeError в /fsdfsdfsdgsdrweerqrww:", e)
        traceback.print_exc()
        raise
    except Exception as e:
        print("Другая ошибка в /fsdfsdfsdgsdrweerqrww:", e)
        traceback.print_exc()
        raise

@app.get("/getallorders")
@handle_api_exceptions
def get_all_orders():
    return OrdersDAO.select_all_orders()


@app.get("/getordersbyid")
@handle_api_exceptions
def get_order_by_user(user_id : UUID4):
    return OrdersDAO.select_all_orders_by_user_id(user_id)

@app.post("/createorder")
@handle_api_exceptions
def create_new_order(user_id : UUID4, order_date: date):
    return OrdersDAO.create_new_order(user_id,order_date)

@app.patch("/updateorder")
@handle_api_exceptions
def update_order(order_id : UUID4, order_date : date):
    return OrdersDAO.update_order_by_id(order_id,order_date)

@app.delete("/deleteorder")
@handle_api_exceptions
def delete_order(order_id : UUID4):
    return OrdersDAO.delete_order_by_id(order_id)

@app.get("/getallproductsuser",response_model=list[UserFridgeItemDTO])
@handle_api_exceptions
def get_fridge_by_user(user_id: UUID4):
    print(OrdersDAO.user_fridge(user_id))
    return OrdersDAO.user_fridge(user_id)

