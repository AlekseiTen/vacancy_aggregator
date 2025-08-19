import asyncio

from sqlalchemy import Integer, Column, Text, String, Boolean, DateTime, func
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class HH(Base):
    __tablename__ = 'hh'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    employer = Column(Text)
    url = Column(String(2048))
    is_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class SJ(Base):
    __tablename__ = 'superjob'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    employer = Column(Text)
    url = Column(String(2048))
    is_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class MTS(Base):
    __tablename__ = 'mts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    profession = Column(Text)
    url = Column(String(2048))
    is_sent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class TelegramUser(Base):
    __tablename__ = 'telegram_users'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True, index=True, nullable=False)
    user_name = Column(String)


DATABASE_URL = "postgresql+asyncpg://postgres:Thuglife7!@localhost/vacancy_aggregator"

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Асинхронная функция для создания таблиц
async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Запускаем создание таблиц
if __name__ == "__main__":
    asyncio.run(init_models())
