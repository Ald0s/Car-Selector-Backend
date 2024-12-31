"""Vehicle specific API endpoints."""
from fastapi import APIRouter

from fastapi_pagination.ext.sqlalchemy import paginate

from app import config, database, utility as util
from app.dependencies import Sesh
from app.logger import log

from . import schemas

router = APIRouter(
    prefix = "/vehicles",
    tags = ["vehicles"]
)

# Make a new page response type configured with the desired page sizes.
PageResponse = util.make_page_response()


@router.get("/makes", response_model = PageResponse[schemas.VehicleMakeResponse])
async def search_vehicle_makes(sesh: Sesh):
    """Search for Vehicle makes. This is a pagination route, so you may
    also provide the following arguments:

    :page: The requested page.
    :limit: The number per page."""
    log.debug(f"attempting to locate vehicle makes")
    makes_q = database.build_make_query()
    return await paginate(sesh, makes_q)
    

@router.get("/types", response_model = PageResponse[schemas.VehicleTypeResponse])
async def search_vehicle_types(mk: str, sesh: Sesh):
    """Search for vehicle types for the given make UID.
    :mk: The make UID.
    
    This is a pagination route, so you may also provide the following arguments:
    :page: The requested page.
    :limit: The number per page."""
    log.debug("attempting to locate vehicle types with make '%s'" % mk)
    types_q = database.build_type_query(mk)
    return await paginate(sesh, types_q)
    

@router.get("/models", response_model = PageResponse[schemas.VehicleModelResponse])
async def search_vehicle_models(mk: str, t: str, sesh: Sesh):
    """Search for vehicle models for the given make UID and type ID.
    :mk: The make UID.
    :t: the Type ID.

    This is a pagination route, so you may also provide the following arguments:
    :page: The requested page.
    :limit: The number per page."""
    log.debug("attempting to locate vehicle models with make '%s' and type '%s'"
              % (mk, t,))
    models_q = database.build_model_query(mk, t)
    return await paginate(sesh, models_q)
    

@router.get("/years", response_model = PageResponse[schemas.VehicleYearModelResponse])
async def search_vehicle_years(
    mk: str,
    t: str,
    mdl: str,
    sesh: Sesh
):
    """Search for vehicle years given make UID, type ID and model UID:
    :mk: The make UID.
    :t: The type ID.
    :mdl: The model's UID.
    
    This is a pagination route, so you may also provide the following arguments:
    :page: The requested page.
    :limit: The number per page."""
    log.debug("Attempting to locate vehicle years with make '%s', type '%s' and model '%s'"\
              % (mk, t, mdl,))
    year_models_q = database.build_year_model_query(mk, t, mdl)
    return await paginate(sesh, year_models_q)


@router.get("/stock", response_model = PageResponse[schemas.VehicleResponse])
async def search_vehicles_stock(
    mk: str,
    t: str,
    mdl: str,
    y: int,
    sesh: Sesh
):
    """Search for vehicles given a set of cascading criteria. Accepted parameters (also in this order):
    :mk: The make UID.
    :t: The type ID.
    :mdl: The model's UID.
    :y: The target year.
    
    This is a pagination route, so you may also provide the following arguments:
    :page: The requested page.
    :limit: The number per page."""
    log.debug("attempting to locate vehicle stocks with make '%s', type '%s'"\
              ", model '%s' and year '%d'" % (mk, t, mdl, y,))
    vehicles_q = database.build_vehicle_query(mk, t, mdl, y)
    results = await sesh.execute(vehicles_q)
    print(results.all())
    return await paginate(sesh, vehicles_q)