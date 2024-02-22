from datetime import datetime

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert

from models import Currency


class CurrencyRepository:
    """Class for vendors repository"""
    table = Currency

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def get_all(self):
        """Get all currencies"""
        query = select(self.table).order_by(self.table.code)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def insert_many(self, data):
        """Insert many currencies"""
        query = insert(self.table).values(data).returning(self.table)
        result = await self.db.execute(query)
        await self.db.commit()
        return result.scalars().all()

    async def update_all(self, data):
        """Update all currencies"""
        # codes = [currency['code'] for currency in data]
        # rates = [currency['rate'] for currency in data]
        # query = update(
        #     self.table
        # ).where(self.table.code.in_(codes)).values(rate=rates)
        query = pg_insert(self.table).values(data)
        on_conflict_update = query.on_conflict_do_update(
            index_elements=['code'],
            set_={
                'rate': query.excluded.rate,
                'updated_at': datetime.utcnow()
            }
        )
        await self.db.execute(on_conflict_update)
        await self.db.commit()

    async def get_by_code(self, code: str):
        """Get currency by code"""
        query = select(self.table).where(self.table.code == code)
        result = await self.db.execute(query)
        return result.scalars().first()
