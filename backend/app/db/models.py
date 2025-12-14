from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True) # UUID from Supabase Auth or generated
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    hashed_password = Column(String, nullable=False)  # Added for authentication
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ParkingLot(Base):
    __tablename__ = "parking_lots"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    geo_location = Column(String) # Simple string for now, or JSON
    admin_id = Column(String, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    slots = relationship("Slot", back_populates="lot")
    cameras = relationship("Camera", back_populates="lot")

class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(Integer, ForeignKey("parking_lots.id"))
    name = Column(String) # e.g. "A1"
    polygon = Column(JSON) # List of points [[x,y], [x,y]...]
    slot_type = Column(String, default="regular") # regular, premium, ev
    rate_per_hour = Column(Float, default=10.0)
    is_active = Column(Boolean, default=True)
    status = Column(String, default="free") # Current status: free, occupied, reserved
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    lot = relationship("ParkingLot", back_populates="slots")
    status_history = relationship("SlotStatus", back_populates="slot")

class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True, index=True)
    lot_id = Column(Integer, ForeignKey("parking_lots.id"))
    rtsp_url = Column(String)
    position = Column(String)
    
    lot = relationship("ParkingLot", back_populates="cameras")

class SlotStatus(Base):
    __tablename__ = "slot_status"
    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"))
    status = Column(String) # free, occupied, reserved
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String) # ml, camera, manual
    
    slot = relationship("Slot", back_populates="status_history")

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    slot_id = Column(Integer, ForeignKey("slots.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    amount = Column(Float)
    status = Column(String, default="pending") # pending, paid, cancelled
    razorpay_order_id = Column(String)
    razorpay_payment_id = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User")
    slot = relationship("Slot")
