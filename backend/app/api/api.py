from fastapi import APIRouter
from app.api.endpoints import lots, websockets, bookings, auth, health

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(health.router, tags=["health"])
api_router.include_router(lots.router, prefix="/lots", tags=["lots"])
api_router.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
api_router.include_router(websockets.router, tags=["websockets"])

