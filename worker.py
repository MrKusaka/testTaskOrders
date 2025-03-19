import asyncio
import configparser

from aio_pika import connect, IncomingMessage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import update
from app.models.orders import Orders


config = configparser.ConfigParser()
config.read_file(open('config.ini'))
RABBITMQ_URL = config.get('rabbitmq', 'RABBITMQ_URL')
QUEUE_NAME = config.get('rabbitmq', 'QUEUE_NAME')


engine = create_async_engine(config.get('postgres', 'db'), echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Функция для обновления статуса заказа
async def update_order_status(order_id: int, new_status: str):
    async with async_session_maker() as session:
        async with session.begin():
            stmt = update(Orders).where(Orders.id == order_id).values(status=new_status)
            await session.execute(stmt)


# Обработчик сообщений
async def process_message(message: IncomingMessage):
    async with message.process():
        print(f"Заказ №{message.body.decode()} поступил на обработку")
        # Имитация обработки заказа, приостанавливаем на n секунд
        await asyncio.sleep(20) # 20 секунд
        order_id = int(message.body.decode())

        # Обновление статуса заказа в базе данных
        await update_order_status(order_id, "PROCESSED")
        async with async_session_maker() as session:
            async with session.begin():
                order_name = await session.get(Orders, order_id)
        print(f"Статус заказа №{order_id} {order_name.name} обновлен на PROCESSED")


# Воркер для подписки на очередь
async def worker():
    connection = await connect(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        print(f"Подписка на очередь {QUEUE_NAME}...")
        await queue.consume(process_message)

        # Бесконечный цикл для поддержания воркера
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(worker())
