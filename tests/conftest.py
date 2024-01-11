import pytest

from typing import Dict, Generator, Tuple

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app import create_app, dependencies, vehicles
from app.models import SessionLocal, init_database


@pytest.fixture(scope = "function")
def sesh() -> Generator[Session, None, None]:
    # Create a new database session.
    sesh = SessionLocal()
    # Initialise database on the session.
    init_database(sesh)
    # Yield for tests.
    yield sesh


@pytest.fixture(scope = "function")
def test_app(sesh: Session) -> FastAPI:
    # Create a new app.
    new_app = create_app()

    # Define an override for getting the current database session, which should replace the get_session dependency defined in app dependencies.
    def override_get_session() -> Generator[Session, None, None]:
        # We will override the get_session generator with this function to ensure we always return that session.
        yield sesh

    # Set the override on new app.
    new_app.dependency_overrides[dependencies.get_session] = override_get_session

    # Use vehicles module to import data.
    vehicles.load_vehicles_from_file(sesh, "vehicles.json")

    # Flush.
    sesh.flush()

    # Yield the new app.
    yield new_app


@pytest.fixture(scope = "function")
def client(test_app: FastAPI) -> Generator[TestClient, None, None]:
    # Create a new test client with the function-scoped test application.
    with TestClient(test_app) as c:
        # Yield this client.
        yield c
