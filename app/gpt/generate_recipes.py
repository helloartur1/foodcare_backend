from fastapi import APIRouter
from openai import OpenAI
from dotenv import load_dotenv
import os
from app.schemas import ProductList
load_dotenv()

KEY = os.getenv("KEY_FOR_GPT")

client = OpenAI(api_key=KEY,base_url="https://api.deepseek.com")


app = APIRouter(prefix="/GPT")


@app.post("/generate_recipes")
def generate_recipes(data:ProductList):

    products = ", ".join(data.products)

    system_prompt = (
        "Ты опытный шеф повар. Тебе дается ряд продуктов от пользователя."
        "Предложи минимум 3 блюда, которые можно приготовить из этих продуктов."
        "Необязательно использовать все продукты при приготовлении."
    )

    message = [
        {"role" : "system", "content": system_prompt},
        {"role" : "user", "content": f"Пользовательские продукты: {products}"}
    ]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=message,
        temperature=0.7
    )

    ans = response.choices[0].message.content
    return ans