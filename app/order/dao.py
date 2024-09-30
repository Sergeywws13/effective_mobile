from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from app.database import async_session_maker
from app.order.models import Order, OrderItem
from app.order.schemas import SOrder, SOrderItem, SOrderCreate, SOrderItemCreate
from app.product.models import Product

class OrderDAO:
    model = Order


    @staticmethod
    async def create_order(order: SOrderCreate) -> SOrder:
        async with async_session_maker() as session:
            new_order = Order(date_create=order.date_create, status=order.status)
            session.add(new_order)
            await session.flush()

            for item in order.items:
                product = await session.get(Product, item.product_id)
                if product is None:
                    raise ValueError(f"Product with id {item.product_id} not found")
                if product.quantity < item.quantity:
                    raise ValueError(f"Not enough quantity for product {item.product_id}. Available: {product.quantity}, Requested: {item.quantity}")
                
                new_order_item = OrderItem(order_id=new_order.id, product_id=item.product_id, quantity=item.quantity)
                session.add(new_order_item)
                
                product.quantity -= item.quantity

            await session.commit()
            await session.refresh(new_order)
            return SOrder.from_orm(new_order)


    @staticmethod
    async def get_order(order_id: int) -> dict:
        async with async_session_maker() as session:
            query = (
                select(Order)
                .options(joinedload(Order.items))
                .filter(Order.id == order_id)
            )
            result = await session.execute(query)
            order = result.unique().scalar_one_or_none()
            if order is None:
                raise ValueError(f"Order with id {order_id} not found")
            return {
                "id": order.id,
                "date_create": order.date_create,
                "status": order.status,
                "items": [
                    {
                        "id": item.id,
                        "order_id": item.order_id,
                        "product_id": item.product_id,
                        "quantity": item.quantity
                    } for item in order.items
                ]
            }


    @staticmethod
    async def update_order_status(order_id: int, new_status: str) -> SOrder:
        async with async_session_maker() as session:
            order = await session.get(Order, order_id)
            if order is None:
                raise ValueError(f"Order with id {order_id} not found")
            
            if new_status not in [Order.IN_PROCESS, Order.SENT, Order.DELIVERED]:
                raise ValueError("Invalid order status")
            
            order.status = new_status
            session.add(order)
            await session.commit()
            await session.refresh(order)


            items = await session.execute(select(OrderItem).where(OrderItem.order_id == order_id))
            order.items = items.scalars().all()
            return SOrder.from_orm(order)


    @staticmethod
    async def get_all_orders() -> list[dict]:
        async with async_session_maker() as session:
            query = select(Order).options(joinedload(Order.items))
            result = await session.execute(query)
            orders = result.unique().scalars().all()
            return [
                {
                    "id": order.id,
                    "date_create": order.date_create,
                    "status": order.status,
                    "items": [
                        {
                            "id": item.id,
                            "order_id": item.order_id,
                            "product_id": item.product_id,
                            "quantity": item.quantity
                        } for item in order.items
                    ]
                } for order in orders
            ]
