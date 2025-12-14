# 🚀 Quick Setup Guide for Juniors

## 📦 What You'll Receive

A complete Smart Parking System with:
- ✅ Backend API (FastAPI)
- ✅ ML Detection Service (YOLOv8)
- ✅ Frontend Dashboard (HTML/React)
- ✅ Database (SQLite - pre-configured)
- ✅ Sample video for testing

---

## ⚡ Quick Start (5 Minutes)

### Step 1: Install Python
1. Download Python 3.8+ from [python.org](https://python.org)
2. During installation, **CHECK** "Add Python to PATH"
3. Verify: Open CMD/Terminal and type `python --version`

### Step 2: Setup Backend

```bash
# Open terminal in project folder
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
.\venv\Scripts\Activate.ps1
# Mac/Linux:
source venv/bin/activate

# Install packages (takes 2-3 minutes)
pip install fastapi uvicorn pydantic python-multipart

# Run backend
python minimal_backend.py
```

**You should see:**
```
🚗 MINIMAL Smart Parking Backend
✓ Server: http://localhost:8000
```

### Step 3: Setup ML Service (New Terminal)

```bash
# Open NEW terminal in project folder
cd ml_service

# Install packages (takes 5-10 minutes first time)
pip install flask opencv-python ultralytics shapely requests

# Run ML service
python inference_fast.py
```

**You should see:**
```
⚡ FAST AUTO-DETECT PARKING SYSTEM
✅ AUTO-DETECTED 3 PARKING SLOTS!
🔄 Starting detection...
```

### Step 4: Open Frontend

1. Navigate to `frontend` folder
2. Right-click `login.html`
3. Open with Chrome/Firefox
4. Register a new account
5. Login and see the dashboard!

---

## 📁 Project Structure

```
parking-system/
├── backend/
│   ├── minimal_backend.py    ← Main backend server
│   ├── sql_app.db            ← Database (pre-configured)
│   ├── fix_users_table.py    ← Database setup script
│   └── venv/                 ← Virtual environment (create this)
│
├── ml_service/
│   ├── inference_fast.py     ← ML detection service
│   └── yolov8n.pt           ← AI model (auto-downloads)
│
├── frontend/
│   ├── login.html           ← Login page (OPEN THIS FIRST)
│   ├── dashboard.html       ← Main dashboard
│   └── videoplayback.mp4    ← Sample parking video
│
└── TEACHING_GUIDE.md        ← Complete documentation
```

---

## 🎯 What Each Service Does

### Backend (Port 8000)
- Handles user login/registration
- Stores parking slot data
- Receives updates from ML service
- Provides API for frontend

### ML Service (Port 5000)
- Detects cars in video using AI
- Auto-creates parking slot boxes (A1, A2, A3)
- Sends status updates to backend
- Streams live video feed

### Frontend (Browser)
- Login/Register interface
- Live video feed display
- Real-time parking slot status
- Booking functionality

---

## ✅ Testing the System

### 1. Test Backend
Open browser: `http://localhost:8000/docs`
- You should see FastAPI documentation

### 2. Test ML Service
Open browser: `http://localhost:5000/video_feed`
- You should see live video with colored boxes

### 3. Test Frontend
1. Open `login.html` in browser
2. Register: Name: "Test User", Email: "test@test.com", Password: "test1234"
3. Login with same credentials
4. You should see dashboard with:
   - Live video feed
   - Parking slots (A1, A2, A3)
   - Green = Available, Red = Occupied

---

## 🐛 Common Issues

### Issue: "python: command not found"
**Fix:** Install Python and add to PATH

### Issue: "pip: command not found"
**Fix:** Use `python -m pip install` instead of `pip install`

### Issue: "Cannot activate virtual environment"
**Fix (Windows):** Run PowerShell as Administrator, then:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: "Port 8000 already in use"
**Fix:** 
```bash
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux:
lsof -ti:8000 | xargs kill -9
```

### Issue: "Module not found"
**Fix:** Make sure virtual environment is activated (you should see `(venv)` in terminal)

### Issue: Slots not updating
**Fix:** 
1. Refresh dashboard page (F5)
2. Check both backend and ML service are running
3. Look for "✓ Updated slot X to occupied" in backend logs

---

## 📚 Learning Path

### Day 1: Understand the System
- Read `TEACHING_GUIDE.md`
- Run the system and test all features
- Watch how slots update in real-time

### Day 2: Explore Backend
- Open `minimal_backend.py`
- Understand each endpoint
- Try adding a new endpoint

### Day 3: Explore ML Service
- Open `inference_fast.py`
- Understand auto-detection algorithm
- Try changing number of slots

### Day 4: Explore Frontend
- Open `login.html` and `dashboard.html`
- Understand authentication flow
- Try adding a new feature

### Day 5: Modify & Extend
- Add phone number to registration
- Change slot colors
- Add booking history page

---

## 🎓 Exercises for Practice

### Beginner
1. Change the parking lot name from "Main Parking Lot" to your college name
2. Modify slot rate from ₹50/hour to ₹100/hour
3. Add a footer to the dashboard

### Intermediate
1. Add a "Forgot Password" feature
2. Create an admin page to view all users
3. Add email validation during registration

### Advanced
1. Implement WebSocket for real-time updates (no page refresh)
2. Add booking history for users
3. Create analytics dashboard showing usage statistics

---

## 📞 Support

If you get stuck:
1. Check `TEACHING_GUIDE.md` - Common Issues section
2. Read error messages carefully
3. Google the error message
4. Ask your instructor

---

## 🎉 Success Checklist

- [ ] Python installed and in PATH
- [ ] Backend running on port 8000
- [ ] ML service running on port 5000
- [ ] Can open login page in browser
- [ ] Can register a new account
- [ ] Can login successfully
- [ ] Dashboard shows live video feed
- [ ] Parking slots (A1, A2, A3) are visible
- [ ] Slots change color (green/red) based on video
- [ ] Can click "Book Now" on available slots

---

## 💡 Tips for Success

1. **Always activate virtual environment** before running Python commands
2. **Keep both terminals open** - one for backend, one for ML service
3. **Check logs** - they show what's happening
4. **Start simple** - get it running first, then modify
5. **Read the code** - it's well-commented
6. **Experiment** - try changing values and see what happens
7. **Ask questions** - no question is too simple

---

## 🚀 Next Steps After Setup

1. **Understand the flow:**
   - User registers → Backend saves to database
   - User logs in → Backend returns token
   - Dashboard loads → Fetches slots from backend
   - ML detects car → Sends update to backend
   - Backend updates database → Dashboard shows new status

2. **Explore the code:**
   - Start with `minimal_backend.py` (simplest)
   - Then `inference_fast.py` (ML logic)
   - Finally `dashboard.html` (React components)

3. **Make it yours:**
   - Change colors and styling
   - Add new features
   - Improve the UI
   - Add more parking lots

---

## 📖 Additional Resources

- **FastAPI Tutorial:** https://fastapi.tiangolo.com/tutorial/
- **YOLOv8 Docs:** https://docs.ultralytics.com/
- **React Tutorial:** https://react.dev/learn
- **Python Basics:** https://www.python.org/about/gettingstarted/

---

**Remember:** This is a learning project. Don't worry about breaking things - that's how you learn! Experiment, make mistakes, and have fun! 🎓

---

*Setup time: ~15 minutes | Difficulty: Beginner-friendly*
