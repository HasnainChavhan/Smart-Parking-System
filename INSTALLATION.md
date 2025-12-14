# 📦 Smart Parking System - Installation Guide

## Quick Install

### Backend
```bash
cd backend
pip install -r requirements_minimal.txt
```

### ML Service
```bash
cd ml_service
pip install -r requirements.txt
```

## All Dependencies

### Backend (FastAPI)
- fastapi==0.104.1
- uvicorn==0.24.0
- pydantic==2.5.0
- python-multipart==0.0.6

### ML Service (YOLOv8)
- flask==3.0.0
- opencv-python==4.8.1.78
- ultralytics==8.0.220
- shapely==2.0.2
- requests==2.31.0
- numpy==1.24.3

## Installation Time
- Backend: ~1-2 minutes
- ML Service: ~5-10 minutes (first time, downloads YOLO model)

## Verify Installation
```bash
# Backend
python -c "import fastapi; print('FastAPI installed!')"

# ML Service
python -c "import cv2; print('OpenCV installed!')"
```
