import datetime
import logging

from typing import Any, Dict, Optional, Union, List, Tuple

from sqlalchemy import select, asc, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from .. import errors
from ..models import Vehicle
from ..schemas import VehicleCreate, VehicleUpdate

from app.logger import log


class CRUDVehicle(CRUDBase[Vehicle, VehicleCreate, VehicleUpdate]):
    pass

vehicle = CRUDVehicle(Vehicle)