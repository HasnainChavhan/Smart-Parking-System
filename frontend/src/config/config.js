// API Configuration
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';
export const API_V1 = `${API_BASE_URL}/api/v1`;

// WebSocket Configuration
export const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000';
export const WS_V1 = `${WS_BASE_URL}/api/v1`;

// ML Service Configuration
export const ML_SERVICE_URL = import.meta.env.VITE_ML_SERVICE_URL || 'http://localhost:5000';

// App Configuration
export const APP_NAME = 'Smart Parking System';
export const APP_VERSION = '1.0.0';

// Local Storage Keys
export const STORAGE_KEYS = {
    ACCESS_TOKEN: 'parking_access_token',
    REFRESH_TOKEN: 'parking_refresh_token',
    USER: 'parking_user',
};

// API Endpoints
export const ENDPOINTS = {
    // Auth
    LOGIN: `${API_V1}/auth/login`,
    REGISTER: `${API_V1}/auth/register`,
    REFRESH: `${API_V1}/auth/refresh`,
    ME: `${API_V1}/auth/me`,
    LOGOUT: `${API_V1}/auth/logout`,

    // Parking Lots
    LOTS: `${API_V1}/lots`,
    LOT_BY_ID: (id) => `${API_V1}/lots/${id}`,
    SLOTS: (lotId) => `${API_V1}/lots/${lotId}/slots`,
    SLOT_STATUS: (lotId, slotId) => `${API_V1}/lots/${lotId}/slots/${slotId}/status`,

    // Bookings
    BOOKINGS: `${API_V1}/bookings`,
    BOOKING_VERIFY: `${API_V1}/bookings/verify`,

    // WebSocket
    WS_LOT: (lotId) => `${WS_V1}/ws/lot/${lotId}`,

    // Health
    HEALTH: `${API_V1}/health`,
    HEALTH_DETAILED: `${API_V1}/health/detailed`,

    // ML Service
    VIDEO_FEED: `${ML_SERVICE_URL}/video_feed`,
};

// Query Keys for React Query
export const QUERY_KEYS = {
    LOTS: 'lots',
    LOT: 'lot',
    SLOTS: 'slots',
    BOOKINGS: 'bookings',
    USER: 'user',
    HEALTH: 'health',
};

// Status Colors
export const STATUS_COLORS = {
    free: 'success',
    occupied: 'danger',
    reserved: 'warning',
};

// Slot Types
export const SLOT_TYPES = {
    REGULAR: 'regular',
    PREMIUM: 'premium',
    EV: 'ev',
};
