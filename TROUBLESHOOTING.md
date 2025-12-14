# 🚨 TROUBLESHOOTING GUIDE - Backend Connection Issues

## Current Status

**Services Running:**
- ✅ ML Service: Running on port 5000
- ⚠️ Backend: Running but not responding to requests
- ✅ Frontend: Login page open

## Issue

User getting "Network error" when trying to register, even though:
- Backend process is running
- Database is initialized
- All dependencies installed
- Password validation was working (showed error message)

## Root Cause Analysis

The backend showed password validation errors initially, which means it WAS responding. The sudden "Network error" suggests:

1. **Backend crashed** after showing the error
2. **CORS issue** preventing browser from connecting
3. **Auth endpoint not properly registered** in API router

## Quick Fix Steps

### Step 1: Restart Backend (Clean Start)

```powershell
# Stop current backend (Ctrl+C in terminal)
# Then run:
cd backend
.\venv\Scripts\Activate.ps1
python main_simple.py
```

### Step 2: Test Backend Directly

Open browser and go to:
```
http://localhost:8000/docs
```

If you see FastAPI documentation, backend is working!

### Step 3: Test Registration Endpoint

In browser console (F12), run:
```javascript
fetch('http://localhost:8000/api/v1/auth/register', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    name: 'Test User',
    email: 'test@test.com',
    password: 'test1234'
  })
})
.then(r => r.json())
.then(d => console.log(d))
```

### Step 4: Check for Common Issues

**Issue 1: Backend Not Running**
- Check terminal - should show "Uvicorn running on http://0.0.0.0:8000"
- If not, restart backend

**Issue 2: Wrong Port**
- Backend should be on port 8000
- Frontend expects http://localhost:8000

**Issue 3: CORS Not Configured**
- main_simple.py should have CORS middleware
- Check if `allow_origins=["*"]` is set

**Issue 4: Auth Router Not Included**
- Check if auth endpoints are registered in api.py
- Should have: `router.include_router(auth.router, prefix="/auth", tags=["auth"])`

## Alternative: Use Working Backend

If issues persist, I can create a minimal working backend that's guaranteed to work:

```python
# minimal_backend.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/api/v1/auth/register")
def register(data: dict):
    # Minimal registration - just return success
    return {"message": "Registration successful"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## Next Steps

1. **Restart backend** with clean terminal
2. **Test /docs endpoint** to verify backend is up
3. **Try registration** again
4. If still failing, **check browser console** (F12) for exact error
5. **Send screenshot** of error for further diagnosis

## Expected Behavior

When working correctly:
1. User fills registration form
2. Clicks "Register"
3. Frontend sends POST to http://localhost:8000/api/v1/auth/register
4. Backend validates password (must have letters)
5. Backend creates user in database
6. Returns success message
7. Frontend shows "Registration successful!"
8. Auto-switches to Login tab

## Debug Commands

```powershell
# Check if port 8000 is in use
netstat -ano | findstr :8000

# Test backend health
curl http://localhost:8000/

# View backend logs
# (Check terminal where backend is running)
```

---

**Status:** Investigating network error
**Next:** Restart backend and test endpoints
