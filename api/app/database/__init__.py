"""Global database functionality defined here."""
from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app import datamodels as data
from app.logger import log

from . import errors, compat
from .session import async_engine, async_session
from .basemodel import Model
from .models import *
from .crud import *
from .schemas import *


async def init_database():
    """Initialise the database."""
    async with async_engine.begin() as conn:
        pass


async def close_database():
    """Properly shut the database connection down."""
    await async_engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, Any]:
    """Generate and yield an async database session, that has begun."""
    async with async_session() as sesh, sesh.begin():
        yield sesh


async def find_vehicle_make(
    sesh: AsyncSession,
    make_id: str
) -> Optional[VehicleMake]:
    """Given a session and a Make's UID, attempt to find and return a vehicle
    make for that UID. If none can be found, None will be returned.
    """
    return await vehicle_makes.get_by_id(sesh, make_id)


def build_make_query():
    """Build a query for a selection of VehicleMake."""
    return (
        select(VehicleMake)
    )


def build_type_query(make_id: str):
    """Build a query for a selection of VehicleTypes."""
    return (
        select(VehicleType)
        .join(
            VehicleModel,
            VehicleModel.type_id == VehicleType.id
        )
        .join(
            VehicleMake,
            VehicleMake.id == VehicleModel.vehicle_make_id
        )
        .where(
            VehicleMake.id == make_id
        )
        .group_by(
            VehicleType.id
        )
    )


def build_model_query(make_id: str, type_id: str):
    """Build a query for a selection of VehicleModels."""
    return (
        select(VehicleModel)
        .where(
            and_(
                VehicleModel.type_id == type_id,
                VehicleModel.vehicle_make_id == make_id
            )
        )
    )


def build_year_model_query(make_id: str, type_id: str, model_id: str):
    """Build a query for a selection of VehicleYearModels."""
    return (
        select(VehicleYearModel)
        .join(
            VehicleModel,
            VehicleModel.id == VehicleYearModel.vehicle_model_id
        )
        .where(
            and_(
                VehicleYearModel.vehicle_make_id == make_id,
                VehicleYearModel.vehicle_model_id == model_id
            )
        )
        .where(
            VehicleModel.type_id == type_id
        )
    )


def build_vehicle_query(
    make_id: str,
    type_id: str,
    model_id: str,
    year: int
):
    """Build a query for a selection of Vehicles."""
    return (
        select(
            Vehicle
        )
        .join(
            VehicleYearModel,
            VehicleYearModel.id == Vehicle.vehicle_year_model_id
        )
        .join(
            VehicleModel,
            VehicleModel.id == VehicleYearModel.vehicle_model_id
        )
        .where(
            and_(
                VehicleModel.vehicle_make_id == make_id,
                and_(
                    VehicleModel.type_id == type_id,
                    VehicleModel.id == model_id
                )
            )
        )
        .where(
            VehicleYearModel.year == year
        )
    )


async def update_vehicles(
    sesh: AsyncSession,
    vehicles: data.Vehicles
) -> bool:
    """Upsert all vehicles in the given container into the database, then
    return a boolean depending on the outcome of that operation.
    """
    # first upsert all types.
    for type in vehicles.types:
        await _upsert_type(sesh, type)
    await sesh.flush()
    # now iterate all makes, upserting each.
    for make in vehicles.makes:
        await _upsert_make(sesh, make)
    return True


async def _upsert_type(sesh: AsyncSession, type: data.VehicleType):
    """Upsert the given type into database. This function will not commit."""
    log.debug("attempting to insert type '%s'" % type.name)
    # load a creation schema for the object.
    vehicle_type_create = VehicleTypeCreate\
        .model_validate(type.model_dump(by_alias = True))
    try:
        # within a nested transaction, we'll attempt to insert the object.
        async with sesh.begin_nested():
            await vehicle_types.create(sesh, vehicle_type_create, 
                commit = False)
    except errors.ObjectAlreadyExistsException as oaee:
        # this object already exists, we will update instead.
        log.debug("type '%s' already exists, updating it instead..." % type.name)
        # load an update for this object.
        vehicle_type_update = VehicleTypeUpdate\
            .model_validate(type.model_dump(by_alias = True))
        await vehicle_types.update(sesh, type.type_id, vehicle_type_update,
            commit = False)
    

