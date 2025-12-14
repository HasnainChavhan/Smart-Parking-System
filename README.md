# 🚗 Smart Car Parking System

A production-ready, AI-powered parking management system with real-time slot detection, booking capabilities, and payment integration.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![React](https://img.shields.io/badge/react-18.2+-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.109+-green.svg)

## ✨ Features

### 🔐 Authentication & Security
- JWT-based authentication with access and refresh tokens
- Secure password hashing with bcrypt
- Rate limiting to prevent API abuse
- CORS configuration for secure cross-origin requests

### 🎯 Real-time Parking Management
- AI-powered vehicle detection using YOLOv8
- Live CCTV feed with detection overlays
- WebSocket-based real-time slot updates
- Automatic status synchronization across all clients

### 💳 Booking & Payments
- Interactive booking interface
- Razorpay payment gateway integration
- Duration-based pricing calculation
- Booking history and management

### 📊 Dashboard & Analytics
- Real-time statistics (total, available, occupied, reserved slots)
- Professional glassmorphism UI design
- Responsive layout for all devices
- Toast notifications for user feedback

### 🛠️ Production-Ready Infrastructure
- Structured logging with file rotation
- Comprehensive error handling
- Health check endpoints
- Environment-based configuration
- Database migrations support

## 🏗️ Architecture

```
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│    Frontend     │◄────►│     Backend     │◄────►│   ML Service    │
│   (React +      │ HTTP │   (FastAPI)     │ HTTP │   (YOLOv8 +     │
│   Tailwind)     │  WS  │                 │      │    Flask)       │
│                 │      │                 │      │                 │
└─────────────────┘      └────────┬────────┘      └─────────────────┘
                                  │
                                  │
                         ┌────────▼────────┐
                         │                 │
                         │    Database     │
                         │   (SQLite/      │
                         │   PostgreSQL)   │
                         │                 │
                         └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration

# Run the server
python main.py
```

The backend API will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/v1/health

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

The frontend will be available at: http://localhost:5173

### ML Service Setup

```bash
cd ml_service

# Install dependencies (if not already installed)
pip install flask ultralytics opencv-python-headless shapely requests python-dotenv loguru

# Run the service
python inference.py
```

The ML service will be available at: http://localhost:5000

## 📁 Project Structure

```
parking-system/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth.py          # Authentication endpoints
│   │   │   │   ├── bookings.py      # Booking management
│   │   │   │   ├── health.py        # Health checks
│   │   │   │   ├── lots.py          # Parking lot management
│   │   │   │   └── websockets.py    # WebSocket connections
│   │   │   └── api.py               # API router
│   │   ├── core/
│   │   │   ├── config.py            # Configuration management
│   │   │   ├── security.py          # JWT & password handling
│   │   │   ├── logging_config.py    # Logging setup
│   │   │   ├── exceptions.py        # Custom exceptions
│   │   │   └── middleware.py        # Request/response middleware
│   │   ├── db/
│   │   │   ├── models.py            # Database models
│   │   │   └── session.py           # Database session
│   │   └── schemas/
│   │       └── schemas.py           # Pydantic schemas
│   ├── .env                         # Environment variables
│   ├── .env.example                 # Environment template
│   ├── main.py                      # Application entry point
│   └── requirements.txt             # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── config/
│   │   │   └── config.js            # API configuration
│   │   ├── store/
│   │   │   ├── authStore.js         # Authentication state
│   │   │   └── parkingStore.js      # Parking data state
│   │   ├── utils/
│   │   │   ├── api.js               # Axios client
│   │   │   └── helpers.js           # Utility functions
│   │   ├── App.jsx                  # Main application
│   │   ├── main.jsx                 # Entry point
│   │   └── index.css                # Global styles
│   ├── package.json                 # Node dependencies
│   ├── tailwind.config.js           # Tailwind configuration
│   └── vite.config.js               # Vite configuration
├── ml_service/
│   ├── inference.py                 # ML detection service
│   └── requirements.txt             # Python dependencies
└── README.md                        # This file
```

## 🔧 Configuration

### Backend Environment Variables

Create a `.env` file in the `backend` directory:

```env
# Application
PROJECT_NAME=Car Parking System
ENVIRONMENT=development
DEBUG=True
API_V1_STR=/api/v1

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=sqlite:///./sql_app.db

# Security
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# Razorpay
RAZORPAY_KEY_ID=your-razorpay-key-id
RAZORPAY_KEY_SECRET=your-razorpay-secret

# ML Service
ML_SERVICE_URL=http://localhost:5000

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Rate Limiting
RATE_LIMIT_PER_MINUTE=60
RATE_LIMIT_ENABLED=True
```

### Frontend Environment Variables

Create a `.env` file in the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_BASE_URL=ws://localhost:8000
VITE_ML_SERVICE_URL=http://localhost:5000
```

## 📚 API Documentation

### Authentication

#### Register
```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "name": "John Doe"
}
```

#### Login
```http
POST /api/v1/auth/login
Content-Type: multipart/form-data

