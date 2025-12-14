"""
Custom middleware for request handling, logging, and error tracking.
"""

import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request for tracking."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses with timing information."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = getattr(request.state, "request_id", "unknown")
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request started | ID: {request_id} | Method: {request.method} | "
            f"Path: {request.url.path} | Client: {request.client.host if request.client else 'unknown'}"
        )
        
        # Process request
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            
            # Log response
            logger.info(
                f"Request completed | ID: {request_id} | Status: {response.status_code} | "
                f"Duration: {process_time:.3f}s"
            )
            
            # Add timing header
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            process_time = time.time() - start_time
            logger.error(
                f"Request failed | ID: {request_id} | Error: {str(e)} | "
                f"Duration: {process_time:.3f}s"
            )
            raise


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Catch and log unhandled exceptions."""
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            request_id = getattr(request.state, "request_id", "unknown")
            logger.exception(
                f"Unhandled exception | ID: {request_id} | Path: {request.url.path} | "
                f"Error: {str(e)}"
            )
            raise
