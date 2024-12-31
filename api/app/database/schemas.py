from typing import Optional
from pydantic import BaseModel, ConfigDict


class VehicleTypeBase(BaseModel):
    name: str
    description: str


class VehicleTypeCreate(VehicleTypeBase):
    id: str


class VehicleTypeUpdate(VehicleTypeBase):
    name: Optional[str] = None
    description: Optional[str] = None


class VehicleBase(BaseModel):
    """Vehicle base should actually be an abstract type that refers to
    multiple children types like Car and Bike but for brevity, Vehicle
    is synonymous with Car.
    """
    motor_type: str
    trans_type: Optional[str]
    num_gears: Optional[int]
    displacement: Optional[float]
    version: Optional[str]
    induction: Optional[str]
    badge: Optional[str]
    fuel_type: Optional[str]
    power: Optional[float]
    elec_type: Optional[str]


class VehicleCreate(VehicleBase):
    id: str
    type_id: str
    vehicle_year_model_id: str


class VehicleUpdate(VehicleBase):
    motor_type: Optional[str] = None
    trans_type: Optional[str] = None
    num_gears: Optional[int] = None
    displacement: Optional[float] = None
    version: Optional[str] = None
    induction: Optional[str] = None
    badge: Optional[str] = None
    fuel_type: Optional[str] = None
    power: Optional[float] = None
    elec_type: Optional[str] = None


class VehicleYearModelBase(BaseModel):
    vehicle_make_id: str
    vehicle_model_id: str
    year: int


class VehicleYearModelCreate(VehicleYearModelBase):
    id: str


class VehicleYearModelUpdate(VehicleYearModelBase):
    vehicle_make_id: Optional[str] = None
    vehicle_model_id: Optional[str] = None
    year: Optional[int] = None


class VehicleModelBase(BaseModel):
    vehicle_make_id: str
    type_id: str
    name: str


class VehicleModelCreate(VehicleModelBase):
    id: str


class VehicleModelUpdate(VehicleModelBase):
    vehicle_make_id: Optional[str] = None
    type_id: Optional[str] = None
    name: Optional[str] = None


class VehicleMakeBase(BaseModel):
    name: str
    logo_media_uri: str


class VehicleMakeCreate(VehicleMakeBase):
    id: str


class VehicleMakeUpdate(VehicleMakeBase):
    name: Optional[str] = None
    logo_media_uri: Optional[str] = None