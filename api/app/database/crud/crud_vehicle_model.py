import datetime
import logging

from typing import Any, Dict, Optional, Union, List, Tuple

from sqlalchemy import select, asc, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from .. import errors
from ..models import VehicleModel
from ..schemas import VehicleModelCreate, VehicleModelUpdate

from app.logger import log


class CRUDVehicleModel(CRUDBase[VehicleModel, VehicleModelCreate, VehicleModelUpdate]):
    pass

vehicle_model = CRUDVehicleModel(VehicleModel)