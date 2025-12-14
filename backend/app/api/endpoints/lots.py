from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from app.db import models, session
from app.schemas import schemas
from app.api.endpoints.websockets import manager

router = APIRouter()

@router.get("/", response_model=List[schemas.ParkingLot])
def read_parking_lots(skip: int = 0, limit: int = 100, db: Session = Depends(session.get_db)):
    lots = db.query(models.ParkingLot).offset(skip).limit(limit).all()
    # print(f"DEBUG: Found {len(lots)} lots")
    return lots

@router.post("/", response_model=schemas.ParkingLot)
def create_parking_lot(lot: schemas.ParkingLotCreate, db: Session = Depends(session.get_db)):
    db_lot = models.ParkingLot(**lot.dict(), admin_id="test_admin")
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return db_lot

@router.post("/{lot_id}/slots", response_model=schemas.Slot)
def create_slot(lot_id: int, slot: schemas.SlotCreate, db: Session = Depends(session.get_db)):
    db_slot = models.Slot(**slot.dict(), lot_id=lot_id)
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.post("/{lot_id}/slots/{slot_id}/status", response_model=schemas.Slot)
async def update_slot_status(
    lot_id: int, 
    slot_id: int, 
    status_update: schemas.SlotStatusUpdate, 
    db: Session = Depends(session.get_db)
):
    slot = db.query(models.Slot).filter(models.Slot.id == slot_id, models.Slot.lot_id == lot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    current_status = slot.status

    # --- Priority Logic ---
    # 1. If Slot is 'reserved'
    if current_status == "reserved":
        # Only allow switching to 'occupied' (Car arrived)
        # Identify if ML is saying 'free' -> Ignore
        if status_update.status == "free":
            print(f"Ignored ML update 'free' for Reserved slot {slot_id}")
            return slot # Return current state without change

    slot.status = status_update.status
    db.commit()
    db.refresh(slot)

    # Broadcast to WS
    message = {
        "type": "slot_update",
        "slot": {
            "id": slot.id,
            "status": slot.status,
            "lot_id": lot_id
        }
    }
    await manager.broadcast(message, str(lot_id))
    
    return slot
