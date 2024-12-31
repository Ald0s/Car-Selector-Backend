from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    """Base for all models to extend - this will register all models
    we define further.
    """