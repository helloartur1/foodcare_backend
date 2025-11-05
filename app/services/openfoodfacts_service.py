from __future__ import annotations
import openfoodfacts
import datetime as dt
from typing import Any, Dict, List
import anyio
from fastapi import HTTPException


api = openfoodfacts.API(user_agent="FoodCareBackend/1.0")
_FIELDS: List[str] = ["code",
                      "product_name", "product_name_ru", "product_name_en",
                      "brands_tags", "categories_tags_ru", "categories_tags", "image_url",
                      "ingredients_text_ru", "generic_name_ru", "ingredients_text", "generic_name"]


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


# Парсинг словаря с информацией о продуктах
def parse_off_product(off: Dict[str, Any]) -> Dict[str, Any]:
    name = (off.get("product_name")
            or off.get("product_name_ru")
            or off.get("product_name_en")
            or "").strip().capitalize()

    brand_tags = off.get("brands_tags") or []
    brand = (brand_tags[0].capitalize() if brand_tags else None)

    prod_type = (off.get("categories_tags_ru")[0] or off.get("categories_tags")[0])

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
        "product_type_name": prod_type,
        "description": description,
        "thumbnail": thumbnail,
        "barcode": barcode,
    }


def today_date() -> dt.date:
    return dt.datetime.utcnow().date()
