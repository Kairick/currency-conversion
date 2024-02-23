from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine,
)

from settings import db_settings, server_settings


async def get_local_session():
    async with async_session() as session:
        return session


def _get_engine(dsn, debug: bool = False):
    """Retrieve database engine"""

    return create_async_engine(
        dsn,
        echo=debug,
        pool_pre_ping=True,
        poolclass=NullPool,
        connect_args={'prepare_threshold': 0},
    )


def _get_async_session(dsn, debug: bool = False):
    """Retrieves db session object"""
    engine = _get_engine(dsn, debug)
    return async_sessionmaker(
        bind=engine, class_=AsyncSession,
        autocommit=False, autoflush=False, expire_on_commit=False
    )


def get_db_session_dependence(dsn, debug: bool = False):
    """Func which for using on Depends()"""
    _async_session = _get_async_session(dsn, debug)

    async def get_db_session() -> AsyncSession:
        """
        Create new db session and guarantees that it will be closed.
        """
        async with _async_session() as db:
            yield db

    return get_db_session


get_async_session = get_db_session_dependence(
    db_settings.dsn, server_settings.debug)
async_session = _get_async_session(db_settings.dsn, server_settings.debug)
