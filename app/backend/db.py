from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

import configparser


config = configparser.ConfigParser()
config.read_file(open('config.ini'))

engine = create_async_engine(config.get('postgres', 'db'), echo=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class Base(DeclarativeBase):
    pass