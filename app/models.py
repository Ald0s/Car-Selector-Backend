from typing import Any, List, Dict, Union

from sqlalchemy import create_engine
from sqlalchemy.orm import as_declarative, sessionmaker, Session
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy import String, Text, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.expression import cast
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy

from app import config

# Create a new engine. Check same thread only required for SQLite, not other databases.
engine = create_engine(config.SQLALCHEMY_DATABASE_URI,
    connect_args = config.SQLALCHEMY_CONNECT_ARGS, poolclass = config.SQLALCHEMY_POOLCLASS)

# Create a sessionmaker bound to this engine we just created.
SessionLocal = sessionmaker(
    autocommit = False, autoflush = False, bind = engine)


def init_database(sesh: Session, **kwargs) -> Session:
    """Initialise the database by creating all tables on the given session."""
    try:
        Model.metadata.create_all(
            bind = engine)
        return sesh
    except Exception as e:
        raise e


@as_declarative()
class Model():
    """A class that represents a the declarative base. All models will extend from this class."""
    id: Any

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class VehicleType(Model):
    """A general overview of a specific type of vehicle such as a Car or Bike."""
    __tablename__ = "vehicle_type"

    type_id: Mapped[str] = mapped_column(String(32), primary_key = True)

    # The name of this vehicle type. Can't be None; this is also unique.
    name: Mapped[str] = mapped_column(String(32), unique = True, nullable = False)
    # The description of this vehicle type. Can't be None.
    description: Mapped[str] = mapped_column(Text(), nullable = False)

    # Relationship to the vehicle model table, all models that are this vehicle type.
    models_: Mapped[List["VehicleModel"]] = relationship(
        back_populates = "type",
        uselist = True)

    def __repr__(self):
        return f"VehicleType<{self.name}>"
    
    '''@property
    def models(self) -> List["VehicleModel"]:
        """Return the models attached to this vehicle type."""
        return self.models_

    @models.setter
    def models(self, value):
        """Set the models attached to this vehicle type."""
        raise NotImplementedError
        self.models_ = value.values()'''


class VehicleYear(Model):
    """A single year of vehicles."""
    __tablename__ = "vehicle_year"

    year_: Mapped[int] = mapped_column(primary_key = True)

    def __repr__(self):
        return f"VehicleYear<{self.year_}>"
    
    @property
    def year(self) -> int:
        """Return this year."""
        return self.year_


class VehicleMake(Model):
    """A single vehicle make, that can refer to many vehicle models."""
    __tablename__ = "vehicle_make"

    uid: Mapped[str] = mapped_column(String(128), primary_key = True)

    # The name of this vehicle make. Can't be None; this is also unique.
    name: Mapped[str] = mapped_column(String(48), nullable = False)

    # A relationship to the make table, all models within this vehicle.
    models_: Mapped[List["VehicleModel"]] = relationship(
        back_populates = "make",
        uselist = True)

    def __repr__(self):
        return f"VehicleMake<{self.name}>"
    
    @property
    def models(self) -> List["VehicleModel"]:
        return self.models_

    @models.setter
    def models(self, models_dict: Dict[str, Dict]):
        """Set models within this make to vehicle model instances."""
        self.models_ = [VehicleModel(**x) for x in models_dict.values()]


class VehicleModel(Model):
    """A single vehicle model, which is owned by a single vehicle make, and is differentiated by its name and type. This is where we can abstract a single make
    also producing cars if they're primarily a bike producer etc."""
    __tablename__ = "vehicle_model"

    uid: Mapped[str] = mapped_column(String(128), primary_key = True)
    # The vehicle model's make UID. This can't be None.
    make_uid: Mapped[str] = mapped_column(String(128), ForeignKey("vehicle_make.uid"), nullable = False)
    # The vehicle type's ID. This can't be None.
    type_id: Mapped[str] = mapped_column(String(32), ForeignKey("vehicle_type.type_id"), nullable = False)

    # The name of this vehicle make. Can't be None; this is also unique.
    name: Mapped[str] = mapped_column(String(48), nullable = False)
    
    # Relationship to the vehicle type for this model. This is eager.
    type: Mapped[VehicleType] = relationship(
        back_populates = "models_",
        uselist = False)
    # Relationship to the vehicle make for this model. This is eager.
    make: Mapped[VehicleMake] = relationship(
        back_populates = "models_",
        uselist = False)
    # Relationship to all year models.
    year_models_: Mapped[List["VehicleYearModel"]] = relationship(
        back_populates = "model",
        uselist = True)

    def __repr__(self):
        return f"VehicleModel<{self.name},mk={self.make.name}>"
    
    @property
    def year_models(self) -> List["VehicleYearModel"]:
        return self.year_models_

    @year_models.setter
    def year_models(self, year_models_dict: Dict[str, Dict]):
        """Set year models within this model to vehicle year model instances."""
        self.year_models_ = [VehicleYearModel(**x) for x in year_models_dict.values()]


