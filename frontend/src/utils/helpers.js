import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

/**
 * Utility function to merge Tailwind CSS classes
 * Combines clsx and tailwind-merge for optimal class handling
 */
export function cn(...inputs) {
    return twMerge(clsx(inputs));
}

/**
 * Format date to readable string
 */
export function formatDate(date) {
    if (!date) return '';
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
    });
}

/**
 * Format date and time to readable string
 */
export function formatDateTime(date) {
    if (!date) return '';
    return new Date(date).toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
    });
}

/**
 * Format currency
 */
export function formatCurrency(amount, currency = 'INR') {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency,
    }).format(amount);
}

/**
 * Get status color class
 */
export function getStatusColor(status) {
    const colors = {
        free: 'success',
        occupied: 'danger',
        reserved: 'warning',
        paid: 'success',
        pending: 'warning',
        cancelled: 'danger',
    };
    return colors[status] || 'primary';
}

/**
 * Get status badge class
 */
export function getStatusBadgeClass(status) {
    const classes = {
        free: 'badge-free',
        occupied: 'badge-occupied',
        reserved: 'badge-reserved',
    };
    return classes[status] || 'badge-free';
}

/**
 * Capitalize first letter
 */
export function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Truncate text
 */
export function truncate(str, length = 50) {
    if (!str) return '';
    if (str.length <= length) return str;
    return str.slice(0, length) + '...';
}

/**
 * Debounce function
 */
export function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

/**
 * Handle API errors
 */
export function handleApiError(error) {
    if (error.response) {
        // Server responded with error
        return error.response.data?.detail || error.response.data?.message || 'An error occurred';
    } else if (error.request) {
        // Request made but no response
        return 'No response from server. Please check your connection.';
    } else {
        // Something else happened
        return error.message || 'An unexpected error occurred';
    }
}
