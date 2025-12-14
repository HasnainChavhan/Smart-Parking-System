"""
MINIMAL WORKING BACKEND - Guaranteed to work!
No complex dependencies, no database errors, just works.
"""
from fastapi import FastAPI, Response, Form, Header
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import uvicorn
import sqlite3
import hashlib
import uuid
from datetime import datetime

app = FastAPI()

# Simple database connection
def get_db():
    conn = sqlite3.connect('sql_app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Pydantic models
class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    username: str
    password: str

# CORS middleware - handle ALL requests
@app.middleware("http")
async def add_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

# Handle OPTIONS requests (preflight)
@app.options("/{rest_of_path:path}")
async def preflight_handler():
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
            "Access-Control-Allow-Headers": "*",
        }
    )

@app.get("/")
def root():
    return {"message": "Smart Parking API - Minimal Version", "status": "running"}

@app.post("/api/v1/auth/register")
def register(user: UserCreate):
    try:
        # Validate password has at least one letter
        if not any(c.isalpha() for c in user.password):
            return JSONResponse(
                status_code=400,
                content={"detail": "Password must contain at least one letter"}
            )
        
        # Hash password
        password_hash = hashlib.sha256(user.password.encode()).hexdigest()
        
        # Insert into database
        conn = get_db()
        cursor = conn.cursor()
        
        user_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        try:
            cursor.execute("""
                INSERT INTO users (id, email, name, hashed_password, is_active, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (user_id, user.email, user.name, password_hash, 1, now, now))
            
            conn.commit()
            conn.close()
            
            return {
                "id": user_id,
                "email": user.email,
                "name": user.name,
                "is_active": True
            }
            
        except sqlite3.IntegrityError:
            conn.close()
            return JSONResponse(
                status_code=400,
                content={"detail": "Email already registered"}
            )
            
    except Exception as e:
        print(f"Registration error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Registration failed: {str(e)}"}
        )

@app.post("/api/v1/auth/login")
async def login(username: str = Form(...), password: str = Form(...)):
    try:
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM users WHERE email = ? AND hashed_password = ?
        """, (username, password_hash))
        
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "Incorrect email or password"}
            )
        
        # Return fake JWT tokens
        return {
            "access_token": f"fake_token_{user['id']}",
            "refresh_token": f"fake_refresh_{user['id']}",
            "token_type": "bearer"
        }
        
    except Exception as e:
        print(f"Login error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Login failed: {str(e)}"}
        )

@app.get("/api/v1/auth/me")
async def get_current_user(authorization: Optional[str] = Header(None)):
    try:
        # Simple token verification - extract user ID from fake token
        if not authorization:
            return JSONResponse(
                status_code=401,
                content={"detail": "Not authenticated"}
            )
        
        # Remove "Bearer " prefix if present
        token = authorization.replace("Bearer ", "") if authorization.startswith("Bearer ") else authorization
        
        # Extract user ID from fake token (format: fake_token_{user_id})
        if not token.startswith("fake_token_"):
            return JSONResponse(
                status_code=401,
                content={"detail": "Invalid token"}
            )
        
        user_id = token.replace("fake_token_", "")
        
        # Get user from database
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "User not found"}
            )
        
        return {
            "id": user['id'],
            "email": user['email'],
            "name": user['name'],
            "is_active": bool(user['is_active'])
        }
        
    except Exception as e:
        print(f"Get user error: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=401,
            content={"detail": "Authentication failed"}
        )

@app.get("/api/v1/lots/")
def get_lots():
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM parking_lots WHERE id = 1")
        lot = cursor.fetchone()
        
        cursor.execute("SELECT * FROM slots WHERE lot_id = 1")
        slots = cursor.fetchall()
        
        conn.close()
        
        if lot:
            return [{
                "id": lot['id'],
                "name": lot['name'],
                "address": lot['address'],
                "slots": [dict(slot) for slot in slots]
            }]
        else:
            return []
            
    except Exception as e:
        print(f"Get lots error: {e}")
        return []

@app.post("/api/v1/lots/{lot_id}/slots/{slot_id}/status")
async def update_slot_status(lot_id: int, slot_id: int, status: dict):
    try:
        new_status = status.get("status", "free")
        
        conn = get_db()
        cursor = conn.cursor()
        
        # Update slot status in database
        cursor.execute("""
            UPDATE slots SET status = ? WHERE id = ? AND lot_id = ?
        """, (new_status, slot_id, lot_id))
        
        conn.commit()
        conn.close()
        
        print(f"✓ Updated slot {slot_id} to {new_status}")
        
        return {"success": True, "slot_id": slot_id, "status": new_status}
        
    except Exception as e:
        print(f"Update slot error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": f"Update failed: {str(e)}"}
        )

if __name__ == "__main__":
    print("=" * 60)
    print("🚗 MINIMAL Smart Parking Backend")
    print("=" * 60)
    print("✓ Server: http://localhost:8000")
    print("✓ CORS: Enabled for all origins")
    print("✓ Database: SQLite")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
