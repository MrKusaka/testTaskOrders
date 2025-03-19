import pytest
import pytest_asyncio

from httpx import AsyncClient, ASGITransport

from app.main import app


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
    assert response.status_code == 200
    data = response.json()
    assert data == {
        'status_code': 201,
        'transaction': 'Successful'
    }


@pytest.mark.asyncio(loop_scope="session")
async def test_get_all_orders(client):
    response = await client.get("/orders/all_orders")
    assert response.status_code == 200


@pytest.mark.asyncio(loop_scope="session")
async def test_get_order(client):
    response = await client.get("/orders/order?order_id=2")
    assert response.status_code == 200
    assert response.json() == {
        'name': 'кубик рубэк',
        'quantity': 1,
        'price': 500,
        'status': 'PROCESSED',
        'description': 'топовый',
        'id': 2,
        'created_at': '2025-02-16T15:52:50.906679',
        'is_active': True
    }

    response2 = await client.get("/orders/order?order_id=999")
    assert response2.status_code == 404
    assert response2.json() == {'detail': 'Нет заказа с таким ID'}
