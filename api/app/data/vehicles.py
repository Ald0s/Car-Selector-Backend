"""Business layer logic for reading & parsing Vehicle information,
then facilitating its upsertion into database.
"""
import os
import pathlib
import aiofiles

from typing import Optional, Union

from sqlalchemy.ext.asyncio import AsyncSession

from app import config, database, datamodels as data
from app.logger import log


async def import_vehicles_from(
    sesh: AsyncSession,
    input_: Optional[Union[str, pathlib.Path]] = None
) -> bool:
    """Given an input; either a path or a string that is a path, read the
    vehicle master data indicated and insert/upsert it all into the database,
    inserting and updating where relevant.

    This function will return a boolean indicating success.
    """
    vehicles: data.Vehicles = await read_vehicles_from(input_)
    return await database.update_vehicles(sesh, vehicles)


async def read_vehicles_from(
    input_: Optional[Union[str, pathlib.Path]] = None
) -> data.Vehicles:
    """Given an input; either a path or a string that is a path, read and
    return that as a vehicles container. If input is none, the best source
    file is determined based on current environment.
    """
    if input_ is None:
        # no input explicitly given, try to use current master directory, then
        # the vehicles.json filename.
        input_: str = os.path.join(
            config.MASTER_DIRECTORY,
            "vehicles.json"
        )
        log.warning("no vehicles data input given, trying to find one "\
                    "located at %s..." % (input_))
    # build a path from this, ensure its a file.
    path = pathlib.Path(input_)
    if not path.is_file():
        raise Exception("failed to import cars from '%s', that is not a file."
                        % input_)
    # now parse contents as a vehicles container.
    async with aiofiles.open(path, mode = "r") as r:
        contents: str = await r.read()
        return data.Vehicles\
            .model_validate_json(contents)