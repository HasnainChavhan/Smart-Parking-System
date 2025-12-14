import { useState, useEffect, useCallback } from 'react';
import { Toaster, toast } from 'react-hot-toast';
import { Car, Video, RefreshCw, LogOut, User, Clock, DollarSign, CheckCircle, XCircle, AlertCircle } from 'lucide-react';
import useAuthStore from './store/authStore';
import useParkingStore from './store/parkingStore';
import apiClient from './utils/api';
import { ENDPOINTS, WS_V1, ML_SERVICE_URL } from './config/config';
import { formatDateTime, getStatusBadgeClass, handleApiError, cn } from './utils/helpers';

function App() {
    const { user, isAuthenticated, setAuth, clearAuth } = useAuthStore();
    const { lots, currentLot, slots, setLots, setCurrentLot, updateSlotStatus, selectedSlot, setSelectedSlot, clearSelectedSlot } = useParkingStore();

    const [isLoading, setIsLoading] = useState(true);
    const [showAuthModal, setShowAuthModal] = useState(false);
    const [authMode, setAuthMode] = useState('login'); // 'login' or 'register'
    const [showBookingModal, setShowBookingModal] = useState(false);
    const [wsConnected, setWsConnected] = useState(false);
    const [ws, setWs] = useState(null);

    // Auth form state
    const [authForm, setAuthForm] = useState({
        email: '',
        password: '',
        name: '',
    });

    // Booking form state
    const [bookingForm, setBookingForm] = useState({
        duration_hours: 1,
    });

    // Fetch parking lots
    const fetchLots = useCallback(async () => {
        try {
            setIsLoading(true);
            const response = await apiClient.get(ENDPOINTS.LOTS);
            setLots(response.data);

            if (response.data.length > 0) {
                setCurrentLot(response.data[0]);
            }

            toast.success('Parking data loaded');
        } catch (error) {
            toast.error(handleApiError(error));
        } finally {
            setIsLoading(false);
        }
    }, [setLots, setCurrentLot]);

    // WebSocket connection
    useEffect(() => {
        if (!currentLot) return;

        const lotId = currentLot.id;
        const websocket = new WebSocket(`${WS_V1}/ws/lot/${lotId}`);

        websocket.onopen = () => {
            console.log('WebSocket connected');
            setWsConnected(true);
            toast.success('Live updates connected', { icon: '🔴', duration: 2000 });
        };

        websocket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.type === 'slot_update') {
                updateSlotStatus(data.slot.id, data.slot.status);
                toast(`Slot ${data.slot.id} is now ${data.slot.status}`, {
                    icon: data.slot.status === 'free' ? '✅' : '🚗',
                    duration: 3000,
                });
            }
        };

        websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
            setWsConnected(false);
            toast.error('Live updates disconnected');
        };

        websocket.onclose = () => {
            console.log('WebSocket closed');
            setWsConnected(false);

            // Attempt to reconnect after 5 seconds
            setTimeout(() => {
                console.log('Attempting to reconnect WebSocket...');
                fetchLots();
            }, 5000);
        };

        setWs(websocket);

        return () => {
            websocket.close();
        };
    }, [currentLot, updateSlotStatus, fetchLots]);

    // Initial data fetch
    useEffect(() => {
        fetchLots();
    }, [fetchLots]);

    // Handle login
    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const formData = new FormData();
            formData.append('username', authForm.email);
            formData.append('password', authForm.password);

            const response = await apiClient.post(ENDPOINTS.LOGIN, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });

            const { access_token, refresh_token } = response.data;

            // Fetch user data
            const userResponse = await apiClient.get(ENDPOINTS.ME, {
                headers: { Authorization: `Bearer ${access_token}` },
            });

            setAuth(userResponse.data, access_token, refresh_token);
            setShowAuthModal(false);
            setAuthForm({ email: '', password: '', name: '' });
            toast.success(`Welcome back, ${userResponse.data.name}!`);
        } catch (error) {
            toast.error(handleApiError(error));
        }
    };

    // Handle register
    const handleRegister = async (e) => {
        e.preventDefault();

        try {
            const response = await apiClient.post(ENDPOINTS.REGISTER, {
                email: authForm.email,
                password: authForm.password,
                name: authForm.name,
            });

            toast.success('Registration successful! Please login.');
            setAuthMode('login');
            setAuthForm({ ...authForm, password: '' });
        } catch (error) {
            toast.error(handleApiError(error));
        }
    };

    // Handle logout
    const handleLogout = () => {
        clearAuth();
        toast.success('Logged out successfully');
    };

    // Handle booking
    const handleBooking = async (e) => {
        e.preventDefault();

        if (!isAuthenticated) {
            toast.error('Please login to book a slot');
            setShowAuthModal(true);
            return;
        }

        if (!selectedSlot) return;

        try {
            const response = await apiClient.post(ENDPOINTS.BOOKINGS, {
                slot_id: selectedSlot.id,
                duration_hours: bookingForm.duration_hours,
            });

            const { order_id, amount, currency, key_id } = response.data;

            // Initialize Razorpay (in production, load Razorpay script)
            toast.success(`Booking initiated! Amount: ₹${amount / 100}`);
            toast.info('Payment integration ready (Razorpay)');

            setShowBookingModal(false);
            clearSelectedSlot();
            setBookingForm({ duration_hours: 1 });
        } catch (error) {
            toast.error(handleApiError(error));
        }
    };

    // Get slot statistics
    const slotStats = {
        total: slots.length,
        free: slots.filter(s => s.status === 'free').length,
        occupied: slots.filter(s => s.status === 'occupied').length,
        reserved: slots.filter(s => s.status === 'reserved').length,
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
            <Toaster position="top-right" />

            {/* Header */}
            <header className="glass-card sticky top-0 z-50 mb-8">
                <div className="container mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                            <div className="p-2 bg-gradient-to-br from-primary-500 to-purple-600 rounded-xl">
                                <Car className="w-8 h-8 text-white" />
                            </div>
                            <div>
                                <h1 className="text-2xl font-bold text-gradient">Smart Parking System</h1>
                                <p className="text-sm text-slate-600">Real-time Slot Management</p>
                            </div>
                        </div>

                        <div className="flex items-center space-x-4">
                            {/* Live Status Indicator */}
                            <div className="flex items-center space-x-2 px-4 py-2 bg-white/50 rounded-lg">
                                <div className={cn("pulse-dot", wsConnected ? "pulse-dot-success" : "pulse-dot-danger")}></div>
                                <span className="text-sm font-medium text-slate-700">
                                    {wsConnected ? 'Live' : 'Offline'}
                                </span>
                            </div>

                            {/* Refresh Button */}
                            <button
                                onClick={fetchLots}
                                className="p-2 hover:bg-white/50 rounded-lg transition-colors"
                                title="Refresh data"
                            >
                                <RefreshCw className="w-5 h-5 text-slate-700" />
                            </button>

                            {/* Auth Button */}
                            {isAuthenticated ? (
                                <div className="flex items-center space-x-3">
                                    <div className="flex items-center space-x-2 px-4 py-2 bg-white/50 rounded-lg">
                                        <User className="w-4 h-4 text-primary-600" />
                                        <span className="text-sm font-medium text-slate-700">{user?.name}</span>
                                    </div>
                                    <button
                                        onClick={handleLogout}
                                        className="p-2 hover:bg-red-50 rounded-lg transition-colors"
                                        title="Logout"
                                    >
                                        <LogOut className="w-5 h-5 text-red-600" />
                                    </button>
                                </div>
                            ) : (
                                <button
                                    onClick={() => setShowAuthModal(true)}
                                    className="btn-primary"
                                >
                                    Login
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="container mx-auto px-6 pb-12">
                {isLoading ? (
                    <div className="flex items-center justify-center h-64">
                        <div className="spinner text-primary-600"></div>
                        <span className="ml-3 text-slate-600">Loading parking data...</span>
                    </div>
                ) : (
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                        {/* Left Column - Parking Slots */}
                        <div className="lg:col-span-2 space-y-6">
                            {/* Statistics Cards */}
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div className="glass-card p-4 card-hover">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <p className="text-sm text-slate-600">Total Slots</p>
                                            <p className="text-2xl font-bold text-slate-800">{slotStats.total}</p>
                                        </div>
                                        <Car className="w-8 h-8 text-primary-500" />
                                    </div>
                                </div>

                                <div className="glass-card p-4 card-hover">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <p className="text-sm text-slate-600">Available</p>
                                            <p className="text-2xl font-bold text-success-600">{slotStats.free}</p>
                                        </div>
                                        <CheckCircle className="w-8 h-8 text-success-500" />
                                    </div>
                                </div>

                                <div className="glass-card p-4 card-hover">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <p className="text-sm text-slate-600">Occupied</p>
                                            <p className="text-2xl font-bold text-danger-600">{slotStats.occupied}</p>
                                        </div>
                                        <XCircle className="w-8 h-8 text-danger-500" />
                                    </div>
                                </div>

                                <div className="glass-card p-4 card-hover">
                                    <div className="flex items-center justify-between">
                                        <div>
                                            <p className="text-sm text-slate-600">Reserved</p>
                                            <p className="text-2xl font-bold text-warning-600">{slotStats.reserved}</p>
                                        </div>
                                        <AlertCircle className="w-8 h-8 text-warning-500" />
                                    </div>
                                </div>
                            </div>

                            {/* Parking Slots Grid */}
                            <div className="glass-card p-6">
                                <h2 className="text-xl font-bold text-slate-800 mb-4">Parking Slots</h2>

                                {slots.length === 0 ? (
                                    <p className="text-center text-slate-500 py-8">No slots available</p>
                                ) : (
                                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                                        {slots.map((slot) => (
                                            <div
                                                key={slot.id}
                                                onClick={() => {
                                                    if (slot.status === 'free') {
                                                        setSelectedSlot(slot);
                                                        setShowBookingModal(true);
                                                    }
                                                }}
                                                className={cn(
                                                    "p-6 border-2 rounded-xl transition-all duration-300 cursor-pointer",
                                                    slot.status === 'free' && "bg-success-50 border-success-300 hover:shadow-lg hover:scale-105",
                                                    slot.status === 'occupied' && "bg-danger-50 border-danger-300 cursor-not-allowed opacity-75",
                                                    slot.status === 'reserved' && "bg-warning-50 border-warning-300 cursor-not-allowed opacity-75"
                                                )}
                                            >
                                                <div className="flex items-center justify-between mb-3">
                                                    <h3 className="text-2xl font-bold text-slate-800">{slot.name}</h3>
                                                    <Car className={cn(
                                                        "w-6 h-6",
                                                        slot.status === 'free' && "text-success-600",
                                                        slot.status === 'occupied' && "text-danger-600",
                                                        slot.status === 'reserved' && "text-warning-600"
                                                    )} />
                                                </div>

                                                <div className="space-y-2">
                                                    <span className={getStatusBadgeClass(slot.status)}>
                                                        {slot.status.toUpperCase()}
                                                    </span>

                                                    <div className="flex items-center text-sm text-slate-600">
                                                        <DollarSign className="w-4 h-4 mr-1" />
                                                        <span>₹{slot.rate_per_hour}/hr</span>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Right Column - CCTV Feed */}
                        <div className="space-y-6">
                            <div className="glass-card p-6">
                                <div className="flex items-center justify-between mb-4">
                                    <h2 className="text-xl font-bold text-slate-800">Live CCTV Feed</h2>
                                    <Video className="w-6 h-6 text-primary-600" />
                                </div>

                                <div className="relative rounded-lg overflow-hidden bg-slate-900 aspect-video">
                                    <img
                                        src={`${ML_SERVICE_URL}/video_feed`}
                                        alt="Live CCTV Feed"
                                        className="w-full h-full object-cover"
                                        onError={(e) => {
                                            e.target.src = 'data:image/svg+xml,%3Csvg xmlns="http://www.w3.org/2000/svg" width="400" height="300"%3E%3Crect fill="%23334155" width="400" height="300"/%3E%3Ctext fill="%23fff" x="50%25" y="50%25" text-anchor="middle" dy=".3em"%3ECamera Offline%3C/text%3E%3C/svg%3E';
                                        }}
                                    />
                                    <div className="absolute top-2 left-2 px-3 py-1 bg-red-600 text-white text-xs font-semibold rounded-full flex items-center space-x-1">
                                        <div className="w-2 h-2 bg-white rounded-full animate-pulse"></div>
                                        <span>LIVE</span>
                                    </div>
                                </div>

                                <p className="text-sm text-slate-600 mt-3">
                                    Real-time AI-powered parking detection
                                </p>
                            </div>

                            {/* Info Card */}
                            <div className="glass-card p-6">
                                <h3 className="font-bold text-slate-800 mb-3">How it works</h3>
                                <ul className="space-y-2 text-sm text-slate-600">
                                    <li className="flex items-start">
                                        <CheckCircle className="w-4 h-4 text-success-500 mr-2 mt-0.5 flex-shrink-0" />
                                        <span>AI detects vehicle presence in real-time</span>
                                    </li>
                                    <li className="flex items-start">
                                        <CheckCircle className="w-4 h-4 text-success-500 mr-2 mt-0.5 flex-shrink-0" />
                                        <span>Slot status updates automatically</span>
                                    </li>
                                    <li className="flex items-start">
                                        <CheckCircle className="w-4 h-4 text-success-500 mr-2 mt-0.5 flex-shrink-0" />
                                        <span>Book available slots instantly</span>
                                    </li>
                                    <li className="flex items-start">
                                        <CheckCircle className="w-4 h-4 text-success-500 mr-2 mt-0.5 flex-shrink-0" />
                                        <span>Secure payment with Razorpay</span>
                                    </li>
                                </ul>
                            </div>
                        </div>
                    </div>
                )}
            </main>

            {/* Auth Modal */}
            {showAuthModal && (
                <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="glass-card p-8 max-w-md w-full animate-slide-up">
                        <h2 className="text-2xl font-bold text-slate-800 mb-6">
                            {authMode === 'login' ? 'Welcome Back' : 'Create Account'}
                        </h2>

                        <form onSubmit={authMode === 'login' ? handleLogin : handleRegister} className="space-y-4">
                            {authMode === 'register' && (
                                <div>
                                    <label className="block text-sm font-medium text-slate-700 mb-2">Name</label>
                                    <input
                                        type="text"
                                        value={authForm.name}
                                        onChange={(e) => setAuthForm({ ...authForm, name: e.target.value })}
                                        className="input-field"
                                        required
                                    />
                                </div>
                            )}

                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-2">Email</label>
                                <input
                                    type="email"
                                    value={authForm.email}
                                    onChange={(e) => setAuthForm({ ...authForm, email: e.target.value })}
                                    className="input-field"
                                    required
                                />
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-2">Password</label>
                                <input
                                    type="password"
                                    value={authForm.password}
                                    onChange={(e) => setAuthForm({ ...authForm, password: e.target.value })}
                                    className="input-field"
                                    required
                                    minLength={8}
                                />
                            </div>

                            <div className="flex space-x-3">
                                <button type="submit" className="btn-primary flex-1">
                                    {authMode === 'login' ? 'Login' : 'Register'}
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setShowAuthModal(false)}
                                    className="btn-secondary flex-1"
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>

                        <p className="text-center text-sm text-slate-600 mt-4">
                            {authMode === 'login' ? "Don't have an account? " : "Already have an account? "}
                            <button
                                onClick={() => setAuthMode(authMode === 'login' ? 'register' : 'login')}
                                className="text-primary-600 font-semibold hover:underline"
                            >
                                {authMode === 'login' ? 'Register' : 'Login'}
                            </button>
                        </p>
                    </div>
                </div>
            )}

            {/* Booking Modal */}
            {showBookingModal && selectedSlot && (
                <div className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4">
                    <div className="glass-card p-8 max-w-md w-full animate-slide-up">
                        <h2 className="text-2xl font-bold text-slate-800 mb-6">Book Slot {selectedSlot.name}</h2>

                        <form onSubmit={handleBooking} className="space-y-4">
                            <div className="bg-slate-50 p-4 rounded-lg space-y-2">
                                <div className="flex justify-between text-sm">
                                    <span className="text-slate-600">Rate per hour:</span>
                                    <span className="font-semibold text-slate-800">₹{selectedSlot.rate_per_hour}</span>
                                </div>
                                <div className="flex justify-between text-sm">
                                    <span className="text-slate-600">Status:</span>
                                    <span className={getStatusBadgeClass(selectedSlot.status)}>
                                        {selectedSlot.status.toUpperCase()}
                                    </span>
                                </div>
                            </div>

                            <div>
                                <label className="block text-sm font-medium text-slate-700 mb-2">
                                    Duration (hours)
                                </label>
                                <input
                                    type="number"
                                    min="1"
                                    max="24"
                                    value={bookingForm.duration_hours}
                                    onChange={(e) => setBookingForm({ duration_hours: parseInt(e.target.value) })}
                                    className="input-field"
                                    required
                                />
                            </div>

                            <div className="bg-primary-50 p-4 rounded-lg">
                                <div className="flex justify-between items-center">
                                    <span className="text-sm text-slate-700">Total Amount:</span>
                                    <span className="text-2xl font-bold text-primary-600">
                                        ₹{selectedSlot.rate_per_hour * bookingForm.duration_hours}
                                    </span>
                                </div>
                            </div>

                            <div className="flex space-x-3">
                                <button type="submit" className="btn-success flex-1">
                                    Proceed to Payment
                                </button>
                                <button
                                    type="button"
                                    onClick={() => {
                                        setShowBookingModal(false);
                                        clearSelectedSlot();
                                    }}
                                    className="btn-secondary flex-1"
                                >
                                    Cancel
                                </button>
                            </div>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;

