from decimal import Decimal

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from external_service import CurrencyClient
from repository import CurrencyRepository
from schemas import ConvertSchema


class CurrencyService:
    def __init__(self, db: AsyncSession = Depends(get_async_session)):
        self.external_client = CurrencyClient()
        self.repo = CurrencyRepository(db)

    async def get_currency_list(self):
        """Get all currencies"""
        result = await self.repo.get_all()
        if not result:
            currencies = await self.external_client.init_currencies()
            result = await self.repo.insert_many(currencies)

        return result

    async def update_currency(self):
        """Update all currencies"""
        data = await self.external_client.get_currencies()
        await self.repo.update_all(data)

    async def convert_currency(self, data: ConvertSchema):
        """Convert currency from source to target"""
        if data.source == data.target:
            return data.amount
        source = await self.repo.get_by_code(data.source)
        target = await self.repo.get_by_code(data.target)
        if not source or not target:
            HTTPException(
                status_code=400,
                detail='Invalid source or target currency code.'
            )
        result = Decimal(data.amount) * target.rate / source.rate
        return result
