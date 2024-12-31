"""Assemble all available routes."""
from fastapi import APIRouter

from .general import router as general_router
from .vehicles import router as vehicle_router


# Create a single router for API overall.
api_router = APIRouter(
    prefix = "/api",
    tags = ["api"]
)

# Add all other routes to this router.
api_router.include_router(general_router)
api_router.include_router(vehicle_router)