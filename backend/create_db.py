"""
Initialize the database with all required tables
"""
from app.db.session import engine, Base
from app.db import models

print("Creating database tables...")

# Create all tables
Base.metadata.create_all(bind=engine)

print("✓ Database tables created successfully!")
print("\nTables created:")
print("  - users")
print("  - lots") 
print("  - slots")
print("  - bookings")
