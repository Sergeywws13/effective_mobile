from pydantic import BaseModel


class SProduct(BaseModel):
    id: int
    name_product: str
    description: str
    price: int
    quantity: int

    class Config:
        from_attributes = True