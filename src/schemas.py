from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

code_field = Field(..., max_length=5)


class BaseSchema(BaseModel):
    """A base validation schema of the application"""

    class Config:
        from_attributes = True


class CurrencyShortSchema(BaseSchema):
    """Schema for currency update"""
    code: str = code_field
    rate: Decimal = Field(...,  gt=0, max_digits=20, decimal_places=6)


class CurrencySchema(CurrencyShortSchema):
    """Schema for currency list"""
    name: str
    updated_at: datetime


class ConvertSchema(BaseSchema):
    """Schema for currency convert"""
    amount: float
    source: str = code_field
    target: str = code_field


class CurrencyCreateSchema(CurrencyShortSchema):
    """Schema for currency create"""
    name: str
