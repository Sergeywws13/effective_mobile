import pytest
from app.order.dao import OrderDAO
from app.order.schemas import SOrderCreate

@pytest.fixture
async def order_dao():
    return OrderDAO()


@pytest.mark.asyncio
async def test_create_order(order_dao):
    order = SOrderCreate(date_create="2022-01-01", status="в процессе", items=[{"product_id": 4, "quantity": 2}])
    result = await order_dao.create_order(order)
    assert result.id is not None
    assert result.date_create == "2022-01-01"
    assert result.status == "в процессе"
    assert len(result.items) == 1
    assert result.items[0].product_id == 4
    assert result.items[0].quantity == 2


@pytest.mark.asyncio
async def test_get_order(order_dao):
    order = SOrderCreate(date_create="2022-01-01", status="отправлен", items=[{"product_id": 3, "quantity": 2}])
    result = await order_dao.create_order(order)
    order_id = result.id
    result = await order_dao.get_order(order_id)
    assert result.id == order_id
    assert result.date_create == "2022-01-01"
    assert result.status == "отправлен"
    assert len(result.items) == 1
    assert result.items[0].product_id == 3
    assert result.items[0].quantity == 2


@pytest.mark.asyncio
async def test_update_order_status(order_dao):
    order = SOrderCreate(date_create="2022-01-01", status="доставлен", items=[{"product_id": 4, "quantity": 2}])
    result = await order_dao.create_order(order)
    order_id = result.id
    new_status = "in_progress"
    result = await order_dao.update_order_status(order_id, new_status)
    assert result.id == order_id
    assert result.date_create == "2022-01-01"
    assert result.status == new_status
    assert len(result.items) == 1
    assert result.items[0].product_id == 4
    assert result.items[0].quantity == 2