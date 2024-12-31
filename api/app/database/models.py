"""Database models defined here."""
from typing import Any, List, Dict, Union, Optional

from sqlalchemy import create_engine, func
from sqlalchemy.orm import as_declarative, sessionmaker, Session
from sqlalchemy.ext.declarative import declared_attr

from sqlalchemy import String, Text, Numeric, ForeignKey, ForeignKeyConstraint
from sqlalchemy.sql.expression import ColumnElement, cast
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.associationproxy import association_proxy, AssociationProxy

from app import config, database as db


class VehicleType(db.Model):
    """A single vehicle type."""
    __tablename__ = "vehicle_type"

    # The vehicle type's short name.
    id: Mapped[str] = mapped_column(String(24), nullable = False, primary_key = True)
    # Vehicle type's friendly name.
    name: Mapped[str] = mapped_column(String(64), nullable = False)
    # Vehicle type's description.
    description: Mapped[str] = mapped_column(String(128), nullable = False)


class Vehicle(db.Model):
    """A single vehicle within a year model. This essentially communicates
    varying trim levels on that vehicle.
    """
    __tablename__ = "vehicle"

    # A UUID that identifies this vehicle.
    id: Mapped[str] = mapped_column(String(64), nullable = False, primary_key = True)
    # The vehicle's type ID. Refers the type table. Can't be None. If the type is deleted,
    # this vehicle must be deleted.
    type_id: Mapped[str] = mapped_column(
        String(24),
        ForeignKey("vehicle_type.id", ondelete = "CASCADE"),
        nullable = False
    )
    # The year model to which this vehicle belongs. If the year model is deleted, this vehicle
    # must be deleted.
    vehicle_year_model_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("vehicle_year_model.id", ondelete = "CASCADE"),
        nullable = False
    )
    # Motor type is required.
    motor_type: Mapped[str] = mapped_column(String(32), nullable = False)

    # The vehicle's version. This can be None.
    version: Mapped[Optional[str]] = mapped_column(
        String(64), 
        nullable = True, 
        default = None
    )
    # The vehicle's badge. This can be None.
    badge: Mapped[Optional[str]] = mapped_column(
        String(64), 
        nullable = True, 
        default = None
    )
    # Transmission type; can be None.
    trans_type: Mapped[Optional[str]] = mapped_column(
        String(24), 
        nullable = True, 
        default = None
    )
    # The number of gears in this transmission. Can be None.
    num_gears: Mapped[Optional[int]] = mapped_column(nullable = True, default = None)
    # Displacement can be None; this is in liters.
    displacement: Mapped[Optional[float]] = mapped_column(
        Numeric(3, 1),
        nullable = True, 
        default = None
    )
    # The induction type. This can be None.
    induction: Mapped[Optional[str]] = mapped_column(
        String(24),
        nullable = True,
        default = None
    )
    # The fuel type. This can be None.
    fuel_type: Mapped[Optional[str]] = mapped_column(
        String(24),
        nullable = True,
        default = None
    )
    # Power; referring only to ELECTRIC vehicles. Can be None.
    power: Mapped[Optional[float]] = mapped_column(
        Numeric(3, 1),
        nullable = True,
        default = None
    )
    # The type of eletric motor. This can be None.
    elec_type: Mapped[Optional[str]] = mapped_column(
        String(24),
        nullable = True,
        default = None
    )

    # Association proxy to the vehicle's make through year model.
    make: AssociationProxy["VehicleMake"] = association_proxy("year_model", "make")
    # Association proxy to the vehicle's model through year model.
    model: AssociationProxy["VehicleModel"] = association_proxy("year_model", "model")
    # The type of vehicle. Can't be None.
    type: Mapped["VehicleType"] = relationship(
        uselist = False
    )
    # The vehicle year model describing this Vehicle. Can't be None.
    year_model: Mapped["VehicleYearModel"] = relationship(
        back_populates = "vehicles",
        uselist = False
    )

    @hybrid_property
    def title(self) -> str:
        """Return a title for this vehicle. Consists of the year, make name
        and model name. Like 1994 Toyota Supra.
        """
        return "%d %s %s" % (self.year_model.year, self.make.name, self.model.name,)
    
    @title.inplace.expression
    @classmethod
    def _title(cls) -> ColumnElement[str]:
        """Expression level title relies on joins to year model,
        make and model.
        """
        return cast(VehicleYearModel.year, String) + " " \
            + VehicleMake.name + " " \
            + VehicleModel.name


class VehicleYearModel(db.Model):
    """A single vehicle year model, within a model."""
    __tablename__ = "vehicle_year_model"

    # A unique string identifying this model.
    id: Mapped[str] = mapped_column(String(64), nullable = False, primary_key = True)
    # The make this year model belongs to, refers to vehicle make.
    vehicle_make_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("vehicle_make.id"),
        nullable = False
    )
    # The model this year model belongs to, refers to vehicle model.
    vehicle_model_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("vehicle_model.id"),
        nullable = False
    )
    # This year models year.
    year: Mapped[int] = mapped_column(nullable = False)

    # The vehicle make this year model belongs to. Can't be None.
    make: Mapped["VehicleMake"] = relationship(
        uselist = False
    )
    # The vehicle model this year model belongs to. Can't be None.
    model: Mapped["VehicleModel"] = relationship(
        uselist = False
    )
    # All vehicles belonging to this year model.
    vehicles: Mapped[List[Vehicle]] = relationship(
        back_populates = "year_model",
        uselist = True
    )


class VehicleModel(db.Model):
    """A single vehicle model, within a make."""
    __tablename__ = "vehicle_model"

    # A unique string identifying this model.
    id: Mapped[str] = mapped_column(String(64), nullable = False, primary_key = True)
    # The make this model belongs to, refers to vehicle make.
    vehicle_make_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("vehicle_make.id"),
        nullable = False
    )
    # This models' type ID, refers to vehicle type.
    type_id: Mapped[str] = mapped_column(
        String(24), 
        ForeignKey("vehicle_type.id"),
        nullable = False
    )
    # The model's name.
    name: Mapped[str] = mapped_column(String(128), nullable = False)

    # The type that describes this model. Can't be None.
    type: Mapped[VehicleType] = relationship(
        uselist = False
    )
    # The vehicle make that owns this model. Can't be None.
    make: Mapped["VehicleMake"] = relationship(
        back_populates = "models",
        uselist = False
    )


class VehicleMake(db.Model):
    """A single vehicle make."""
    __tablename__ = "vehicle_make"

    # A unique string identifying this make. Looks like toyota-XXXXXXX
    id: Mapped[str] = mapped_column(String(64), nullable = False, primary_key = True)
    # The make's name.
    name: Mapped[str] = mapped_column(String(128), nullable = False)
    # The make's logo, can't be None. This will be something like; import/vehicles/logos/toyota.png
    logo_media_uri: Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    # All models belonging to this make.
    models: Mapped[List[VehicleModel]] = relationship(
        back_populates = "make",
        uselist = True
    )