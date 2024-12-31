import datetime
import logging

from typing import Any, Dict, Optional, Union, List, Tuple

from sqlalchemy import select, asc, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from .. import errors
from ..models import VehicleType
from ..schemas import VehicleTypeCreate, VehicleTypeUpdate

from app.logger import log


class CRUDVehicleType(CRUDBase[VehicleType, VehicleTypeCreate, VehicleTypeUpdate]):
    pass

vehicle_type = CRUDVehicleType(VehicleType)