from fastapi import FastAPI, Query, Depends
from typing import Optional
from datetime import date
from pydantic import BaseModel


from app.order.router import router as router_order
from app.product.router import router as router_product

app = FastAPI()

app.include_router(router_order)
app.include_router(router_product)

