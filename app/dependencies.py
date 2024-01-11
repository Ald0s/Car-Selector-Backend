from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app import config, models


def get_session() -> Session:
    """A generator that will yield database sessions."""
    # Create a new session.
    sesh = models.SessionLocal()
    try:
        # Yield the session.
        yield sesh
    finally:
        # Always close the session after use.
        sesh.close()
# Define a shared dependency here so we can just use this everywhere.
DatabaseSessionDep = Annotated[Session, Depends(get_session)]