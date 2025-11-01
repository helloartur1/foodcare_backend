from __future__ import annotations
import openfoodfacts
import datetime as dt
from typing import Any, Dict, List
import anyio
from fastapi import HTTPException


api = openfoodfacts.API(user_agent="FoodCareBackend/1.0")
_FIELDS: List[str] = ["code",
                      "product_name", "product_name_ru", "product_name_en",
                      "brands_tags", "categories_tags_ru", "image_url"]


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


# Парсинг словаря с информацией о продуктах
def parse_off_product(off: Dict[str, Any]) -> Dict[str, Any]:
    name = (off.get("product_name")
            or off.get("product_name_ru")
            or off.get("product_name_en")).strip()

    brand = off.get("brands_tags")
    prod_type = off.get("categories_tags")
    thumbnail = (off.get("image_url") or None)
    barcode = (off.get("code") or "").strip() or None

    return {
        "name": name,
        "brand": brand,
        "product_type_name": prod_type,
        "thumbnail": thumbnail,
        "barcode": barcode,
    }


def today_date() -> dt.date:
    return dt.datetime.utcnow().date()
# res = api.product.get(code, fields=["code", "product_name", "brands_tags",
# "categories_tags_ru", "image_url", "image_small_url", "image_front_small_url"])
# product_name = 'product_name' + 'brands_tags'
# product_thumbnail = 'image_url'
# product_type = 'categories_tags'
# product_desc = ''
# product_barcode = 'code'