username=user@example.com
password=SecurePass123
```

#### Get Current User
```http
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

### Parking Lots

#### Get All Lots
```http
GET /api/v1/lots
```

#### Update Slot Status
```http
POST /api/v1/lots/{lot_id}/slots/{slot_id}/status
Content-Type: application/json

{
  "status": "occupied"
}
```

### Bookings

#### Create Booking
```http
POST /api/v1/bookings
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "slot_id": 1,
  "duration_hours": 2
}
```

### WebSocket

#### Connect to Lot Updates
```javascript
const ws = new WebSocket('ws://localhost:8000/api/v1/ws/lot/1');

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'slot_update') {
    console.log('Slot updated:', data.slot);
  }
};
```

## 🎨 UI Features

- **Glassmorphism Design**: Modern frosted glass effect with backdrop blur
- **Gradient Backgrounds**: Vibrant color transitions
- **Real-time Indicators**: Live connection status with pulse animation
- **Interactive Slots**: Click-to-book with visual feedback
- **Toast Notifications**: User-friendly feedback for all actions
- **Responsive Layout**: Works seamlessly on mobile, tablet, and desktop
- **Professional Typography**: Google Fonts (Inter, Outfit)

## 🔒 Security Features

- JWT-based authentication with automatic token refresh
- Password hashing using bcrypt
- Rate limiting (60 requests/minute by default)
- CORS configuration
- Input validation with Pydantic
- SQL injection prevention with SQLAlchemy ORM
- XSS protection
- Environment-based secrets management

## 📊 Monitoring & Logging

- Structured logging with Loguru
- File rotation (10MB per file)
- Separate error logs
- Request ID tracking
- Performance monitoring
- Health check endpoints

## 🚢 Deployment

### Production Checklist

- [ ] Update environment variables in `.env`
- [ ] Change `SECRET_KEY` and `JWT_SECRET_KEY`
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=False`
- [ ] Use PostgreSQL instead of SQLite
- [ ] Configure proper CORS origins
- [ ] Set up SSL/TLS certificates
- [ ] Configure reverse proxy (nginx)
- [ ] Set up log aggregation
- [ ] Configure monitoring and alerting
- [ ] Set up automated backups

### Docker Deployment (Coming Soon)

Docker support will be added in the next update with:
- Multi-stage builds for optimization
- Docker Compose for easy orchestration
- Nginx reverse proxy
- PostgreSQL database
- Redis for caching

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest tests/ -v --cov=app

# Frontend tests
cd frontend
npm run test
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Your Name - Initial work

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React for the frontend library
- Ultralytics for YOLOv8
- Tailwind CSS for the styling framework
- Razorpay for payment integration

## 📞 Support

For support, email chavhanhasnain30@gmail.com or open an issue in the repository.

---

**Made with ❤️ for efficient parking management**
