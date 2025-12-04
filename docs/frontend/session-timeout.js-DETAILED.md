# session-timeout.js - Detaljeret Dokumentation

## Overordnet Formål
`session-timeout.js` implementerer auto-logout funktionalitet for sikkerhed. Den:
- Detecterer bruger inaktivitet (10 minutter)
- Viser warning alert
- Redirecter til logout page
- Beskytter mod uautoriseret adgang til forladt session

**Fil størrelse**: 43 linjer
**Dependencies**: Ingen
**Global exports**: `resetInactivityTimer()`, `initSessionTimeout()`

---

## Global State (Linje 4-5)

### Inactivity Timer (Linje 4)
```javascript
let inactivityTimer;
```
- **Purpose**: Holds `setTimeout` reference
- **Scope**: Global (module level)
- **Type**: `number` (timeout ID) or `undefined`
- **Used for**: Clearing/resetting timer

### Timeout Duration (Linje 5)
```javascript
const TIMEOUT_DURATION = 10 * 60 * 1000; // 10 minutes in milliseconds
```
- **Value**: `600000` (10 minutes)
- **Calculation**: 10 minutes × 60 seconds × 1000 milliseconds
- **Convention**: UPPERCASE for constants
- **Comment explains**: Human-readable duration

**Math breakdown:**
```
10 minutes
× 60 = 600 seconds
× 1000 = 600,000 milliseconds
```

---

## resetInactivityTimer() Function (Linje 7-19)

### Function Signature (Linje 7)
```javascript
function resetInactivityTimer() {
```

### Purpose
Resets the inactivity countdown. Called whenever user interacts with page.

### Clear Existing Timer (Linje 9-11)
```javascript
if (inactivityTimer) {
    clearTimeout(inactivityTimer);
}
```
- **Linje 9**: Check if timer exists
  - `undefined` on first call
  - `number` (timeout ID) after first call
  
- **Linje 10**: **Clear previous timeout**
  - `clearTimeout()` - Browser API
  - Cancels pending timeout
  - **Why?** Prevents multiple timers running simultaneously

**Example without clearing:**
```javascript
// BAD - Multiple timers:
setTimeout(logout, 600000);  // Timer 1
// User clicks → new timer
setTimeout(logout, 600000);  // Timer 2 (Timer 1 still running!)
// User clicks again
setTimeout(logout, 600000);  // Timer 3 (1 and 2 still running!)
// → Multiple logout attempts
```

**Correct with clearing:**
```javascript
// GOOD - Single timer:
const timer1 = setTimeout(logout, 600000);
// User clicks
clearTimeout(timer1);  // Cancel Timer 1
const timer2 = setTimeout(logout, 600000);  // Fresh timer
```

### Set New Timer (Linje 14-18)
```javascript
inactivityTimer = setTimeout(() => {
    alert('Session expired due to inactivity. You will be logged out.');
    window.location.href = '/logout';
}, TIMEOUT_DURATION);
```
- **Linje 14**: **setTimeout with arrow function**
  - `setTimeout(callback, delay)` - Browser API
  - Executes callback after delay
  - Returns timeout ID (stored in `inactivityTimer`)
  
