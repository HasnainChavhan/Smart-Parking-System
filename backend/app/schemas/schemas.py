from pydantic import BaseModel, EmailStr, Field, validator
from typing import List, Optional, Any
from datetime import datetime

# --- User & Authentication Schemas ---
class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    password: str = Field(..., min_length=8, description="Password (min 8 characters)")
    name: str = Field(..., min_length=2, description="User's full name")
    
    @validator('password')
    def validate_password(cls, v):
        if not any(char.isdigit() for char in v):
            raise ValueError('Password must contain at least one digit')
        if not any(char.isalpha() for char in v):
            raise ValueError('Password must contain at least one letter')
        return v


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


# --- Shared Properties ---
class ParkingLotBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Parking lot name")
    address: Optional[str] = Field(None, max_length=500, description="Physical address")
    geo_location: Optional[str] = Field(None, description="GPS coordinates or location string")


class SlotBase(BaseModel):
    name: str = Field(..., description="Slot identifier (e.g., A1, B2)")
    polygon: Optional[List[List[float]]] = Field(None, description="Polygon coordinates for slot area")
    slot_type: str = Field(default="regular", description="Slot type: regular, premium, ev")
    rate_per_hour: float = Field(default=10.0, ge=0, description="Hourly rate in currency")
    is_active: bool = Field(default=True, description="Whether slot is active")


class CameraBase(BaseModel):
    rtsp_url: str = Field(..., description="RTSP stream URL")
    position: Optional[str] = Field(None, description="Camera position description")


# --- Creation Schemas ---
class ParkingLotCreate(ParkingLotBase):
    pass


class SlotCreate(SlotBase):
    pass


class CameraCreate(CameraBase):
    pass


class BookingCreate(BaseModel):
    slot_id: int = Field(..., description="ID of the slot to book")
    duration_hours: int = Field(..., ge=1, le=24, description="Booking duration in hours (1-24)")


class InferenceResult(BaseModel):
    camera_id: int
    detections: List[dict] # {class, conf, box}


# --- Response Schemas ---
class Slot(SlotBase):
    id: int
    lot_id: int
    status: str = "free"  # Computed/Latest
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ParkingLot(ParkingLotBase):
    id: int
    slots: List[Slot] = []
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class Booking(BaseModel):
    id: int
    slot_id: int
    user_id: str
    start_time: datetime
    end_time: datetime
    amount: float
    status: str
    razorpay_order_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SlotStatusUpdate(BaseModel):
    status: str = Field(..., description="New status: free, occupied, reserved")
    
    @validator('status')
    def validate_status(cls, v):
        allowed_statuses = ['free', 'occupied', 'reserved']
        if v not in allowed_statuses:
            raise ValueError(f'Status must be one of: {", ".join(allowed_statuses)}')
        return v


# --- Pagination Schema ---
class PaginationMeta(BaseModel):
    total: int
    page: int
    page_size: int
    total_pages: int


# --- Error Response Schema ---
class ErrorResponse(BaseModel):
    detail: str
    status_code: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None

