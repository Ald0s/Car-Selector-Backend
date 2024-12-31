"""Definitions for various models."""
import os

from typing import Annotated, List, Literal, Optional, Dict, Union
from pydantic import BaseModel, RootModel, Field, computed_field


class BaseVehicle(BaseModel):
    id: str = Field(validation_alias = "vehicle_uid")
    vehicle_year_model_id: str = Field(validation_alias = "year_model_uid")


class Car(BaseVehicle):
    type_id: Literal["car"]
    motor_type: str
    trans_type: Optional[str] = None
    num_gears: Optional[int] = None
    displacement: Optional[float] = None
    version: Optional[str] = None
    induction: Optional[str] = None
    badge: Optional[str] = None
    fuel_type: Optional[str] = None
    power: Optional[float] = None
    elec_type: Optional[str] = None


class Bike(BaseVehicle):
    type_id: Literal["bike"]

# A nested type annotation combining both car and bike on the basis of
# the value of 'type_id' to discriminate between them.
Vehicle = Annotated[Union[Car, Bike], Field(discriminator = "type_id")]


class Logo(BaseModel):
    filename: str
    relative_path: str


class VehicleYearModel(BaseModel):
    id: str = Field(validation_alias = "year_model_uid")
    vehicle_make_id: str = Field(validation_alias = "make_uid")
    vehicle_model_id: str = Field(validation_alias = "model_uid")
    year: int
    vehicles: List[Vehicle]

    
class VehicleModel(BaseModel):
    id: str = Field(validation_alias = "model_uid")
    vehicle_make_id: str = Field(validation_alias = "make_uid")
    type_id: str
    name: str = Field(validation_alias = "model_name")
    year_models: List[VehicleYearModel]


class VehicleMake(BaseModel):
    id: str = Field(validation_alias = "make_uid")
    name: str = Field(validation_alias = "make_name")
    logo: Logo
    models: List[VehicleModel]

    @computed_field
    def logo_media_uri(self) -> str:
        """Return full relative path to logo item."""
        return os.path.join(
            self.logo.relative_path,
            self.logo.filename
        )


class VehicleType(BaseModel):
    type_id: str = Field(serialization_alias = "id")
    name: str
    description: str


class Vehicles(BaseModel):
    types: List[VehicleType]
    years: List[int]
    makes: List[VehicleMake]