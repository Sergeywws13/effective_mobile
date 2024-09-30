from fastapi import APIRouter

from app.product.dao import ProductDAO
from app.product.schemas import SProduct


router = APIRouter(
    prefix="/products",
    tags=["Товары"],

)


@router.get("")
async def get_product() -> list[SProduct]:
    return await ProductDAO.find_all()


@router.post("")
async def post_product(
    name_product: str,
    description: str,
    price: int,
    quantity: int
) -> SProduct:
    return await ProductDAO.create_product(ProductDAO, name_product, description, price, quantity)


@router.get("/{id}")
async def get_product_id(id: int) -> SProduct:
    return await ProductDAO.find_by_id(id)


@router.put("/{id}")
async def put_product(id: int, product: SProduct) -> SProduct:
    return await ProductDAO.update_product(id, product)


@router.delete("/{id}")
async def delete_product(id: int) -> None:
    return await ProductDAO.delete_product(id)