from fastapi import APIRouter, HTTPException
from typing import List

from app.order.dao import OrderDAO
from app.order.schemas import SOrder, SOrderCreate, SOrderStatusUpdate

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"],
)


@router.get("", response_model=List[SOrder])
async def get_orders():
    orders = await OrderDAO.get_all_orders()
    return [SOrder(**order) for order in orders]


@router.post("", response_model=SOrder)
async def create_order(order: SOrderCreate):
    try:
        return await OrderDAO.create_order(order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}", response_model=SOrder)
async def get_order(order_id: int):
    try:
        order = await OrderDAO.get_order(order_id)
        return SOrder(**order)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.patch("/{order_id}/status", response_model=SOrder)
async def update_order_status(order_id: int, status_update: SOrderStatusUpdate):
    try:
        return await OrderDAO.update_order_status(order_id, status_update.status)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