async def _upsert_make(sesh: AsyncSession, make: data.VehicleMake):
    log.debug("attempting to insert make '%s'" % make.name)
    # load a creation schema for the object.
    vehicle_make_create = VehicleMakeCreate\
        .model_validate(make.model_dump(by_alias = True))
    try:
        # within a nested transaction, we'll attempt to insert the object.
        async with sesh.begin_nested():
            await vehicle_makes.create(sesh, vehicle_make_create, 
                commit = False)
    except errors.ObjectAlreadyExistsException as oaee:
        # this object already exists, we will update instead.
        vehicle_make_update = VehicleMakeUpdate\
            .model_validate(make.model_dump(by_alias = True))
        # load an update for this object.
        await vehicle_makes.update(sesh, make.id, vehicle_make_update,
            commit = False)
    # commit before next object.
    await sesh.flush()
    # now upsert all models within this make.
    for model in make.models:
        await _upsert_model(sesh, model)


async def _upsert_model(sesh: AsyncSession, model: data.VehicleModel):
    log.debug("attempting to insert model '%s'" % model.name)
    # load a creation schema for the object.
    vehicle_model_create = VehicleModelCreate\
        .model_validate(model.model_dump(by_alias = True))
    try:
        # within a nested transaction, we'll attempt to insert the object.
        async with sesh.begin_nested():
            await vehicle_models.create(sesh, vehicle_model_create, 
                commit = False)
    except errors.ObjectAlreadyExistsException as oaee:
        # this object already exists, we will update instead.
        vehicle_model_update = VehicleModelUpdate\
            .model_validate(model.model_dump(by_alias = True))
        # load an update for this object.
        await vehicle_models.update(sesh, model.id, vehicle_model_update,
            commit = False)
    # commit before next object.
    await sesh.flush()
    # now upsert all year models in this model.
    for year_model in model.year_models:
        await _upsert_year_model(sesh, year_model)


async def _upsert_year_model(sesh: AsyncSession, year_model: data.VehicleYearModel):
    log.debug("attempting to insert year model '%s'" % year_model.id)
    # load a creation schema for the object.
    vehicle_year_model_create = VehicleYearModelCreate\
        .model_validate(year_model.model_dump(by_alias = True))
    try:
        # within a nested transaction, we'll attempt to insert the object.
        async with sesh.begin_nested():
            await vehicle_year_models.create(sesh, vehicle_year_model_create, 
                commit = False)
    except errors.ObjectAlreadyExistsException as oaee:
        # this object already exists, we will update instead.
        vehicle_year_model_update = VehicleYearModelUpdate\
            .model_validate(year_model.model_dump(by_alias = True))
        # load an update for this object.
        await vehicle_year_models.update(sesh, year_model.id, vehicle_year_model_update,
            commit = False)
    # commit before next object.
    await sesh.flush()
    # now upsert all vehicles in this year model.
    for vehicle in year_model.vehicles:
        await _upsert_vehicle(sesh, vehicle)


async def _upsert_vehicle(sesh: AsyncSession, vehicle: data.Vehicle):
    """Abstract between the different kinds of vehicles, and invoke the
    correct upsert logic on that basis.
    """
    log.debug("attempting to insert vehicle '%s'" % str(vehicle))
    if isinstance(vehicle, data.Car):
        await _upsert_car(sesh, vehicle)
    elif isinstance(vehicle, data.Bike):
        await _upsert_bike(sesh, vehicle)
    else:
        raise TypeError("unrecognised vehicle type '%s'" % str(type(vehicle)))
    

async def _upsert_car(sesh: AsyncSession, car: data.Car):
    """Insert the given car into the database according to how cars are
    stored. If the car already exists, update it.
    """
    log.debug("attempting to insert car '%s'" % car.id)
    # load a creation schema for the object.
    vehicle_create = VehicleCreate\
        .model_validate(car.model_dump(by_alias = True))
    try:
        # within a nested transaction, we'll attempt to insert the object.
        async with sesh.begin_nested():
            await vehicles.create(sesh, vehicle_create, 
                commit = False)
    except errors.ObjectAlreadyExistsException as oaee:
        # this object already exists, we will update instead.
        vehicle_update = VehicleUpdate\
            .model_validate(car.model_dump(by_alias = True))
        # load an update for this object.
        await vehicles.update(sesh, car.id, vehicle_update,
            commit = False)


async def _upsert_bike(sesh: AsyncSession, bike: data.Bike):
    """Bikes are not at all supported by this project. So don't even try.
    or do, idc kys
    """
    raise NotImplementedError