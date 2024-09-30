from datetime import date
from pydantic import BaseModel



class SOrderStatusUpdate(BaseModel):
    status: str

    class Config:
        from_attributes = True

        
class SOrderItemCreate(BaseModel):
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class SOrderCreate(BaseModel):
    date_create: date
    status: str
    items: list[SOrderItemCreate]

    class Config:
        from_attributes = True


class SOrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int

    class Config:
        from_attributes = True


class SOrder(BaseModel):
    id: int
    date_create: date
    status: str
    items: list[SOrderItem]

    class Config:
        from_attributes = True


