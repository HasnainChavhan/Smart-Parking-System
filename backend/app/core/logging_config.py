"""
Logging configuration using Loguru for structured, production-ready logging.
"""

import sys
import os
from pathlib import Path
from loguru import logger
from app.core.config import settings

# Remove default handler
logger.remove()

# Create logs directory if it doesn't exist
log_dir = Path(settings.LOG_FILE).parent
log_dir.mkdir(parents=True, exist_ok=True)

# Console handler with color formatting (for development)
logger.add(
    sys.stdout,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level=settings.LOG_LEVEL,
    colorize=True,
)

# File handler with rotation (for production)
logger.add(
    settings.LOG_FILE,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level=settings.LOG_LEVEL,
    rotation="10 MB",  # Rotate when file reaches 10MB
    retention="30 days",  # Keep logs for 30 days
    compression="zip",  # Compress rotated logs
    enqueue=True,  # Thread-safe logging
)

# Error file handler (separate file for errors)
logger.add(
    settings.LOG_FILE.replace(".log", "_error.log"),
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    level="ERROR",
    rotation="10 MB",
    retention="60 days",  # Keep error logs longer
    compression="zip",
    enqueue=True,
)

# JSON format for production (easier to parse)
if settings.ENVIRONMENT == "production":
    logger.add(
        settings.LOG_FILE.replace(".log", "_json.log"),
        format="{message}",
        level=settings.LOG_LEVEL,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        serialize=True,  # JSON format
        enqueue=True,
    )

logger.info(f"Logging initialized - Level: {settings.LOG_LEVEL}, Environment: {settings.ENVIRONMENT}")
