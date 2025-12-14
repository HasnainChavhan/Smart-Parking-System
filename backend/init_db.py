"""
Simple database initialization
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

# Create engine
engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})

# Import Base from models
from app.db.models import Base

# Create all tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✓ Database initialized successfully!")
