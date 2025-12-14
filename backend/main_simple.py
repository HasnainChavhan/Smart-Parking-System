"""
Simplified main.py without complex logging
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# CORS - Allow file:// protocol (null origin) for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins including null
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    allow_origin_regex=".*"  # Allow any origin pattern
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
    print("=" * 60)
    
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
