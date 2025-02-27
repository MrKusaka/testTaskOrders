import aio_pika

from datetime import datetime
from fastapi import APIRouter, Depends, status
from typing import Annotated
from sqlalchemy import insert
from slugify import slugify

from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_db
from app.schemas import CreateOrder
from app.models.orders import Orders


router = APIRouter(prefix='/orders', tags=['order'])

RABBITMQ_URL = "amqp://guest:guest@localhost/"
QUEUE_NAME = "order_queue"


async def send_to_queue(order_id: int):
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=str(order_id).encode()),
            routing_key=QUEUE_NAME,
        )


@router.post("/orders/")
async def create_order(db: Annotated[AsyncSession, Depends(get_db)], create_order: CreateOrder):
    # Создаем заказ в бд и сразу возвращаем айди заказа для передачи в очередь
    new_order = await db.execute(insert(Orders).values(name=create_order.name,
                                                       description=create_order.description,
                                                       price=create_order.price,
                                                       status=create_order.status,
                                                       quantity=create_order.quantity,
                                                       created_at=datetime.now(),
                                                       slug=slugify(create_order.name)).returning(Orders.id))
    await db.commit()

    # Отправляем сообщение в RabbitMQ
    await send_to_queue(new_order.one()[0])

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/all_orders')
async def get_all_orders():
    pass


@router.get('/order')
async def get_order():
    pass

#
#
# @router.put('/update_order')
# async def update_order():
#     pass
#
#
# @router.delete('/delete_order')
# async def delete_order():
#     pass