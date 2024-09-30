from app.product.models import Product
from app.database import async_session_maker


from app.dao.base import BaseDAO
from app.product.schemas import SProduct


class ProductDAO(BaseDAO):
    model = Product


    async def create_product(
            cls,
            name_product: str,
            description: str,
            price: int,
            quantity: int
            ):
        async with async_session_maker() as session:
            new_product = Product(name_product=name_product, description=description,
                                price=price, quantity=quantity)
            session.add(new_product)
            await session.commit()
            return SProduct.from_orm(new_product)
    

    async def update_product(id: int, product: SProduct) -> SProduct:
        async with async_session_maker() as session:
            existing_product = await session.get(Product, id)
            if existing_product:
                existing_product.name_product = product.name_product
                existing_product.description = product.description
                existing_product.price = product.price
                existing_product.quantity = product.quantity
                session.add(existing_product)
                await session.commit()
                return SProduct.from_orm(existing_product)
            else:
                raise Exception("Product not found")


    async def delete_product(id: int) -> None:
        async with async_session_maker() as session:
            product = await session.get(Product, id)
            if product:
                await session.delete(product)
                await session.commit()
            else:
                raise Exception("Product not found")

