import pytest
import json

from typing import Tuple

from fastapi import FastAPI
from sqlalchemy.orm import Session

from ..app import config, vehicles, models, schemas


class TestVehicleArgsModel():
    def test_ensure_fails_missed_arg(self):
        """Ensure attempting to make a vehicle args with non-consecutive arguments fails. For instance, provide make UID, type ID and year (missing model UID)."""
        bad_args = dict(
            make_uid = "MAKE", type_id = "TYPE", year = "2004")
        
        with pytest.raises(Exception) as e:
            # Now make a new vehicle args. Ensure this fails.
            schemas.VehicleArgs(**bad_args)


class TestMakeSearchVehicleQuery():
    def test_makes(self, sesh: Session, test_app: FastAPI):
        """Ensure an assembled query for Makes returns both Toyota and Mazda."""
        # Assemble the query, supply an empty dict.
        makes_q, MakeCls = vehicles.make_search_vehicles_query()
        # Ensure make cls is Make.
        assert MakeCls == schemas.Make
        # Query all results.
        all_makes = sesh.scalars(makes_q).all()
        # Ensure there's 2 in total.
        assert len(all_makes) == 2

    def test_types(self, sesh: Session, test_app: FastAPI):
        """Ensure an assembled query for Types with make UID 'mazda-GANMfBBPNc' returns one type; Car."""
        # Assemble the query, supply a dict with make UID set.
        types_q, TypeCls = vehicles.make_search_vehicles_query(dict(
            make_uid = "mazda-GANMfBBPNc"))
        # Ensure make cls is Type.
        assert TypeCls == schemas.Type
        # Ensure there's one type.
        all_types = sesh.scalars(types_q).all()
        assert len(all_types) == 1
        # Ensure that one type's name is 'Car'.
        assert all_types[0].name == "Car"

    def test_models(self, sesh: Session, test_app: FastAPI):
        """Ensure an assembled query for Models with make UID 'mazda-GANMfBBPNc' and type ID 'car' returns 3 models; '6', 'MX-5' and 'RX-7'"""
        # Assemble the query, supply a dict with make UID and type ID set.
        models_q, ModelCls = vehicles.make_search_vehicles_query(dict(
            make_uid = "mazda-GANMfBBPNc", type_id = "car"))
        # Ensure make cls is Model.
        assert ModelCls == schemas.Model
        # Ensure there's three models.
        all_models = sesh.scalars(models_q).all()
        assert len(all_models) == 3

    def test_year_models(self, sesh: Session, test_app: FastAPI):
        """Ensure an assembled query for Models with make UID 'mazda-GANMfBBPNc', type ID 'car' and model UID 'rx-7-3exDTapq5g'"""
        # Assemble the query, supply a dict with make UID, type ID and model UID set.
        year_models_q, YearModelCls = vehicles.make_search_vehicles_query(dict(
            make_uid = "mazda-GANMfBBPNc", type_id = "car", model_uid = "rx-7-3exDTapq5g"))
        # Ensure make cls is YearModel.
        assert YearModelCls == schemas.YearModel
        # Ensure there are 24 results in total.
        all_year_models = sesh.scalars(year_models_q).all()
        assert len(all_year_models) == 24

    def test_vehicles(self, sesh: Session, test_app: FastAPI):
        """Ensure an assembled query for Models with make UID 'mazda-GANMfBBPNc', type ID 'car', model UID 'rx-7-3exDTapq5g' and year 2000."""
        # Assemble the query, supply a dict with make UID set.
        vehicles_q, VehicleCls = vehicles.make_search_vehicles_query(dict(
            make_uid = "mazda-GANMfBBPNc", type_id = "car", model_uid = "rx-7-3exDTapq5g", year = 2000))
        # Ensure make cls is Stock.
        assert VehicleCls == schemas.Stock
        # Ensure there's 4 in total.
        vehicles_ = sesh.scalars(vehicles_q).all()
        assert len(vehicles_) == 4


class TestLoadVehicleData():
    pass


class TestLoadVehiclesFromFile():
    pass