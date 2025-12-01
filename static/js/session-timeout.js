// Session timeout functionality
// Auto-logout after 10 minutes of inactivity

let inactivityTimer;
const TIMEOUT_DURATION = 10 * 60 * 1000; // 10 minutes in milliseconds

function resetInactivityTimer() {
    // Clear existing timer
    if (inactivityTimer) {
        clearTimeout(inactivityTimer);
    }
    
    // Set new timer
    inactivityTimer = setTimeout(() => {
        // Auto-logout after timeout
        alert('Session expired due to inactivity. You will be logged out.');
        window.location.href = '/logout';
    }, TIMEOUT_DURATION);
}

function initSessionTimeout() {
    // Events that indicate user activity
    const activityEvents = [
        'mousedown',
        'mousemove',
        'keypress',
        'scroll',
        'touchstart',
        'click'
    ];
    
    // Reset timer on any activity
    activityEvents.forEach(event => {
        document.addEventListener(event, resetInactivityTimer, true);
    });
    
    // Start the initial timer
    resetInactivityTimer();
}

// Initialize on page load
initSessionTimeout();
