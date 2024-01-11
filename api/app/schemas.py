from typing import List, Dict, Union

from pydantic import (
    Field,
    BaseModel,
    ConfigDict,
    model_validator
)


class VehicleArgs(BaseModel):
    """A model for containing and validating user sent arguments for a desired vehicle."""
    make_uid: Union[str, None] = None
    type_id: Union[str, None] = None
    model_uid: Union[str, None] = None
    year: Union[int, None] = None
    
    @model_validator(mode = "after")
    def ensure_arguments_cascade(self):
        """TODO: complete this.
        Arguments from top to bottom must be non-None consecutively, no argument must be skipped. Fail if this is not the case."""
        pass


class YearBase(BaseModel):
    """A base schema for a year."""
    year: int


class YearCreate(YearBase):
    pass


class Year(YearBase):
    model_config = ConfigDict(
        from_attributes = True)


class TypeBase(BaseModel):
    """A base schema for a vehicle's type."""
    type_id: str
    name: str
    description: str


class TypeCreate(TypeBase):
    pass


class Type(TypeBase):
    model_config = ConfigDict(
        from_attributes = True)


class YearModelBase(BaseModel):
    """A base schema for a vehicle's year model."""
    make_uid: str
    model_uid: str
    year: int


class YearModelCreate(YearModelBase):
    stock_vehicles: List["StockCreate"] = Field(alias = "vehicles")


class YearModel(YearModelBase):
    model_config = ConfigDict(
        from_attributes = True)


class ModelBase(BaseModel):
    """A base schema for loading a Model."""
    uid: str = Field(alias = str("model_uid"))
    make_uid: str
    name: str = Field(alias = str("model_name"))


class Model(ModelBase):
    model_config = ConfigDict(
        from_attributes = True)
    uid: str
    name: str
    type: Type


class ModelCreate(ModelBase):
    type_id: str
    year_models: Dict[int, YearModelCreate]


class MakeBase(BaseModel):
    """A base schema for loading a Make."""
    uid: str = Field(alias = str("make_uid"))
    name: str = Field(alias = str("make_name"))


class MakeCreate(MakeBase):
    models: Dict[str, ModelCreate]


class Make(MakeBase):
    model_config = ConfigDict(
        from_attributes = True)
    uid: str
    name: str


class StockBase(BaseModel):
    """A base schema for loading a Stock."""
    vehicle_uid: str

    badge: Union[str, None] = None
    version: Union[str, None] = None

    motor_type: str
    displacement: Union[int, None] = None
    induction: Union[str, None] = None
    fuel_type: Union[str, None] = None

    power: Union[int, None] = None
    elec_type: Union[str, None] = None

    trans_type: Union[str, None] = None
    num_gears: Union[int, None] = None


class StockCreate(StockBase):
    pass


class Stock(StockBase):
    model_config = ConfigDict(
        from_attributes = True)
    make: Make
    model: Model
    year_model_year_: int