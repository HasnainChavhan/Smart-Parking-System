"""
Seed the database with initial parking lot and slots
"""
import sys
sys.path.insert(0, '.')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import uuid

# Create engine
engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Import models
from app.db.models import Lot, Slot

db = SessionLocal()

try:
    # Check if lot already exists
    existing_lot = db.query(Lot).filter(Lot.id == 1).first()
    
    if not existing_lot:
        print("Creating parking lot...")
        
        # Create parking lot
        lot = Lot(
            id=1,
            name="Main Parking Lot",
            location="Building A",
            total_slots=3,
            lot_type="outdoor"
        )
        db.add(lot)
        db.commit()
        
        # Create 3 parking slots
        for i in range(1, 4):
            slot = Slot(
                id=i,
                lot_id=1,
                name=f"A{i}",
                status="free",
                rate_per_hour=50
            )
            db.add(slot)
        
        db.commit()
        print("✓ Created 1 parking lot with 3 slots (A1, A2, A3)")
    else:
        print("✓ Parking lot already exists")
        
        # Check slots
        slots = db.query(Slot).filter(Slot.lot_id == 1).all()
        print(f"✓ Found {len(slots)} parking slots")
        
except Exception as e:
    print(f"Error: {e}")
    db.rollback()
finally:
    db.close()

print("\n✓ Database seeded successfully!")
