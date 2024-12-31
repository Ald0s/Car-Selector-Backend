import asyncio
import typer

from app import create_app, database
from app.data import vehicles
from app.logger import log

application = create_app()
wrapper = typer.Typer()


@wrapper.command()
def main():
    """Main command for CSB management."""
    pass


@wrapper.command()
def init_db():
    """Database initialisation command for CSB - this ensures the schema
    is created and up to date.
    """
    log.info("ensuring CSB database is created...")
    async def _async_init_db():
        async with database.async_engine.begin() as conn:
            await conn.run_sync(database.Model.metadata.create_all)
    # run until complete.
    asyncio.get_event_loop()\
        .run_until_complete(_async_init_db())
    log.info("done :)")


@wrapper.command()
def update_master():
    """Update master data tables."""
    log.debug("now updating vehicle master...")
    async def _async_update_master():
        async with database.async_session() as sesh, sesh.begin():
            # with a new started session, invoke vehicles import.
            await vehicles.import_vehicles_from(sesh)
            # commit session.
            await sesh.commit()
    # run until complete.
    asyncio.get_event_loop()\
        .run_until_complete(_async_update_master())
    log.info("done :)")


if __name__ == "__main__":
    wrapper()