from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import razorpay
from typing import Any

from app.core.config import settings
from app.db import models, session
from app.schemas import schemas

router = APIRouter()

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

@router.post("/", response_model=Any)
def create_booking_order(booking_request: schemas.BookingCreate, db: Session = Depends(session.get_db)):
    """
    1. Check if slot is free
    2. Create Razorpay Order
    3. Return Order ID to frontend
    """
    # Check slot availability
    slot = db.query(models.Slot).filter(models.Slot.id == booking_request.slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    
    # Simple check: In real app, check 'SlotStatus' or future bookings overlap
    # For now, just proceed.

    amount_paise = int(booking_request.duration_hours * slot.rate_per_hour * 100) # INR to Paise
    
    try:
        payment = client.order.create({
            "amount": amount_paise,
            "currency": "INR",
            "receipt": f"receipt_{booking_request.slot_id}",
            "payment_capture": 1
        })
    except Exception as e:
        print(f"Razorpay Error: {e}")
        raise HTTPException(status_code=500, detail="Payment Gateway Error")

    return {
        "order_id": payment['id'],
        "amount": payment['amount'],
        "currency": payment['currency'],
        "key_id": settings.RAZORPAY_KEY_ID
    }

@router.post("/verify")
def verify_payment(
    razorpay_order_id: str, 
    razorpay_payment_id: str, 
    razorpay_signature: str,
    slot_id: int,
    db: Session = Depends(session.get_db)
):
    """
    Verify signature and save booking
    """
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': razorpay_payment_id,
            'razorpay_signature': razorpay_signature
        })
    except razorpay.errors.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Payment Signature")

    # Create Booking Record
    booking = models.Booking(
        slot_id=slot_id,
        user_id="test_user", # Placeholder
        amount=100.0, # Placeholder, should match order
        status="paid",
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id
    )
    db.add(booking)
    db.commit()
    
    return {"status": "success", "message": "Booking Confirmed"}
