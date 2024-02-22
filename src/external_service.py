import aiohttp
from fastapi import HTTPException

from schemas import CurrencyCreateSchema, CurrencyShortSchema
from settings import currency_settings


class CurrencyClient:
    """Class for getting data from https://currencyapi.com/docs/latest"""
    api_key = currency_settings.api_key
    api_url = currency_settings.api_url

    async def get_currencies(self):
        """Get currency list with actual rates"""
        result = []
        rates = await self._get_data('latest')
        for currency in rates['data'].values():
            result.append(
                CurrencyShortSchema(
                    code=currency['code'],
                    rate=f'{currency["value"]:0.6f}'
                ).dict()
            )
        return result

    async def init_currencies(self) -> list[dict]:
        """Get all currencies' names and rates"""
        result = []
        currencies = await self._get_data('currencies')
        rates = await self._get_data('latest')
        for currency in currencies['data'].values():
            result.append(
                CurrencyCreateSchema(
                    code=currency['code'],
                    name=currency['name'],
                    rate=f'{rates["data"][currency["code"]]["value"]:0.6f}'
                ).dict()
            )
        return result

    async def _get_data(self, suffix: str) -> dict:
        """Get data from external service"""
        headers = {'apikey': self.api_key}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(f'{self.api_url}/{suffix}') as response:
                result = await response.json()
                if response.status == 429:
                    raise HTTPException(
                        status_code=400,
                        detail='Your limit is exceeded. Try again later.'
                    )
                if response.status != 200:
                    raise HTTPException(
                        status_code=400,
                        detail='Invalid request. Check api documentation.'
                    )
                return result