- **Linje 15**: **Alert user**
  - `alert()` - Blocking browser dialog
  - **Message**: "Session expired due to inactivity. You will be logged out."
  - **Why alert?** Forces user to see message (can't miss it)
  - **Drawback**: Blocks page (user must click OK)
  
- **Linje 16**: **Redirect to logout**
  - `window.location.href = '/logout'` - Full page navigation
  - Goes to Flask `/logout` route
  - Backend clears session, redirects to login page
  
- **Linje 17**: **Delay**
  - `TIMEOUT_DURATION` = 600,000ms (10 minutes)

**Execution timeline:**
```
User last activity → Start 10-min timer
↓ (10 minutes of inactivity)
Alert shows → User clicks OK
↓
Redirect to /logout → Backend clears session
↓
Redirect to /login → User must log in again
```

---

## initSessionTimeout() Function (Linje 21-40)

### Function Signature (Linje 21)
```javascript
function initSessionTimeout() {
```

### Purpose
Sets up event listeners to detect user activity and initialize timeout system.

### Activity Events Array (Linje 23-29)
```javascript
const activityEvents = [
    'mousedown',
    'mousemove',
    'keypress',
    'scroll',
    'touchstart',
    'click'
];
```
- **Array of DOM event types** that indicate user is active
  
#### Event Breakdown:

1. **`'mousedown'`** - Mouse button pressed
   - Triggers before `click`
   - Catches drag starts
   
2. **`'mousemove'`** - Mouse cursor moves
   - **Most frequent** event
   - Detects mouse activity even without clicking
   
3. **`'keypress'`** - Keyboard key pressed
   - Typing in textarea
   - Keyboard shortcuts
   
4. **`'scroll'`** - Page scrolled
   - Mouse wheel
   - Keyboard (arrow keys, space)
   - Touch swipe
   
5. **`'touchstart'`** - Touch screen tap
   - **Mobile support**
   - Finger touches screen
   
6. **`'click'`** - Mouse click (button release)
   - Most common interaction
   - Buttons, links

**Why multiple events?**
- **Comprehensive coverage** - Different interaction types
- **Mobile + desktop** - `touchstart` for mobile, `mousedown`/`click` for desktop
- **Passive activity** - `mousemove` detects user present (even without clicking)

### Register Event Listeners (Linje 32-34)
```javascript
activityEvents.forEach(event => {
    document.addEventListener(event, resetInactivityTimer, true);
});
```
- **Linje 32**: Loop over each event type
  
- **Linje 33**: **addEventListener** with capture phase
  - `document.addEventListener(type, callback, useCapture)`
  - **Target**: `document` - Listens on entire page
  - **Callback**: `resetInactivityTimer` - Function reference (not invoked)
  - **useCapture**: `true` - **Capture phase** (not bubbling)

#### Event Propagation Phases:
```
Click on button:
1. CAPTURE phase (document → body → button)  ← We listen here
2. TARGET phase (button itself)
3. BUBBLE phase (button → body → document)
```

**Why capture phase?**
- **Triggers first** - Before any other handlers
- **Can't be stopped** - Even if event.stopPropagation() called
- **Reliable** - Catches all events, even if target prevents bubbling

**Example:**
```html
<button onclick="event.stopPropagation()">Click</button>

<!-- Without capture (useCapture: false): -->
document.addEventListener('click', reset, false);
// → WON'T trigger (stopPropagation blocks bubble phase)

<!-- With capture (useCapture: true): -->
document.addEventListener('click', reset, true);
// → WILL trigger (capture happens before stopPropagation)
```

### Start Initial Timer (Linje 37)
```javascript
resetInactivityTimer();
```
- **Call immediately** on page load
- Starts the first 10-minute countdown
- **Important**: Without this, timer only starts after first activity

---

## Auto-Initialize (Linje 43)

```javascript
initSessionTimeout();
```
- **Executes when script loads**
- No need to call from other files
- **Self-contained** - Works immediately

---

## Data Flow

### Initial Setup:
```
Page loads → script executes
    ↓
initSessionTimeout() called
    ↓
6 event listeners registered on document (capture phase)
    ↓
resetInactivityTimer() called
    ↓
10-minute timer starts
```

### User Activity:
```
User moves mouse → 'mousemove' event
    ↓
Capture phase triggers on document
    ↓
resetInactivityTimer() called
    ↓
clearTimeout(inactivityTimer)  ← Cancel old timer
    ↓
setTimeout(..., 10 minutes)  ← Start fresh 10-minute timer
```

### Inactivity Timeout:
```
10 minutes pass with no activity
    ↓
setTimeout callback executes
    ↓
alert('Session expired...')  ← User sees message
    ↓
User clicks OK
    ↓
window.location.href = '/logout'  ← Navigate to logout
    ↓
Flask /logout route:
    ├─ session.clear()
    └─ redirect('/login')
    ↓
User sees login page (must re-authenticate)
```

---

## Security Benefits

### 1. Protects Unattended Sessions
- **Scenario**: User walks away from computer
- **Without timeout**: Session active forever
- **With timeout**: Auto-logout after 10 minutes
- **Result**: Unauthorized person can't access account

### 2. OWASP Recommendation
- **OWASP Session Management Cheat Sheet** recommends timeouts
- **10-15 minutes** is standard for medium-security apps
- **High-security**: 2-5 minutes
- **Low-security**: 30+ minutes

### 3. Multi-Layer Protection
- **Client-side** (this file): UX convenience (warning + redirect)
- **Server-side** (Flask session): Actual security (session expiry)
- **Both needed**: Client can be bypassed, server enforces

---

## Potential Improvements

### 1. Warning Before Logout
```javascript
// 30 seconds before timeout:
setTimeout(() => {
    const keepAlive = confirm('Session about to expire. Stay logged in?');
    if (keepAlive) {
        resetInactivityTimer();  // Reset if user responds
    }
}, TIMEOUT_DURATION - 30000);
```

### 2. Backend Sync
```javascript
// Ping backend to keep session alive:
fetch('/ping', { method: 'POST' })
    .then(() => resetInactivityTimer());
```

### 3. Configurable Duration
```javascript
// Read timeout from backend:
const TIMEOUT_DURATION = window.sessionTimeoutConfig || (10 * 60 * 1000);
```

### 4. Activity Indicator
```javascript
// Show timer countdown in UI:
function updateTimerDisplay() {
    const remaining = (TIMEOUT_DURATION - Date.now() + lastActivity) / 1000;
    document.getElementById('timer').textContent = `${Math.floor(remaining / 60)}m`;
}
```

---

## Performance Considerations

### Event Listener Overhead
- **`mousemove` fires frequently** - Up to 60 times per second
- **`resetInactivityTimer()` is lightweight**:
  - 1 if check
  - 1 clearTimeout
  - 1 setTimeout
- **Total**: ~0.001ms per call
- **Impact**: Negligible (even at 60 FPS)

### Memory Leaks
- **Single timer** - Old timer cleared before new one
- **Event listeners** - Never removed (intentional - active for page lifetime)
- **No leaks** - Browser cleans up on page unload

---

## Browser Compatibility

### setTimeout/clearTimeout
- **All browsers** - Since JavaScript 1.0 (1995)
- **IE 5.5+**, **Chrome 1+**, **Firefox 1+**, **Safari 1+**

### addEventListener (capture phase)
- **IE 9+**, **Chrome 1+**, **Firefox 1+**, **Safari 1+**
- **Fallback for IE 8**: Use `attachEvent` (not implemented here)

### window.location.href
- **All browsers** - Universal support

---

## Testing Scenarios

### Test 1: Normal Activity
```
1. Load page → Timer starts (10 min)
2. Move mouse at 5 min → Timer resets (10 min)
3. Click at 9 min → Timer resets (10 min)
4. Type at 15 min → Timer resets (10 min)
→ PASS: No logout
```

### Test 2: Inactivity
```
1. Load page → Timer starts
2. Wait 10 minutes (no activity)
3. Alert shows → User clicks OK
4. Redirects to /logout
5. Session cleared, redirects to /login
→ PASS: Auto-logout works
```

### Test 3: Event Capture
```
1. Load page
2. Click button with stopPropagation()
3. Timer should still reset
→ PASS: Capture phase works
```

---

## Edge Cases

### 1. Multiple Tabs
- **Each tab** has own timer
- **One tab active** - Keeps session alive
- **All tabs inactive** - First to timeout logs out ALL tabs (shared session)

### 2. Alert Shown
- **Timer keeps running** during alert
- **If timeout occurs** while alert shown:
  - Second alert queued
  - User clicks first OK → Second alert shows immediately

### 3. Network Failure
- **Redirect to /logout** might fail if offline
- **User sees** error page or nothing happens
- **Session still expired** on backend (server-side timeout)

---

## Konklusion

`session-timeout.js` er en simpel men effektiv sikkerheds-feature:
- **Auto-logout** efter 10 minutters inaktivitet
- **Comprehensive activity detection** (mouse, keyboard, touch, scroll)
- **Capture phase listeners** (can't be blocked)
- **User-friendly alert** before logout
- **Security best practice** (OWASP recommendation)

**Key design decisions:**
- **10 minutes** - Balance mellem security og UX
- **Capture phase** - Reliable event detection
- **Alert** - Forces user awareness (not silent logout)
- **Self-initializing** - No setup needed

**File size**: 43 lines of essential security logic.
