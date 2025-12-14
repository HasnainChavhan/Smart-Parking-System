"""
Simplified main.py with custom CORS handling for file:// protocol
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.api.api import api_router
from app.db.session import engine
from app.db.models import Base

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Smart Parking System API",
    version="1.0.0"
)

# Custom middleware to handle CORS for null origin (file:// protocol)
@app.middleware("http")
async def custom_cors_middleware(request: Request, call_next):
    response = await call_next(request)
    
    # Get the origin from the request
    origin = request.headers.get("origin", "*")
    
    # Allow all origins including null (file://)
    response.headers["Access-Control-Allow-Origin"] = origin if origin != "null" else "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    response.headers["Access-Control-Expose-Headers"] = "*"
    
    return response

# Handle preflight requests
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    origin = request.headers.get("origin", "*")
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": origin if origin != "null" else "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        }
    )

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "Smart Parking System API", "status": "running"}

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 Smart Parking System - Backend API")
    print("=" * 60)
    print("✓ Server starting on http://localhost:8000")
    print("✓ API docs: http://localhost:8000/docs")
    print("✓ CORS enabled for file:// protocol")
    print("=" * 60)
    
    uvicorn.run(
        "main_cors_fixed:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
