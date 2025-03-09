import pytest
import pytest_asyncio
import asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.routers.orders import router


@pytest_asyncio.fixture(loop_scope="session")
async def client():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac


@pytest.mark.asyncio(loop_scope="session")
async def test_post_create_order(client):
    response = await client.post("/orders/create_order", json={
        "name": "name",
        "description": "description",
        "price": 100,
        "image_url": "image",
        "quantity": 1,
    })
    print("СЮДААААААААААА", response)
    assert response.status_code == 200
    data = response.json()
    print('otvet', data)
    assert data == {
    'status_code': 201,
    'transaction': 'Successful'
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_orders(client):
    response = await client.get("/orders/all_orders")
    print(response)
    assert response.status_code == 200
    data = response.json()
    print(data)
    # assert len(data) > 1


# Поиск определенного заказа
# @pytest.mark.asyncio(loop_scope="session")
# async def test_get_order(client):
#     order_id = 5
#     response = await client.get(f"/orders/order?order_id={order_id}")
#     assert response.status_code == 200
#     print("Получение заказа", response)
#     # assert response.status_code == 200
#     data = response.json()
#     print(data)



