from __future__ import annotations
import re
import openfoodfacts
import datetime as dt
from typing import Any, Dict, List
import anyio
from fastapi import HTTPException
from app.database import SessionLocal
from app.models import ProductType
from sqlalchemy import select

api = openfoodfacts.API(user_agent="FoodCareBackend/1.0")
_FIELDS: List[str] = ["code",
                      "product_name", "product_name_ru", "product_name_en",
                      "brands_tags", "categories_tags_ru", "categories_tags", "image_url",
                      "ingredients_text_ru", "generic_name_ru", "ingredients_text", "generic_name"]
russian_pattern = re.compile(r"[А-Яа-яЁё]")


# Получение данных о продукте по шрихкоду из OpenFoodFacts
async def fetch_off_product(barcode: str) -> Dict[str, Any]:
    try:
        product = await anyio.to_thread.run_sync(
            lambda: api.product.get(barcode, fields=_FIELDS)
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"OpenFoodFacts SDK error: {e}") from e

    if not product or not isinstance(product, dict) or not product.get("code"):
        raise HTTPException(status_code=404, detail="Продукт по этому штрихкоду в OpenFoodFacts не найден")

    return product


def normalize_tag_to_name(tag: str):
    part = tag.split(":", 1)[-1]
    part = part.replace("-", " ").replace("_", " ").strip()
    return part.capitalize()


def find_matching_product_type(prod_types: List[str]):
    normalized_prod_types = [
        pt.strip() for pt in prod_types if pt and pt.strip()
    ]
    if not normalized_prod_types:
        return None

    with SessionLocal() as session:
        query = select(ProductType)
        db_product_types = session.execute(query).scalars().all()

    db_type_names = {
        pt.prodtype_name.lower(): pt.prodtype_name
        for pt in db_product_types
        if pt.prodtype_name
    }
    # Поиск среди типов продуктов на русском языке
    for prod_type in normalized_prod_types:
        if not russian_pattern.search(prod_type):
            continue
        key = prod_type.lower()
        if key in db_type_names:
            return db_type_names[key]
    # Если не найдены совпадения, возвращаем первый тип продукта на русском
    for prod_type in normalized_prod_types:
        if russian_pattern.search(prod_type):
            return prod_type
    # Если нет ничего на русском, возвращаем первый тип продукта
    return normalized_prod_types[0]


# Парсинг словаря с информацией о продуктах
def parse_off_product(off: Dict[str, Any]) -> Dict[str, Any]:
    name = (off.get("product_name")
            or off.get("product_name_ru")
            or off.get("product_name_en")
            or "").strip().capitalize()

    brand_tags = off.get("brands_tags") or []
    brand = (brand_tags[0].capitalize() if brand_tags else None)

    prod_types = off.get("categories_tags_ru", []) + off.get("categories_tags", [])
    matched_type = find_matching_product_type(prod_types)

    description = (
            off.get("ingredients_text_ru")
            or off.get("generic_name_ru")
            or off.get("ingredients_text")
            or off.get("generic_name")
        )
    thumbnail = (off.get("image_url") or None)
    barcode = (off.get("code") or "").strip() or None

    return {
        "name": f"{name} {brand}".strip() if name and brand else (name or brand),
        "product_type_name": matched_type,
        "description": description,
        "thumbnail": thumbnail,
        "barcode": barcode,
    }


def today_date() -> dt.date:
    return dt.datetime.utcnow().date()

#Методы для обрезки описания
def normalize_product_desc(desc:str)->str:
    if not desc:
        return ""
    if len(desc) >= 254:
        return desc[0:251] + "..."
    return desc