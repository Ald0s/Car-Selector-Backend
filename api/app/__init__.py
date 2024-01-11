import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from . import config
from .routes import router

LOG = logging.getLogger("carselector")
LOG.setLevel(logging.DEBUG)


def create_app():
    # Create a new FastAPI instance.
    app = FastAPI(
        title = config.PROJECT_NAME, dependencies = [])
    # Configure to allow CORS. This is just an example app so we will have no restrictions.
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"])
    # Create a fast api pagination for this app.
    add_pagination(app)
    # Include the router on our fastapi app.
    app.include_router(router)
    # Return app.
    return app
