from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, registry

mapper_registry = registry()
Base = mapper_registry.generate_base()


class Currency(Base):
    """Model for currency"""
    __tablename__ = 'currency'

    id: Mapped[int] = mapped_column(
        nullable=False, unique=True,
        primary_key=True, autoincrement=True, comment='ID'
    )
    name: Mapped[str] = mapped_column(
        nullable=True, comment='Currency name'
    )
    rate: Mapped[Decimal] = mapped_column(
        Numeric(20, 6),
        nullable=False, comment='Currency rate to USD', default=1)
    code: Mapped[str] = mapped_column(
        String(5), nullable=False, unique=True,
        index=True, comment='Currency code',
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow,
        comment='Last update date'
    )

    def __str__(self):
        return f'{self.name} {self.code}'

