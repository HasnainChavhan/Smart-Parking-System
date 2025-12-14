"""
Custom exception classes for better error handling and API responses.
"""

from typing import Any, Optional


class ParkingSystemException(Exception):
    """Base exception class for all parking system errors."""
    
    def __init__(
        self,
        message: str = "An error occurred",
        status_code: int = 500,
        details: Optional[Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class SlotNotFoundException(ParkingSystemException):
    """Raised when a parking slot is not found."""
    
    def __init__(self, slot_id: int, message: str = None):
        super().__init__(
            message=message or f"Parking slot with ID {slot_id} not found",
            status_code=404,
            details={"slot_id": slot_id}
        )


class SlotAlreadyBookedException(ParkingSystemException):
    """Raised when attempting to book an already occupied/reserved slot."""
    
    def __init__(self, slot_id: int, current_status: str, message: str = None):
        super().__init__(
            message=message or f"Slot {slot_id} is already {current_status}",
            status_code=409,
            details={"slot_id": slot_id, "current_status": current_status}
        )


class PaymentFailedException(ParkingSystemException):
    """Raised when payment processing fails."""
    
    def __init__(self, reason: str, message: str = None):
        super().__init__(
            message=message or f"Payment failed: {reason}",
            status_code=402,
            details={"reason": reason}
        )


class AuthenticationException(ParkingSystemException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=401,
            details=None
        )


class AuthorizationException(ParkingSystemException):
    """Raised when user doesn't have permission for an action."""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            status_code=403,
            details=None
        )


class ValidationException(ParkingSystemException):
    """Raised when input validation fails."""
    
    def __init__(self, field: str, message: str):
        super().__init__(
            message=f"Validation error for {field}: {message}",
            status_code=422,
            details={"field": field, "error": message}
        )


class LotNotFoundException(ParkingSystemException):
    """Raised when a parking lot is not found."""
    
    def __init__(self, lot_id: int, message: str = None):
        super().__init__(
            message=message or f"Parking lot with ID {lot_id} not found",
            status_code=404,
            details={"lot_id": lot_id}
        )


class BookingNotFoundException(ParkingSystemException):
    """Raised when a booking is not found."""
    
    def __init__(self, booking_id: int, message: str = None):
        super().__init__(
            message=message or f"Booking with ID {booking_id} not found",
            status_code=404,
            details={"booking_id": booking_id}
        )


class MLServiceException(ParkingSystemException):
    """Raised when ML service communication fails."""
    
    def __init__(self, message: str = "ML service unavailable"):
        super().__init__(
            message=message,
            status_code=503,
            details={"service": "ml_service"}
        )
