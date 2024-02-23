from typing import Annotated

from fastapi import APIRouter, Depends

from schemas import ConvertSchema, CurrencySchema
from service import CurrencyService

currency_api = APIRouter()


@currency_api.get('/currency_list', response_model=list[CurrencySchema])
async def get_currency_list(service: Annotated[CurrencyService, Depends()]):
    """Returns a list of currencies and date of last update

    All currencies are returned with their rates
    depending on the base currency (USD).
    """
    return await service.get_currency_list()


@currency_api.patch('/update_currency')
async def update_currency_list(service: Annotated[CurrencyService, Depends()]):
    """Returns updated list of currencies and date of last update"""
    await service.update_currency()
    return {'message': 'Currencies updated'}


@currency_api.get('/convert_currency')
async def convert_currency(
    service: Annotated[CurrencyService, Depends()],
    data: Annotated[ConvertSchema, Depends()]
) -> float:
    """Converts currency from source to target"""
    return await service.convert_currency(data)