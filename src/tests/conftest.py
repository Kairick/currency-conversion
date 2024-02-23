import os

import pytest_asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine,
)

from models import Base
from tests.factories import CurrencyFactory

URI = 'postgresql+psycopg://test:password@localhost:54433/test_db'


@pytest_asyncio.fixture(autouse=True)
async def session() -> AsyncSession:
    os.environ['POSTGRES_USER'] = 'test'
    os.environ['POSTGRES_PASSWORD'] = 'password'
    os.environ['POSTGRES_HOST'] = 'localhost'
    os.environ['POSTGRES_PORT'] = '54433'
    os.environ['POSTGRES_DB'] = 'test_db'
    engine = create_async_engine(URI)
    async_session_factory = async_sessionmaker(
        engine, expire_on_commit=False, autoflush=False
    )
    async with async_session_factory() as session:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield session

        async with engine.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.drop_all)
            except Exception as e:
                print(f"Error dropping tables: {e}")

    await engine.dispose()


@pytest_asyncio.fixture
async def currencies():
    """Create currencies for testing"""
    currency_1 = await CurrencyFactory(name='Euro', code='EUR', rate=1.2)
    currency_2 = await CurrencyFactory(name='Pound', code='GBP', rate=1.4)
    currency_3 = await CurrencyFactory(name='Dollar', code='USD', rate=1.0)
    return currency_1, currency_2, currency_3
