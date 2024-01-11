import logging

from fastapi import APIRouter, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from . import config, vehicles, schemas
from .dependencies import (
    DatabaseSessionDep
)

LOG = logging.getLogger("carselector.routes")
LOG.setLevel(logging.DEBUG)

router = APIRouter()

# Adjust page size.
Page = Page.with_custom_options(
    size = Query(config.DEFAULT_NUM_PER_PAGE,
        ge = 1,
        le = config.MAX_NUM_PER_PAGE))


@router.get("/api/vehicles/makes", response_model = Page[schemas.Make])
def search_vehicle_makes(
    sesh: DatabaseSessionDep
):
    """Search for Vehicle makes.

    This is a pagination route, so you may also provide the following arguments:
    :page: The requested page.
    :limit: The number per page."""
    try:
        LOG.debug(f"Attempting to locate vehicle makes")
        # Assemble a query for the target entity given our input.
        search_vehicles_q, _ = vehicles.make_search_vehicles_query()

        # Now, return a call to paginate for this query.
        return paginate(sesh, search_vehicles_q)
    except Exception as e:
        raise e
    

@router.get("/api/vehicles/types", response_model = Page[schemas.Type])
def search_vehicle_types(
    mk: str,
    sesh: DatabaseSessionDep
):
    """Search for vehicle types for the given make UID.
    :mk: The make UID.
    
    This is a pagination route, so you may also provide the following arguments:
    :page: The requested page.
    :limit: The number per page."""
    try:
        LOG.debug(f"Attempting to locate vehicle types with make {mk}")
        # Assemble a query for the target entity given our input.
        search_vehicles_q, _ = vehicles.make_search_vehicles_query(dict(
            make_uid = mk))
  
        # Now, return a call to paginate for this query.
        return paginate(sesh, search_vehicles_q)
    except Exception as e:
        raise e
    

@router.get("/api/vehicles/models", response_model = Page[schemas.Model])
def search_vehicle_models(
    mk: str,
    t: str,
    sesh: DatabaseSessionDep
):
    """Search for vehicle models for the given make UID and type ID.
    :mk: The make UID.
    :t: the Type ID.

    This is a pagination route, so you may also provide the following arguments:
    :page: The requested page.
    :limit: The number per page."""
    try:
        LOG.debug(f"Attempting to locate vehicle models with make {mk} and type {t}")
        # Assemble a query for the target entity given our input.
        search_vehicles_q, _ = vehicles.make_search_vehicles_query(dict(
            make_uid = mk, type_id = t))
  
        # Now, return a call to paginate for this query.
        return paginate(sesh, search_vehicles_q)
    except Exception as e:
        raise e
    

@router.get("/api/vehicles/years", response_model = Page[schemas.YearModel])
def search_vehicle_years(
    mk: str,
    t: str,
    mdl: str,
    sesh: DatabaseSessionDep
):
    """Search for vehicle years given make UID, type ID and model UID:
    :mk: The make UID.
    :t: The type ID.
    :mdl: The model's UID.
    
    This is a pagination route, so you may also provide the following arguments:
    :page: The requested page.
    :limit: The number per page."""
    try:
        LOG.debug(f"Attempting to locate vehicle years with make {mk}, type {t} and model {mdl}")
        # Assemble a query for the target entity given our input.
        search_vehicles_q, _ = vehicles.make_search_vehicles_query(dict(
            make_uid = mk, type_id = t, model_uid = mdl))
  
        # Now, return a call to paginate for this query.
        return paginate(sesh, search_vehicles_q)
    except Exception as e:
        raise e
    

@router.get("/api/vehicles/stock", response_model = Page[schemas.Stock])
def search_vehicles_stock(
    mk: str,
    t: str,
    mdl: str,
    y: int,
    sesh: DatabaseSessionDep
):
    """Search for vehicles given a set of cascading criteria. Accepted parameters (also in this order):
    :mk: The make UID.
    :t: The type ID.
    :mdl: The model's UID.
    :y: The target year.
    
    This is a pagination route, so you may also provide the following arguments:
    :page: The requested page.
    :limit: The number per page."""
    try:
        LOG.debug(f"Attempting to locate vehicle stocks with make {mk}, type {t}, model {mdl} and year {y}")
        # Assemble a query for the target entity given our input.
        search_vehicles_q, _ = vehicles.make_search_vehicles_query(dict(
            make_uid = mk, type_id = t, model_uid = mdl, year = y))
  
        # Now, return a call to paginate for this query.
        return paginate(sesh, search_vehicles_q)
    except Exception as e:
        raise e