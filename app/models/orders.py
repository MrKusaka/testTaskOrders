from app.backend.db import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    slug = Column(String, unique=True, index=True)
    quantity = Column(Integer)
    description = Column(String)
    price = Column(Integer)
    created_at = Column(DateTime)
    status = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    # добавить прайс

from sqlalchemy.schema import CreateTable
print(CreateTable(Orders.__table__))
