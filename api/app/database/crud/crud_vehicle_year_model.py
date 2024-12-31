import datetime
import logging

from typing import Any, Dict, Optional, Union, List, Tuple

from sqlalchemy import select, asc, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from .. import errors
from ..models import VehicleYearModel
from ..schemas import VehicleYearModelCreate, VehicleYearModelUpdate

from app.logger import log


class CRUDVehicleYearModel(CRUDBase[VehicleYearModel, VehicleYearModelCreate, VehicleYearModelUpdate]):
    pass

vehicle_year_model = CRUDVehicleYearModel(VehicleYearModel)