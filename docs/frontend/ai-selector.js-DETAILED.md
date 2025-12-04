# ai-selector.js - Detaljeret Dokumentation

## Overordnet Formål
`ai-selector.js` håndterer AI model dropdown funktionalitet. Den:
- Dynamisk opretter dropdown options baseret på tilgængelige AI providers
- Loader saved model preference fra localStorage
- Viser visual feedback ved model switch
- Disabler dropdown hvis kun én model tilgængelig
- Gemmer valg til næste session

**Fil størrelse**: 97 linjer
**Dependencies**: Kræver `window.mistralAvailable`, `window.githubAvailable` fra index.html
**Pattern**: IIFE (Immediately Invoked Function Expression) for encapsulation

---

## IIFE Wrapper (Linje 3-96)

### Structure
```javascript
(function() {
    'use strict';
    // ... code
})();
```

**Purpose of IIFE:**
- **Encapsulation** - Variables don't pollute global scope
- **Self-executing** - Runs immediately when script loads
- **No exports needed** - Setup code, not library

**How it works:**
```javascript
(function() {
    // Code here
})();
// ↑ Function definition
//   ↑ Immediate invocation
```

### Strict Mode (Linje 4)
```javascript
'use strict';
```
- **ES5 feature** - Enforces stricter parsing
- **Prevents**:
  - Undeclared variables (`x = 5` without `var/let/const`)
  - Duplicate function parameters
  - `with` statement
- **Better debugging** - Throws errors instead of silent failures

---

## initAISelector() Function (Linje 6-77)

### Function Declaration (Linje 6)
```javascript
function initAISelector() {
```
- **Scope**: Within IIFE (not global)
- **Called once** on page load (linje 93 eller 95)

### Get Dropdown Element (Linje 7-8)
```javascript
const dropdown = document.getElementById('ai-model-dropdown');
if (!dropdown) return;
```
- **Linje 7**: Query dropdown fra index.html
  - `<select id="ai-model-dropdown">`
- **Linje 8**: **Guard clause** - exit if not found
  - Prevents errors if HTML structure changes
  - Graceful degradation

### Check Available Models (Linje 11-19)
```javascript
const options = [];

if (window.mistralAvailable) {
    options.push({value: 'mistral', text: '🤖 Mistral AI'});
}

if (window.githubAvailable) {
    options.push({value: 'github-copilot', text: '💻 GitHub Copilot'});
}
```

#### Options Array (Linje 11)
- **Empty array** - will be populated based on availability
- **Structure**: `[{value: 'mistral', text: '🤖 Mistral AI'}, ...]`

#### Mistral Check (Linje 13-15)
- **window.mistralAvailable** - Boolean from index.html Jinja2 template
  ```html
  <script>
      window.mistralAvailable = {{ mistral_available|lower }};
  </script>
  ```
- **Python → JavaScript**: `True` → `true`, `False` → `false`
- **value**: `'mistral'` - sent to backend in `/chat` request
- **text**: `'🤖 Mistral AI'` - displayed to user (with emoji)

#### GitHub Check (Linje 17-19)
- **window.githubAvailable** - Same pattern as Mistral
- **value**: `'github-copilot'`
- **text**: `'💻 GitHub Copilot'` - laptop emoji

**Backend Configuration:**
```python
# bot.py
mistral_available = bool(os.getenv('MISTRAL_API_KEY'))
github_available = bool(os.getenv('GITHUB_TOKEN'))

return render_template('index.html', 
    mistral_available=mistral_available,
    github_available=github_available
)
```

### Populate Dropdown (Linje 22-28)
```javascript
dropdown.innerHTML = '';
options.forEach(opt => {
    const option = document.createElement('option');
    option.value = opt.value;
    option.textContent = opt.text;
    dropdown.appendChild(option);
});
```

#### Clear Existing (Linje 22)
- **`innerHTML = ''`** - Remove all child elements
- **Why?** Function might run multiple times (though unlikely)
- **Clean slate** before adding new options

#### Create Options (Linje 23-27)
- **Linje 23**: Loop over options array
- **Linje 24**: Create `<option>` element
- **Linje 25**: Set `value` attribute
  - Used in backend: `request.json['ai_model']`
- **Linje 26**: Set display text (with emoji)
- **Linje 27**: Append to dropdown

