from pydantic import PositiveInt
from pydantic.types import NonNegativeInt
from pydantic_settings import BaseSettings as PyBaseSettings


class BaseSettings(PyBaseSettings):
    """Base settings"""
    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
        extra = 'ignore'


class ServerSettings(BaseSettings):
    """Web server settings"""
    server_host: str = '127.0.0.1'
    server_port: PositiveInt = 8015
    debug: bool = 0  # 1 to work with echo


class DatabaseSettings(BaseSettings):
    """Database settings"""
    dialect: str = 'postgresql'
    driver: str = 'psycopg'
    postgres_user: str = ''
    postgres_password: str = ''
    postgres_host: str = ''
    postgres_port: int = 5432
    postgres_db: str = ''

    db_pool_min_size: PositiveInt = 10
    db_pool_max_size: PositiveInt = 10
    statement_cache_size: NonNegativeInt = 0

    @property
    def uri(self) -> str:
        """Database URI"""
        return (
            f'{self.postgres_user}:{self.postgres_password}'
            f'@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}'
        )

    @property
    def dsn(self) -> str:
        """Data Source Name for database connection"""
        return f'{self.dialect}+{self.driver}://{self.uri}'

class CurrencySettings(BaseSettings):
    """Currency settings"""
    api_key: str = ''
    api_url: str = ''


db_settings = DatabaseSettings()
server_settings = ServerSettings()
currency_settings = CurrencySettings()
