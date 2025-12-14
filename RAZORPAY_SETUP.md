# 🔐 Razorpay Integration Setup Guide

## Step 1: Get Razorpay Credentials

### Create Razorpay Account
1. Go to https://razorpay.com/
2. Click "Sign Up" (free account)
3. Complete registration
4. Verify your email

### Get API Keys
1. Login to Razorpay Dashboard
2. Go to **Settings** → **API Keys**
3. Click "Generate Test Key" (for testing)
4. Copy:
   - **Key ID** (starts with `rzp_test_`)
   - **Key Secret** (keep this secret!)

## Step 2: Configure Backend

### Update `.env` file:
```env
# Razorpay Configuration
RAZORPAY_KEY_ID=rzp_test_YOUR_KEY_ID_HERE
RAZORPAY_KEY_SECRET=YOUR_KEY_SECRET_HERE

# JWT Configuration (already set)
JWT_SECRET_KEY=your-secret-key-keep-it-secret
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database (already set)
DATABASE_URL=sqlite:///./sql_app.db
```

### Example:
```env
RAZORPAY_KEY_ID=rzp_test_1234567890abcd
RAZORPAY_KEY_SECRET=abcdefghijklmnopqrstuvwxyz123456
JWT_SECRET_KEY=my-super-secret-jwt-key-change-this-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Step 3: Restart Backend

```powershell
# Stop current backend (Ctrl+C)
cd backend
python main.py
```

## Step 4: Test the Complete System

### 1. Open the Complete UI
```
file:///c:/Users/91932/Downloads/Car_Parking%20System/parking-system/frontend/index_complete.html
```

### 2. Test Registration
- Click "Register" button
- Fill in:
  - Name: Test User
  - Email: test@example.com
  - Password: password123
- Click "Register"
- Should see success message

### 3. Test Login
- Click "Login" button
- Enter:
  - Email: test@example.com
  - Password: password123
- Click "Login"
- Should see your name in header

### 4. Test Booking
- Click on any **GREEN (FREE)** parking slot
- Select duration (e.g., 2 hours)
- Click "Pay with Razorpay"
- Razorpay payment window opens
- **Test Mode Payment:**
  - Card Number: `4111 1111 1111 1111`
  - Expiry: Any future date (e.g., `12/25`)
  - CVV: Any 3 digits (e.g., `123`)
  - Name: Any name
- Click "Pay"
- Should see booking confirmation!

## Step 5: Verify Everything Works

### Check Backend Logs
You should see:
```
New user registered: test@example.com
User logged in: test@example.com
Booking created for slot X
Payment verified successfully
```

### Check Frontend
- User name appears in header
- Slot status updates in real-time
- Payment confirmation message shows
- Slot might change to OCCUPIED (if ML detects car)

## Complete Flow Diagram

```
1. User Registration
   ↓
2. User Login (get JWT token)
   ↓
3. View Available Slots (live feed + list)
   ↓
4. Select Slot + Duration
   ↓
5. Create Booking Order (backend)
   ↓
6. Open Razorpay Payment Gateway
   ↓
7. User Pays
   ↓
8. Verify Payment (backend)
   ↓
9. Confirm Booking ✅
   ↓
10. Update Slot Status
```

## Features Implemented

### ✅ Authentication
- User registration with validation
- Secure login with JWT tokens
- Token storage in localStorage
- Auto-login on page refresh
- Logout functionality

### ✅ Payment Integration
- Razorpay order creation
- Secure payment gateway
- Payment verification
- Error handling

### ✅ Booking System
- Slot selection
- Duration picker (1-24 hours)
- Price calculation
- Booking confirmation
- Real-time updates

### ✅ UI/UX
- Professional glassmorphism design
- Responsive modals
- Loading states
- Success/error notifications
- Real-time WebSocket updates
- Live ML detection feed

## Troubleshooting

### "Payment Gateway Error"
- Check if Razorpay keys are set in `.env`
- Restart backend after updating `.env`
- Verify keys are correct (no extra spaces)

### "Login failed"
- Check if backend is running on port 8000
- Verify email/password are correct
- Check browser console for errors

### "Slot not updating"
- Check if ML service is running on port 5000
- Verify WebSocket connection (green dot)
- Check backend logs for errors

### "Cannot book slot"
- Make sure you're logged in
- Select a FREE (green) slot only
- Check if backend is running

## Test Mode vs Production

### Test Mode (Current Setup)
- Use test API keys (`rzp_test_...`)
- Test card numbers work
- No real money charged
- Perfect for development

### Production Mode
1. Complete KYC on Razorpay
2. Get live API keys (`rzp_live_...`)
3. Update `.env` with live keys
4. Real payments will be processed
5. Requires SSL/HTTPS

## Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` file to Git
- Keep `RAZORPAY_KEY_SECRET` private
- Use strong `JWT_SECRET_KEY`
- Enable HTTPS in production
- Implement rate limiting
- Add CAPTCHA for registration

## Next Steps

1. ✅ Test complete registration flow
2. ✅ Test login and authentication
3. ✅ Test booking with Razorpay
4. ✅ Verify payment confirmation
5. 📝 Add booking history view
6. 📝 Add booking cancellation
7. 📝 Deploy to production server

---

**Your Smart Parking System is now complete with:**
- 🔐 Full authentication
- 💳 Razorpay payment integration
- 🅿️ Real-time parking detection
- 📱 Professional UI
- ⚡ Fast performance
- 🆓 100% FREE (except Razorpay transaction fees)

**Ready to use! 🚀**
