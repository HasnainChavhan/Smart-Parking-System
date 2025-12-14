# 🚀 QUICK INSTALLATION - Smart Parking System

## ⚡ 5-Minute Setup

### 1. Install Python
- Download from: https://python.org
- ✅ CHECK "Add Python to PATH"

### 2. Setup Backend (Terminal 1)
```bash
cd parking-system/backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn pydantic python-multipart
python minimal_backend.py
```

### 3. Setup ML Service (Terminal 2)
```bash
cd parking-system/ml_service
pip install flask opencv-python ultralytics shapely requests
python inference_fast.py
```

### 4. Open Frontend
- Open `frontend/login.html` in Chrome/Firefox
- Register → Login → See Dashboard!

## ✅ Success Checklist
- [ ] Backend shows: "Uvicorn running on http://0.0.0.0:8000"
- [ ] ML shows: "AUTO-DETECTED 3 PARKING SLOTS!"
- [ ] Dashboard shows live video with colored boxes
- [ ] Slots update automatically

## 🐛 Quick Fixes
- **Network error**: Backend not running → Run Step 2
- **No video**: ML service not running → Run Step 3
- **Module not found**: Activate venv → See `(venv)` in terminal

## 📚 Full Guide
See `JUNIOR_INSTALLATION_GUIDE.txt` for detailed instructions!
