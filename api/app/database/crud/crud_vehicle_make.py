import datetime
import logging

from typing import Any, Dict, Optional, Union, List, Tuple

from sqlalchemy import select, asc, and_, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from .. import errors
from ..models import VehicleMake
from ..schemas import VehicleMakeCreate, VehicleMakeUpdate

from app.logger import log


class CRUDVehicleMake(CRUDBase[VehicleMake, VehicleMakeCreate, VehicleMakeUpdate]):
    async def get_by_id(
        self, 
        sesh: AsyncSession,
        make_id: str
    ) -> Optional[VehicleMake]:
        """Find a vehicle make with the given ID."""
        select_vehicle_make_stmt = (
            select(VehicleMake)
            .where(VehicleMake.id == make_id)
        )
        result = await sesh.execute(select_vehicle_make_stmt)
        return result.scalar()

vehicle_make = CRUDVehicleMake(VehicleMake)