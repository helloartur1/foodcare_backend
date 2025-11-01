from __future__ import annotations
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal
from app.services.openfoodfacts_service import fetch_off_product, parse_off_product, today_date
from app.ProductsDAO.products import ProductsDAO
from app.ProductsDAO.typesproducts import ProductsTypesDAO
from app.ProductsDAO.orders import OrdersDAO
from app.ProductsDAO.ordersproducts import OrdersProductsDAO
from app import models as m
from uuid import UUID
from app.schemas import (
    BarcodeScanIn, ScanResultOut, OffProductOut,
    OrderProductCreate, OrderProductDTO
)

app = APIRouter(prefix="/openfoodfacts", tags=["OpenFoodFacts"])


@app.post("/scan", response_model=ScanResultOut, summary="Скан штрихкода → найти/создать ProductType, Product и Order")
async def scan_barcode(payload: BarcodeScanIn):

    off_raw = await fetch_off_product(payload.barcode)
    parsed = parse_off_product(off_raw)

    if not parsed["barcode"]:
        raise HTTPException(status_code=422, detail="В ответе OpenFoodFacts отсутствует barcode")
    try:
        barcode_int = int(parsed["barcode"])
    except ValueError:
        raise HTTPException(status_code=422, detail="Некорректный формат barcode (не число)")

    prodtype, created_pt = ProductsTypesDAO.get_or_create_producttype(parsed["product_type_name"])

    product = ProductsDAO.select_product_by_barcode(barcode_int)
    if not product and parsed["name"]:
        product = ProductsDAO.select_product_by_name(parsed["name"])

    created_product = False
    if not product:
        product = ProductsDAO.get_or_create_product_from_off(
            name=parsed["name"] or "Без названия",
            barcode_int=barcode_int,
            description=parsed["description"],
            thumbnail=parsed["thumbnail"],
            product_type_id=prodtype.prodtype_id
        )
        created_product = True

    # Cоздаём Order на момент скана
    order_res = OrdersDAO.create_order_for_scan(user_id=payload.user_id, when=today_date())
    order_id = UUID(order_res["order_id"])

    return ScanResultOut(
        order_id=order_id,
        product_id=product.product_id,
        created_product=created_product,
        created_product_type=created_pt,
        product=OffProductOut(
            product_id=product.product_id,
            product_name=product.product_name,
            product_barcode=product.product_barcode,
            product_thumbnail=product.product_thumbnail,
            product_desc=product.product_desc,
            product_type_name=prodtype.prodtype_name,
        ),
    )


@app.post("/orders-products", response_model=OrderProductDTO,
          summary="Сохранить срок годности: создаёт запись в T_OrdersProducts")
async def create_order_product(payload: OrderProductCreate):
    res = OrdersProductsDAO.create_with_defaults(
        id_order=payload.id_order,
        id_product=payload.id_product,
        product_date_end=payload.product_date_end,
        product_date_start=payload.product_date_start,
    )

    op = OrdersProductsDAO.select_order_product_by_id(UUID(res["order_product_id"]))
    return op
