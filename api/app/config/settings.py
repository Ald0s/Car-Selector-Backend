import os

from sqlalchemy.pool import StaticPool


class BaseConfig():
    """TODO: convert to use BaseSettings."""
    TESTING: bool = False
    DEBUG: bool = False

    SQLALCHEMY_SESSION_OPTS = {}
    SQLALCHEMY_ENGINE_OPTS = {}
    SQLALCHEMY_CONNECT_ARGS = {}
    SQLALCHEMY_POOLCLASS = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    PROJECT_NAME: str = "Car-Selector-Backend"

    MAX_CONTENT_LENGTH: int = 16 * 1024 * 1024 # 16 MB
    STREAM_CHUNK_SZ: int = 10 * 1024 * 1024 # 10 MB

    IMPORT_PATH: str = "import"

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_CONNECT_ARGS = {
        "check_same_thread": False}
    SQLALCHEMY_POOLCLASS = StaticPool

    def __init__(self):
        make_dir(self.IMPORT_PATH)


class TestConfig(BaseConfig):
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False

    TESTING = True
    DEBUG = True

    # The default number per page in pagination.
    DEFAULT_NUM_PER_PAGE = 10
    # The maximum allowed number per page in pagination.
    MAX_NUM_PER_PAGE = 10


class DevelopmentConfig(BaseConfig):
    FLASK_ENV = "development"
    FLASK_DEBUG = True
    DEBUG = True

    # The default number per page in pagination.
    DEFAULT_NUM_PER_PAGE = 25
    # The maximum allowed number per page in pagination.
    MAX_NUM_PER_PAGE = 25


class ProductionConfig(BaseConfig):
    FLASK_ENV = "production"

    # The default number per page in pagination.
    DEFAULT_NUM_PER_PAGE = 25
    # The maximum allowed number per page in pagination.
    MAX_NUM_PER_PAGE = 25


def make_dir(path):
    try:
        os.makedirs(os.path.join(os.getcwd(), path))
    except OSError as o:
        pass