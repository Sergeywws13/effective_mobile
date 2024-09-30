from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    date_create = Column(Date, nullable=False)
    status = Column(String, nullable=False)

    items = relationship("OrderItem", back_populates="order")

    IN_PROCESS = "в процессе"
    SENT = "отправлен"
    DELIVERED = "доставлен"   


class OrderItem(Base):
    __tablename__ = "orderitems"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")


    
