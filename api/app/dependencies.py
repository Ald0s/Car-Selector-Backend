"""Define various dependencies for use across the application."""
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session


# Define a dependency that will inject a started database session.
Sesh = Annotated[AsyncSession, Depends(get_session)]