**Generated HTML:**
```html
<select id="ai-model-dropdown">
    <option value="mistral">🤖 Mistral AI</option>
    <option value="github-copilot">💻 GitHub Copilot</option>
</select>
```

### Restore Saved Selection (Linje 31-37)
```javascript
const savedModel = localStorage.getItem('selectedAIModel');
if (savedModel && dropdown.querySelector(`option[value="${savedModel}"]`)) {
    dropdown.value = savedModel;
} else {
    dropdown.value = window.mistralAvailable ? 'mistral' : (options[0]?.value || 'mistral');
}
```

#### Load from localStorage (Linje 31)
- **Key**: `'selectedAIModel'`
- **Value**: `'mistral'` or `'github-copilot'` (from previous session)
- **Returns**: String or `null` if not found

#### Validate and Set (Linje 32-33)
- **Linje 32**: **Two conditions**:
  - `savedModel` - Not null (user has previous selection)
  - `dropdown.querySelector(...)` - Option still exists
    - **Why check?** API key might be removed since last session
    - Prevents selecting non-existent option

- **Linje 33**: Set dropdown to saved value
  - `dropdown.value = 'mistral'` - Selects that option

#### Fallback Default (Linje 34-36)
- **Linje 35**: **Ternary chain**:
  1. `window.mistralAvailable ? 'mistral'` - Prefer Mistral if available
  2. `: (options[0]?.value || 'mistral')` - Otherwise first option
  3. `|| 'mistral'` - Final fallback if options empty

**Logic Tree:**
```
Saved model exists AND valid?
├─ YES → Use saved model
└─ NO → Mistral available?
    ├─ YES → Use Mistral
    └─ NO → First option available?
        ├─ YES → Use first option
        └─ NO → Default to 'mistral' (will fail, but graceful)
```

### Disable if Single Option (Linje 40-43)
```javascript
if (options.length === 1) {
    dropdown.disabled = true;
    dropdown.style.opacity = '0.7';
}
```
- **Linje 40**: Check if only one provider configured
- **Linje 41**: **Disable dropdown**
  - User can't change (no alternatives)
  - Grayed out in UI
- **Linje 42**: **Visual feedback**
  - 70% opacity (semi-transparent)
  - Indicates disabled state

**Why disable?**
- **UX clarity** - No point in dropdown if no choice
- **Prevents confusion** - User can't "switch" to same model
- **Still shows info** - Displays which model is active

### Visual Feedback on Change (Linje 46-69)

#### Change Event Listener (Linje 46-68)
```javascript
dropdown.addEventListener('change', function() {
    const modelName = this.options[this.selectedIndex].text;
    
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 60px;
        right: 20px;
        background: rgba(0, 255, 0, 0.2);
        border: 1px solid #00ff00;
        color: #00ff00;
        padding: 10px 20px;
        border-radius: 5px;
        z-index: 10000;
        font-family: monospace;
        animation: fadeInOut 2s ease-in-out;
    `;
    notification.textContent = `Switched to ${modelName}`;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.remove();
    }, 2000);
});
```

##### Get Selected Model Name (Linje 47)
```javascript
const modelName = this.options[this.selectedIndex].text;
```
- **this** - The dropdown element (event target)
- **this.options** - Array-like collection of `<option>` elements
- **this.selectedIndex** - Index of selected option (0, 1, 2, ...)
- **text** - Display text (`'🤖 Mistral AI'`)

**Example:**
```html
<select>
    <option>🤖 Mistral AI</option>    <!-- selectedIndex = 0 -->
    <option>💻 GitHub Copilot</option> <!-- selectedIndex = 1 -->