class VehicleYearModel(Model):
    """A single vehicle year model, owned by a single vehicle model; this entity centralises all individually optioned stock vehicles for a specific model and year."""
    __tablename__ = "vehicle_year_model"

    # The primary key for the vehicle year model is a composite made up of make UID, model UID and the year.
    # The make's UID, referring to VehicleMake. This can't be None.
    make_uid: Mapped[str] = mapped_column(String(128), ForeignKey("vehicle_make.uid"), primary_key = True)
    # The model's UID, referring to VehicleModel. This can't be None.
    model_uid: Mapped[str] = mapped_column(String(128), ForeignKey("vehicle_model.uid"), primary_key = True)
    # The year, referring to VehicleYear. This can't be None.
    year_: Mapped[int] = mapped_column(ForeignKey("vehicle_year.year_"), primary_key = True)

    # An eager relationship to this year model's make. This does not back populate.
    make: Mapped[VehicleMake] = relationship(
        uselist = False)
    # An eager relationship to this year model's model. This does not back populate.
    model: Mapped[VehicleModel] = relationship(
        uselist = False)
    # A relationship to stock vehicles.
    stock_vehicles_: Mapped[List["VehicleStock"]] = relationship(
        back_populates = "year_model",
        uselist = True)

    def __repr__(self):
        return f"VehicleYearModel<{self.year_},mdl={self.make.name} {self.model.name}>"
    
    @property
    def year(self) -> int:
        """Return the year."""
        return self.year_
    
    @year.setter
    def year(self, value: int):
        self.year_ = value
    
    @property
    def stock_vehicles(self) -> List["VehicleStock"]:
        """Return all stock vehicles."""
        return self.stock_vehicles_

    @stock_vehicles.setter
    def stock_vehicles(self, value: List[Dict]):
        """Set stock vehicles to vehicle stock instances from all dicts in value."""
        self.stock_vehicles_ = [VehicleStock(**x) for x in value]
    
    @hybrid_property
    def make_name(self) -> str:
        return self.make.name
    
    @make_name.expression
    def make_name(cls):
        """Join dependant. Remember to therefore join VehicleMake somehow."""
        return VehicleMake.name

    @hybrid_property
    def model_name(self) -> str:
        return self.model.name
    
    @model_name.expression
    def model_name(cls):
        """Join dependant. Remember to therefore join VehicleModel somehow."""
        return VehicleModel.name
    

