from fastapi import APIRouter
from openai import OpenAI
from dotenv import load_dotenv
import os
from ..routers.orders import OrdersDAO
from pydantic import UUID4
from app.schemas import ProductList
load_dotenv()

KEY = os.getenv("KEY_FOR_GPT")

client = OpenAI(api_key=KEY,base_url="https://api.deepseek.com")


app = APIRouter(prefix="/GPT")


@app.post("/generate_recipes")
def generate_recipes(user_id: UUID4):
    products_data = OrdersDAO.user_fridge(user_id)
    
    # Извлекаем только названия продуктов из объектов DTO
    product_names = [item.product.product_name for item in products_data]
    products_string = ", ".join(product_names)

    system_prompt = (
        "Ты опытный шеф повар. Тебе дается ряд продуктов от пользователя. Не нужно добавлять продукты, которые тебе не дал пользователь."
        "Предложи минимум 3 блюда, которые можно приготовить из этих продуктов."
        "Необязательно использовать все продукты при приготовлении." 
        "Данные нужно вернуть в формате JSON:" 
        "complexity: {сложность приготовления блюда}," 
        "time : {время приготовления блюда}," 
        "recipe {рецепт по которому готовить}" 
    )

    message = [
        {"role" : "system", "content": system_prompt},
        {"role" : "user", "content": f"Пользовательские продукты: {products_string}"}
    ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=message,
        temperature=0.7
    )

    ans = response.choices[0].message.content
    return ans