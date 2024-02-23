from unittest.mock import patch

import pytest
from httpx import AsyncClient

from application import app


def fake_init() -> list:
    return [
        {
            'name': 'Dollar',
            'code': 'USD',
            'rate': 1.0,
        },
        {
            'name': 'Euro',
            'code': 'EUR',
            'rate': 1.2,
        },
        {
            'name': 'Pound',
            'code': "GBP",
            'rate': 1.4,
        }
    ]


def fake_currency() -> list:
    return [
        {
            'code': 'USD',
            'rate': 1.0,
        },
        {
            'code': 'EUR',
            'rate': 1.0234,
        },
        {
            'code': "GBP",
            'rate': 1.5,
        }
    ]


@pytest.mark.asyncio
@patch('external_service.CurrencyClient.init_currencies')
async def test_init_and_get_currencies(monkey_patch):
    """Test init and get currencies, when database is empty"""
    monkey_patch.return_value = fake_init()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/api/currency/currency_list')

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.headers['content-type'] == 'application/json'
    assert response.json()[0]['code'] == 'EUR'
    assert response.json()[1]['code'] == 'GBP'
    assert response.json()[2]['code'] == 'USD'


@pytest.mark.asyncio
async def test_get_currencies(currencies):
    """Test get currencies"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/api/currency/currency_list')

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.headers['content-type'] == 'application/json'
    assert response.json()[0]['code'] == 'EUR'
    assert response.json()[1]['code'] == 'GBP'
    assert response.json()[2]['code'] == 'USD'


@pytest.mark.asyncio
@patch('external_service.CurrencyClient.get_currencies')
async def test_update_currencies(monkey_patch, currencies):
    """Test update currencies"""
    currency_1, currency_2, currency_3 = currencies
    monkey_patch.return_value = fake_currency()

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.patch('/api/currency/update_currency')

    assert response.status_code == 200
    assert response.json()['message'] == 'Currencies updated'

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/api/currency/currency_list')

    assert response.json()[0]['updated_at'] != currency_1.updated_at.strftime(
        '%Y-%m-%dT%H:%M:%S.%f')
    assert response.json()[0]['rate'] == f'{fake_currency()[1]["rate"]:0.6f}'
    assert response.json()[1]['updated_at'] != currency_2.updated_at.strftime(
        '%Y-%m-%dT%H:%M:%S.%f')
    assert response.json()[1]['rate'] == f'{fake_currency()[2]["rate"]:0.6f}'
    assert response.json()[2]['updated_at'] != currency_3.updated_at.strftime(
        '%Y-%m-%dT%H:%M:%S.%f')
    assert response.json()[2]['rate'] == f'{fake_currency()[0]["rate"]:0.6f}'


@pytest.mark.asyncio
async def test_convert_currency(currencies):
    """Test convert currency"""
    currency_1, currency_2, currency_3 = currencies

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/api/currency/convert_currency', params={
            'source': 'USD',
            'target': 'EUR',
            'amount': 10
        })

    assert response.status_code == 200
    assert response.json() == float(10 * currency_1.rate / currency_3.rate)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/api/currency/convert_currency', params={
            'source': 'USD',
            'target': 'USD',
            'amount': 10
        })

    assert response.json() == 10.0


@pytest.mark.asyncio
async def test_convert_with_incorrect_currency(currencies):
    """Test convert currency with incorrect currency"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get('/api/currency/convert_currency', params={
            'source': 'GEL',
            'target': 'EUR',
            'amount': 10
        })

    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Invalid source or target currency code.'
    }
