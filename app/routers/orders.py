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



@router.post('/create')
async def create_order(db: Annotated[AsyncSession, Depends(get_db)], create_order: CreateOrder):
    await db.execute(insert(Orders).values(name=create_order.name,
                                            description=create_order.description,
                                            price=create_order.price,
                                            status=create_order.status,
                                            stock=create_order.stock,
                                            created_at=datetime.now(),
                                            slug=slugify(create_order.name)))
    await db.commit()
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


@router.put('/update_order')
async def update_order():
    pass


@router.delete('/delete_order')
async def delete_order():
    pass