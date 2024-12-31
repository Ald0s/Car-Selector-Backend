import os

from sqlalchemy.pool import StaticPool


class BaseConfig:
    DEBUG = False
    TESTING = False
    
    SQLALCHEMY_POOLCLASS = None
    
    # Set to any value to serve media through nginx.
    USING_NGINX = None

    # Set either the following URI or...
    SQLALCHEMY_DATABASE_URI = None

    # You may also set each of these.
    DB_HOST = None
    DB_USER = None
    DB_PASSWORD = None
    DB_DATABASE = None
    DB_ADAPTER = "mysql+aiomysql"

    # The project's name.
    PROJECT_NAME: str = "Car Selector"
    # Current version.
    VERSION: str = "0.0.1"

    # Directory to where we'll store content that can be requested.
    CONTENT_DIRECTORY = None
    # Directory to where we store master data.
    MASTER_DIRECTORY = None


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"

    # The default number per page in pagination.
    DEFAULT_NUM_PER_PAGE = 10
    # The maximum allowed number per page in pagination.
    MAX_NUM_PER_PAGE = 10


class DevelopmentConfig(BaseConfig):
    TESTING = False
    DEBUG = True

    # The default number per page in pagination.
    DEFAULT_NUM_PER_PAGE = 25
    # The maximum allowed number per page in pagination.
    MAX_NUM_PER_PAGE = 25


class ProductionConfig(BaseConfig):
    # The default number per page in pagination.
    DEFAULT_NUM_PER_PAGE = 25
    # The maximum allowed number per page in pagination.
    MAX_NUM_PER_PAGE = 25