import logging

from fastapi import FastAPI
from fastapi_pagination import add_pagination

from app import config
from app.routes import router

LOG = logging.getLogger("carselector")
LOG.setLevel(logging.DEBUG)

def create_app():
    # Create a new FastAPI instance.
    app = FastAPI(
        title = config.PROJECT_NAME, dependencies = [])
    # Create a fast api pagination for this app.
    add_pagination(app)
    # Include the router on our fastapi app.
    app.include_router(router)
    # Return app.
    return app