</select>
```

##### Create Notification (Linje 50-65)
- **Linje 50**: Create div element

- **Linje 51**: **Inline CSS** via cssText
  - **position: fixed** - Stays in viewport on scroll
  - **top: 60px** - Below theme dropdown
  - **right: 20px** - Right corner
  - **background: rgba(0, 255, 0, 0.2)** - 20% green (semi-transparent)
  - **border: 1px solid #00ff00** - Bright green border
  - **color: #00ff00** - Bright green text (Matrix style)
  - **padding: 10px 20px** - Inner spacing
  - **border-radius: 5px** - Rounded corners
  - **z-index: 10000** - Above everything
  - **font-family: monospace** - Terminal style
  - **animation: fadeInOut 2s** - CSS animation (defined linje 81-86)

- **Linje 65**: Set text content
  - Template literal: `Switched to 🤖 Mistral AI`

- **Linje 66**: Append to body (becomes visible)

##### Auto-Remove (Linje 68-70)
```javascript
setTimeout(() => {
    notification.remove();
}, 2000);
```
- **2 second delay** (2000ms)
- **Remove from DOM** - Cleans up

**Timeline:**
```
0s: User changes dropdown
↓
0s: Notification appears (fadeIn animation)
↓
1s: Notification fully visible
↓
2s: Notification removed (fadeOut complete)
```

### Save to localStorage (Linje 73-75)
```javascript
dropdown.addEventListener('change', function() {
    localStorage.setItem('selectedAIModel', this.value);
});
```
- **Separate listener** - Could be combined with above
- **Saves immediately** on change
- **Key**: `'selectedAIModel'`
- **Value**: `'mistral'` or `'github-copilot'`
- **Persists** across page reloads and browser restarts

---

## CSS Animation (Linje 79-88)

### Style Injection
```javascript
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translateY(-10px); }
        20% { opacity: 1; transform: translateY(0); }
        80% { opacity: 1; transform: translateY(0); }
        100% { opacity: 0; transform: translateY(-10px); }
    }
`;
document.head.appendChild(style);
```

### Animation Breakdown
- **0% (0s)**: 
  - `opacity: 0` - Invisible
  - `transform: translateY(-10px)` - 10px above final position
  
- **20% (0.4s)**:
  - `opacity: 1` - Fully visible
  - `transform: translateY(0)` - At final position
  - **Effect**: Quick fade in + slide down

- **20-80% (0.4s - 1.6s)**:
  - Stay visible and stationary
  - **1.2 seconds** of full visibility

- **80-100% (1.6s - 2s)**:
  - `opacity: 0` - Fade out
  - `translateY(-10px)` - Slide up
  - **Effect**: Quick fade out + slide up

**Visual Timeline:**
```
0s ────┬──── 0.4s ──────────── 1.6s ────┬──── 2s
       │                                  │
    Fade in                           Fade out
    Slide down                        Slide up
       │                                  │
       └──── Visible for 1.2s ───────────┘
```

### Why Inject CSS?
- **Self-contained module** - No external CSS file needed
- **Dynamic loading** - Only loads if script loads
- **No conflicts** - Animation name scoped to this feature

---

## Initialization (Linje 91-95)

### DOM Ready Check
```javascript
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAISelector);
} else {
    initAISelector();
}
```

#### Check readyState (Linje 91)
- **document.readyState** - Current document loading state:
  - `'loading'` - Still parsing HTML
  - `'interactive'` - HTML parsed, resources loading
  - `'complete'` - Fully loaded

#### Conditional Initialization (Linje 92-95)
- **If loading**: Wait for `DOMContentLoaded` event
  - HTML not fully parsed yet
  - Dropdown might not exist
  - **Safe**: Wait for DOM ready
  
- **If already loaded**: Call immediately
  - Script loaded late (async/defer)
  - DOM already available
  - **Safe**: No need to wait

**Why check?**
- **Script placement**: Could be in `<head>` or end of `<body>`
- **Async loading**: Script might load before/after DOM
- **Reliability**: Works in all scenarios

---

## Data Flow Diagram

### Page Load:
```
index.html loads
    ↓
Jinja2 renders:
    window.mistralAvailable = true;
    window.githubAvailable = false;
    ↓
ai-selector.js executes
    ↓
IIFE runs → initAISelector() called
    ↓
Check available models:
    ├─ Mistral: TRUE → Add option
    └─ GitHub: FALSE → Skip
    ↓
Populate dropdown (1 option)
    ↓
Load saved model from localStorage
    ↓
Set dropdown value
    ↓
Disable dropdown (only 1 option)
    ↓
Register change listeners
```

### User Changes Model:
```
User selects dropdown → 'change' event
    ↓
Parallel actions:
    ├─ Create green notification
    │   ├─ "Switched to 💻 GitHub Copilot"
    │   ├─ Show for 2 seconds
    │   └─ Auto-remove
    │
    └─ Save to localStorage
        └─ 'selectedAIModel' = 'github-copilot'
    ↓
Next message sent:
    └─ message-handler.js reads dropdown.value
        └─ Sends to backend: { ai_model: 'github-copilot' }
```

---

## localStorage Integration

