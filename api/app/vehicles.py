"""A module for importing vehicle data."""
import os
import json
import logging

from typing import Union, Type as Type_, Tuple, Any

from pydantic import (
    BaseModel
)
from sqlalchemy import select
from sqlalchemy.orm import Session, Query

from . import config, models
from .schemas import *

LOG = logging.getLogger("carselector.routes")
LOG.setLevel(logging.DEBUG)


class VehicleData(BaseModel):
    """The actual vehicle data stored within a master object."""
    version: str
    version_code: int
    environment: str
    types: List[TypeCreate]
    years: List[int]


class VehicleDataMaster(BaseModel):
    """Master input vehicle data schema- load raw vehicles JSON with this."""
    master: VehicleData
    makes: Dict[str, MakeCreate]


def make_search_vehicles_query(
    input_: Union[Dict, VehicleArgs] = dict()
) -> Tuple[Query, Type_]:
    """Assemble a query for a particular vehicle entity and return it. Based on the input.
    
    Arguments
    ---------
    :input_: Either a dictionary or an instance of VehicleArgs. If directory given, an args will automatically be created."""
    try:
        if isinstance(input_, dict):
            input_ = VehicleArgs(
                **input_)
        elif not isinstance(input_, VehicleArgs):
            # Unrecognised type
            raise TypeError
        
        # Now, construct and return our query.
        result_query = None
        if not input_.make_uid and not input_.type_id and not input_.model_uid and not input_.year:
            # We have been given no arguments at all. Return a query for all makes.
            LOG.debug(f"Querying all vehicle makes!")
            result_query = select(models.VehicleMake)
            OutputCls = Make

        elif not input_.type_id and not input_.model_uid and not input_.year:
            # We have been given just a vehicle make. Return a query for types for that make.
            LOG.debug(f"Querying vehicle types within make {input_.make_uid}!")
            result_query = (
                select(models.VehicleType)
                    .join(models.VehicleModel, models.VehicleModel.type_id == models.VehicleType.type_id)
                    .where(models.VehicleModel.make_uid == input_.make_uid)
                    .group_by(models.VehicleType.type_id)
            )
            OutputCls = Type

        elif not input_.model_uid and not input_.year:
            # We have been given a make UID and a type ID. Return a query for models for that make and type ID.
            LOG.debug(f"Querying vehicle models within make {input_.make_uid} and type ID {input_.type_id}!")
            result_query = (
                select(models.VehicleModel)
                    .where(models.VehicleModel.make_uid == input_.make_uid)
                    .where(models.VehicleModel.type_id == input_.type_id)
            )
            OutputCls = Model

        elif not input_.year:
            # We have been given a make UID, type ID and a model UID. Return a query for year models for that make, type ID and model; ordered in descending fashion.
            LOG.debug(f"Querying vehicle year models within make {input_.make_uid}, type ID {input_.type_id} and model {input_.model_uid}!")
            result_query = (
                select(models.VehicleYearModel)
                    .where(models.VehicleYearModel.make_uid == input_.make_uid)
                    .where(models.VehicleYearModel.model_uid == input_.model_uid)
                    .order_by(models.VehicleYearModel.year_.desc())
            )
            OutputCls = YearModel

        else:
            # We have been given ALL arguments. Return a query for vehicle stocks for that type ID, make, model and year.
            LOG.debug(f"Querying vehicle stocks within make {input_.make_uid}, type ID {input_.type_id}, model {input_.model_uid} and year {input_.year}!")
            result_query = (
                select(models.VehicleStock)
                    .where(models.VehicleStock.year_model_make_uid == input_.make_uid)
                    .where(models.VehicleStock.year_model_model_uid == input_.model_uid)
                    .where(models.VehicleStock.year_model_year_ == input_.year)
            )
            OutputCls = Stock
        
        # Return the query and output class type.
        return result_query, OutputCls
    except Exception as e:
        raise e
    

def load_vehicle_data(sesh: Session, vehicle_data: VehicleDataMaster):
    """Load the given vehicle data into session provided.
    
    Arguments
    ---------
    :sesh: The database session on which to perform our operations.
    :vehicle_data: An instance of VehicleDataMaster from which to load the data."""
    try:
        # Iterate all types in master record and ensure each is created.
        for type_create in vehicle_data.master.types:
            # Ensure this type is created.
            vehicle_type = models.VehicleType(
                **(type_create.model_dump()))
            # Merge with session.
            sesh.merge(vehicle_type)
        
        # Iterate all years in master record and ensure each is created.
        for year in vehicle_data.master.years:
            # Ensure this year is created.
            vehicle_year = models.VehicleYear(
                year_ = year)
            # Merge with session.
            sesh.merge(vehicle_year)

        # Iterate all makes as values.
        for make_name, make_create in vehicle_data.makes.items():
            # Ensure this make is created, this will also merge all dependants.
            vehicle_make = models.VehicleMake(
                **(make_create.model_dump()))
            # Merge with session.
            sesh.merge(vehicle_make)
    except Exception as e:
        raise e


def load_vehicles_from_file(sesh: Session, filename: str, *,
    relative_dir: Union[str, None] = ""
):
    """Load vehicles from the given file.
    
    Arguments
    ---------
    :sesh: The database session on which to perform our operations.
    :filename: The filename for the target JSON file.
    
    Keyword arguments
    -----------------
    :relative_dir: Optionally, a directory relative to current working directory in which to find the file. Default is empty."""
    try:
        # Build an absolute path.
        absolute_path = os.path.join(os.getcwd(), config.IMPORT_PATH, relative_dir, filename)
        if not os.path.isfile(absolute_path):
            """TODO: handle this correctly."""
            raise NotImplementedError(f"Failed to load vehicle data from {absolute_path}, this file does not exist.")
        # Our result object.
        vehicle_data = None
        with open(absolute_path, "r") as f:
            # Read all content from the file and load as JSON.
            vehicle_data_d = json.loads(f.read())
            # Now, instantiate a creation model.
            vehicle_data = VehicleDataMaster(**vehicle_data_d)
        # Now, load this data into database session.
        load_vehicle_data(sesh, vehicle_data)
    except Exception as e:
        raise e
