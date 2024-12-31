import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from . import config, database
from .logger import log
from .routes import api_router


def create_app():
    log.debug("creating a new fastapi app instance in environment %s"
              % (config.APP_ENV))
    # create a new FastAPI instance.
    app = FastAPI(
        title = config.PROJECT_NAME, dependencies = [])
    # configure to allow CORS. This is just an example app so we will
    # have no restrictions.
    app.add_middleware(
        CORSMiddleware,
        allow_origins = ["*"],
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"])
    # register events on the application.
    _register_events(app)
    # create a fast api pagination for this app.
    add_pagination(app)
    # include the API router on our fastapi app.
    #app.include_router(router)
    app.include_router(api_router)
    # return app.
    return app


def _register_events(app: FastAPI):
    """Register key events to the application instance."""
    @app.on_event("startup")
    async def on_startup():
        """Whenever the application starts up, we'll ensure the database has
        been created, and we'll also update the vehicle master.
        """
        log.debug("application starting up, ensuring database is created...")
        await database.init_database()
        log.debug("app startup completed :)")

    @app.on_event("shutdown")
    async def on_shutdown():
        """On shutdown, ensure we close the database properly."""
        log.debug("application shutting down...")
        await database.close_database()
