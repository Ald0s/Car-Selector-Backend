"""Creating connections & session management for the app."""
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)

from app import config


if config.SQLALCHEMY_DATABASE_URI is None:
    # if sqlalchemy database uri is not set, create a URL from
    # the db_ components.
    connection_url = URL.create(
        config.DB_ADAPTER,
        username = config.DB_USER,
        password = config.DB_PASSWORD,
        host = config.DB_HOST,
        database = config.DB_DATABASE
    )
else:
    # otherwise just use configured value.
    connection_url = config.SQLALCHEMY_DATABASE_URI

# create a new async engine with that URL.
async_engine = create_async_engine(connection_url, echo = False)

# create an async session maker bound to that engine.
async_session = async_sessionmaker(
    async_engine,
    class_ = AsyncSession,
    expire_on_commit = False
)