from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

from app.api.api import api_router
from app.core.config import settings
from app.core.middleware import RequestIDMiddleware, LoggingMiddleware, ErrorHandlingMiddleware
from app.core.exceptions import ParkingSystemException
from app.core import logging_config  # Initialize logging
from loguru import logger


# Lifespan context manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting {settings.PROJECT_NAME} - Environment: {settings.ENVIRONMENT}")
    logger.info(f"API Documentation available at: http://{settings.HOST}:{settings.PORT}/docs")
    yield
    # Shutdown
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Smart Car Parking System with Real-time Detection and Booking",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
if settings.RATE_LIMIT_ENABLED:
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# Add custom middleware (order matters - first added is outermost)
app.add_middleware(ErrorHandlingMiddleware)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)

# CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info(f"CORS enabled for origins: {settings.BACKEND_CORS_ORIGINS}")


# Exception handlers
@app.exception_handler(ParkingSystemException)
async def parking_system_exception_handler(request: Request, exc: ParkingSystemException):
    """Handle custom parking system exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "status_code": exc.status_code,
            "details": exc.details,
            "request_id": getattr(request.state, "request_id", None)
        }
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    logger.warning(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": exc.errors(),
            "request_id": getattr(request.state, "request_id", None)
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.exception(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An unexpected error occurred",
            "request_id": getattr(request.state, "request_id", None)
        }
    )


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Root endpoint
@app.get("/", tags=["Root"])
@limiter.limit(f"{settings.RATE_LIMIT_PER_MINUTE}/minute")
async def root(request: Request):
    """
    Root endpoint with API information.
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME} API",
        "version": "1.0.0",
        "environment": settings.ENVIRONMENT,
        "docs": f"/docs",
        "health": f"{settings.API_V1_STR}/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