### Data Structure
```javascript
localStorage = {
    'selectedAIModel': 'mistral',  // or 'github-copilot'
    'chatbot-theme': 'cisco',      // From themes.js
    // ... other keys
}
```

### Persistence
- **Survives**: Page reload, browser restart
- **Scope**: Per origin (http://localhost:5000)
- **Size limit**: ~5MB (varies by browser)
- **Type**: Strings only (no objects)

### Security
- **Not encrypted** - Readable in DevTools
- **Same-origin policy** - Other sites can't access
- **No sensitive data** - Just UI preference

---

## Backend Integration

### Request Format
```javascript
// message-handler.js
fetch('/chat', {
    method: 'POST',
    body: JSON.stringify({
        message: 'Hello',
        ai_model: 'github-copilot'  // From dropdown.value
    })
})
```

### Backend Handling
```python
# bot.py
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    ai_model = data.get('ai_model', 'mistral')  # Default to Mistral
    
    if ai_model == 'mistral':
        response = query_mistral(message)
    elif ai_model == 'github-copilot':
        response = query_github(message)
    
    return jsonify({'response': response})
```

---

## Error Handling

### Missing Dropdown
```javascript
if (!dropdown) return;
```
- **Graceful failure** - No errors thrown
- **Silent**: Nothing happens if dropdown missing
- **Robust**: Works even if HTML changes

### No Models Available
```javascript
dropdown.value = options[0]?.value || 'mistral';
```
- **Optional chaining**: `options[0]?.value`
  - Returns `undefined` if `options` empty
- **Fallback**: `|| 'mistral'`
  - Sets to 'mistral' even if not available
  - Backend will handle error

### Invalid Saved Model
```javascript
if (savedModel && dropdown.querySelector(`option[value="${savedModel}"]`)) {
```
- **Validation**: Checks option exists before setting
- **Scenario**: API key removed since last session
- **Result**: Falls back to default

---

## Browser Compatibility

### localStorage
- **IE 8+**, **Chrome 4+**, **Firefox 3.5+**, **Safari 4+**
- **Fallback**: Feature detection possible
  ```javascript
  if (typeof localStorage !== 'undefined') {
      localStorage.setItem(...);
  }
  ```

### CSS Animations
- **IE 10+**, **Chrome 43+**, **Firefox 16+**, **Safari 9+**
- **Fallback**: Notification still shows (no animation)

### Optional Chaining (`?.`)
- **Chrome 80+**, **Firefox 74+**, **Safari 13.1+**
- **Fallback**: Use regular check
  ```javascript
  options[0] && options[0].value || 'mistral'
  ```

---

## Performance

### Initialization
- **Single call** on page load
- **Minimal DOM operations** (create 1-2 options)
- **Fast**: < 1ms execution time

### Change Handler
- **Event-driven** - Only runs on user action
- **Notification cleanup** - Auto-removed (no memory leak)
- **localStorage write** - Synchronous but fast (< 1ms)

---

## Testing Scenarios

### Test 1: Both Models Available
```
1. Set both API keys in .env
2. Load page
3. Dropdown shows 2 options
4. Dropdown enabled
5. Can switch between models
→ PASS
```

### Test 2: Only Mistral Available
```
1. Only MISTRAL_API_KEY set
2. Load page
3. Dropdown shows 1 option (Mistral)
4. Dropdown disabled (opacity 0.7)
5. Can't change selection
→ PASS
```

### Test 3: Saved Preference
```
1. Select GitHub Copilot
2. Reload page
3. GitHub still selected
4. localStorage has 'selectedAIModel' = 'github-copilot'
→ PASS
```

### Test 4: Notification
```
1. Switch model
2. Green notification appears top-right
3. Shows "Switched to [model]"
4. Fades out after 2 seconds
→ PASS
```

---

## Konklusion

`ai-selector.js` provides intelligent AI model selection:
- **Dynamic options** based on backend configuration
- **Persistent preference** via localStorage
- **Visual feedback** with animated notifications
- **Smart defaults** (Mistral preferred)
- **Graceful degradation** (disable if single option)
- **IIFE encapsulation** (no global pollution)

**Key design decisions:**
- Check availability from backend (not hardcoded)
- Disable dropdown if no choice (UX clarity)
- Green Matrix-style notification (theme consistency)
- Save immediately on change (no delay)
- Validate saved preference (handle removed API keys)

**File size**: 97 lines of smart selector logic.