class VehicleStock(Model):
    """A single stock vehicle. These UIDs can be thought of as associating with a single specific vehicle."""
    __tablename__ = "vehicle_stock"

    # The vehicle stock's UID.
    vehicle_uid: Mapped[str] = mapped_column(String(128), primary_key = True)
    # A composite foreign key to the vehicle year model entity. None of these can be None.
    year_model_make_uid: Mapped[str] = mapped_column(String(128), nullable = False)
    year_model_model_uid: Mapped[str] = mapped_column(String(128), nullable = False)
    year_model_year_: Mapped[int] = mapped_column(nullable = False)

    # The vehicle stock's version. Can be None.
    version: Mapped[str] = mapped_column(nullable = True, default = None)
    # The vehicle stock's badge. Can be None.
    badge: Mapped[str] = mapped_column(nullable = True, default = None)

    # General motor type; piston, electric, rotary. This can't be None, and should be one of 'piston', 'rotary', 'hybrid' or 'electric'.
    motor_type: Mapped[str] = mapped_column(nullable = False)

    ### Specifics for Piston/Rotary types. ###
    # The displacement, in CC. Can be None.
    displacement: Mapped[int] = mapped_column(nullable = True)
    # The induction type. Can be None.
    induction: Mapped[str] = mapped_column(nullable = True)
    # The fuel type. Can be None.
    fuel_type: Mapped[str] = mapped_column(nullable = True)

    ### Specifics for Electric types. ###
    # The amount of power this motor produces. Can be None.
    power: Mapped[int] = mapped_column(nullable = True)
    # The type of electric motor(s). Can be None.
    elec_type: Mapped[str] = mapped_column(nullable = True)

    ### Transmission information. ###
    # The transmission type. Can't be None.
    trans_type: Mapped[str] = mapped_column(nullable = False)
    # The number of gears in this transmission. Can't be None.
    num_gears: Mapped[int] = mapped_column(nullable = False)

    # Association proxy through year model to the vehicle Make entity.
    make: AssociationProxy[VehicleMake] = association_proxy("year_model", "make")
    # Association proxy through year model to the vehicle Model entity.
    model: AssociationProxy[VehicleModel] = association_proxy("year_model", "model")
    # An eager relationship to the year model entity to which this stock vehicle belongs.
    year_model: Mapped[VehicleYearModel] = relationship(
        back_populates = "stock_vehicles_",
        uselist = False)
    
    __table_args__ = (
        ForeignKeyConstraint(
            ["year_model_make_uid", "year_model_model_uid", "year_model_year_"], 
            ["vehicle_year_model.make_uid", "vehicle_year_model.model_uid", "vehicle_year_model.year_"],),)
    
    def __repr__(self):
        return f"VehicleStock<{self.title}>"

    @hybrid_property
    def title(self) -> str:
        """Return a central 'title' for this stock vehicle. This should be a displayable text that uniquely identifies this vehicle and perhaps some of the
        more important options that separates it from the rest."""
        return f"{self.year_model_year_} {self.make.name} {self.model.name}"
    
    @title.expression
    def title(cls):
        """Expression equivalent for the title property. Remember, this is join dependant. In order for this to work properly, ensure you join vehicle stocks'
        year_model attribute, then vehicle year models' make attribute, then vehicle year models' model attribute in your end query."""
        return (
            cast(cls.year_model_year_, String)
            + " "
            + cast(VehicleYearModel.make_name, String)
            + " "
            + cast(VehicleYearModel.model_name, String)
        )
    
    def set_year_model(self, make_uid: str, model_uid: str, year: int):
        """Set the vehicle year model to which this vehicle stock belongs."""
        self.year_model_make_uid = make_uid
        self.year_model_model_uid = model_uid
        self.year_model_year_ = year

    def set_version(self, version: Union[str, None]):
        """Set this vehicle stock's version."""
        self.version = version

    def set_badge(self, badge: Union[str, None]):
        """Set this vehicle stock's badge."""
        self.badge = badge

    def set_motor_type(self, motor_type: str):
        """Set this vehicle's motor type; piston, rotary, electric etc."""
        self.motor_type = motor_type
    
    def set_displacement(self, displacement_cc: Union[int, None]):
        """Set this vehicle's displacement, in CC."""
        self.displacement = displacement_cc
    
    def set_induction_type(self, induction: Union[str, None]):
        """Set this vehicle's induction type."""
        self.induction = induction

    def set_fuel_type(self, fuel_type: Union[str, None]):
        """Set this vehicle's fuel type."""
        self.fuel_type = fuel_type

    def set_power(self, power: Union[int, None]):
        """Set this vehicle's power amount (for electric motors.)"""
        self.power = power

    def set_electric_motor_type(self, elec_type: Union[str, None]):
        """Set this vehicle's electric motor(s) type(s)."""
        self.elec_type = elec_type

    def set_transmission_type(self, trans_type: Union[str, None]):
        """Set this vehicle's transmission type."""
        self.trans_type = trans_type

    def set_num_gears(self, num_gears: Union[int, None]):
        """Set the number of gears on this vehicle's transmission."""
        self.num_gears = num_gears