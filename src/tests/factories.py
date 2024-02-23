from factory import Factory, Faker
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from models import Currency

uri = 'postgresql+psycopg://test:password@localhost:54433/test_db'
engine = create_async_engine(uri)
Session = async_sessionmaker(bind=engine)


class CurrencyFactory(Factory):
    """Currency factory for asynchronous testing"""
    name = Faker('text', max_nb_chars=30)
    code = Faker('text', max_nb_chars=5, text_type='upper')
    rate = Faker('pydecimal', left_digits=4, right_digits=2, min_value=0)

    class Meta:
        model = Currency

    @classmethod
    async def _create(cls, model_class, *args, **kwargs):
        """Override the _create method to work with an asynchronous session."""
        obj = model_class(*args, **kwargs)
        async with Session() as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
            return obj
