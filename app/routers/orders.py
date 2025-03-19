import configparser
import aio_pika

from datetime import datetime
from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy import insert, select

from sqlalchemy.ext.asyncio import AsyncSession
from app.backend.db_depends import get_db
from app.schemas import CreateOrder
from app.models.orders import Orders


router = APIRouter(prefix='/orders', tags=['order'])

config = configparser.ConfigParser()
config.read_file(open('config.ini'))
RABBITMQ_URL = config.get('rabbitmq', 'RABBITMQ_URL')
QUEUE_NAME = config.get('rabbitmq', 'QUEUE_NAME')


async def send_to_queue(order_id: int):
    connection = await aio_pika.connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=str(order_id).encode()),
            routing_key=QUEUE_NAME,
        )


@router.post("/create_order")
async def create_order(db: Annotated[AsyncSession, Depends(get_db)], create_order: CreateOrder):
    """Метод создания заказа"""
    # Создаем заказ в бд и сразу возвращаем айди заказа для передачи в очередь
    new_order = await db.execute(insert(Orders).values(name=create_order.name,
                                                       description=create_order.description,
                                                       price=create_order.price,
                                                       status="NEW",
                                                       quantity=create_order.quantity,
                                                       created_at=datetime.now()).returning(Orders.id))
    await db.commit()
    # Отправляем сообщение в RabbitMQ
    await send_to_queue(new_order.one()[0])
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }


@router.get('/all_orders')
async def get_all_orders(db: Annotated[AsyncSession, Depends(get_db)]):
    """Метод по получению всех заказов"""
    orders = await db.scalars(select(Orders).where(Orders.is_active == True))
    return orders.all()


@router.get('/order')
async def get_order(db: Annotated[AsyncSession, Depends(get_db)], order_id: int):
    """Метод по получению определенного заказа по его ID"""
    order = await db.scalar(
        select(Orders).where(Orders.id == order_id, Orders.is_active == True))
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Нет заказа с таким ID'
        )
    return order
