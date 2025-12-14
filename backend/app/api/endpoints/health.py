"""
Health check endpoints for monitoring service status.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
import httpx
from datetime import datetime

from app.db import session
from app.core.config import settings
from loguru import logger

router = APIRouter()


@router.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """
    Basic health check endpoint.
    Returns 200 OK if service is running.
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Car Parking System API"
    }


@router.get("/health/detailed", status_code=status.HTTP_200_OK)
def detailed_health_check(db: Session = Depends(session.get_db)):
    """
    Detailed health check including database and ML service status.
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Car Parking System API",
        "environment": settings.ENVIRONMENT,
        "components": {}
    }
    
    # Check database connection
    try:
        db.execute(text("SELECT 1"))
        health_status["components"]["database"] = {
            "status": "healthy",
            "type": "sqlite" if "sqlite" in settings.DATABASE_URL else "postgresql"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        health_status["components"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    # Check ML service
    try:
        response = httpx.get(f"{settings.ML_SERVICE_URL}/health", timeout=2.0)
        if response.status_code == 200:
            health_status["components"]["ml_service"] = {
                "status": "healthy",
                "url": settings.ML_SERVICE_URL
            }
        else:
            health_status["components"]["ml_service"] = {
                "status": "unhealthy",
                "url": settings.ML_SERVICE_URL,
                "http_status": response.status_code
            }
            health_status["status"] = "degraded"
    except Exception as e:
        logger.warning(f"ML service health check failed: {str(e)}")
        health_status["components"]["ml_service"] = {
            "status": "unreachable",
            "url": settings.ML_SERVICE_URL,
            "error": str(e)
        }
        health_status["status"] = "degraded"
    
    return health_status
