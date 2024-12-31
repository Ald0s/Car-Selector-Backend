"""Response & request schemas for the API."""
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, computed_field


class VehicleResponse(BaseModel):
    """A vehicle refers to JUST a car in this project.
    Figure it out yourself, loser.
    """
    model_config = ConfigDict(
        from_attributes = True
    )
    id: str
    vehicle_year_model_id: str = Field(serialization_alias = "vehicleYearModelId")
    motor_type: str = Field(serialization_alias = "motorType")
    trans_type: Optional[str] = Field(serialization_alias = "transmissionType")
    num_gears: Optional[int] = Field(serialization_alias = "numGears")
    displacement: Optional[float] = Field(serialization_alias = "displacementLiters")
    version: Optional[str]
    induction: Optional[str]
    badge: Optional[str]
    fuel_type: Optional[str] = Field(serialization_alias = "fuelType")
    power: Optional[float]
    elec_type: Optional[str] = Field(serialization_alias = "elecType")
    title: str

    @computed_field
    def yearModelSpec(self) -> str:
        """Return a string containing this vehicle's unique options. An example
        is something like 'RZ 3.0L T 6 spd Manual'
        """
        result: str = ""
        if self.badge is not None:
            result += self.badge + " "
        elif self.version is not None:
            result += self.version + " "
        if self.motor_type == "piston":
            result += "%.1fL %s" % (self.displacement, self.induction,)
        elif self.motor_type == "rotary":
            return "%.1fL Rotary %s" % (self.displacement, self.induction,)
        elif self.motor_type == "electric":
            raise NotImplementedError("electric motor types not implemented "\
                                      "in options!")
        else:
            raise NotImplementedError
        if self.trans_type == "A":
            result += " %d spd Automatic" % self.num_gears
        elif self.trans_type == "M":
            result += " %d spd Manual" % self.num_gears
        else:
            raise NotImplementedError
        return result


class VehicleYearModelResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )
    id: str
    vehicle_make_id: str = Field(serialization_alias = "vehicleMakeId")
    vehicle_model_id: str = Field(serialization_alias = "vehicleModelId")
    year: int


class VehicleModelResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )
    id: str
    name: str
    vehicle_make_id: str = Field(serialization_alias = "vehicleMakeId")
    type_id: str = Field(serialization_alias = "typeId")


class VehicleTypeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )
    id: str
    name: str
    description: str


class VehicleMakeResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes = True
    )
    id: str
    name: str