import { create } from 'zustand';
import { STORAGE_KEYS } from '../config/config';

const useAuthStore = create((set) => ({
    user: JSON.parse(localStorage.getItem(STORAGE_KEYS.USER) || 'null'),
    accessToken: localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN),
    refreshToken: localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN),
    isAuthenticated: !!localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN),

    setAuth: (user, accessToken, refreshToken) => {
        localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
        localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, accessToken);
        localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, refreshToken);

        set({
            user,
            accessToken,
            refreshToken,
            isAuthenticated: true,
        });
    },

    clearAuth: () => {
        localStorage.removeItem(STORAGE_KEYS.USER);
        localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
        localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);

        set({
            user: null,
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false,
        });
    },

    updateUser: (userData) => {
        const updatedUser = { ...useAuthStore.getState().user, ...userData };
        localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(updatedUser));
        set({ user: updatedUser });
    },
}));

export default useAuthStore;
