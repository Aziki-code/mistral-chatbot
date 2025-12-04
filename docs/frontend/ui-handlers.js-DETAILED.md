# ui-handlers.js - Detaljeret Dokumentation

## Overordnet Formål
`ui-handlers.js` initialiserer UI og event listeners. Den:
- Finder og cacher DOM elements
- Registrerer click/keyboard/paste handlers
- Auto-scroller chat til bunden ved load
- Detekterer pasted code i textarea
- Håndterer image paste fra clipboard
- Dynamisk tilpasser code block heights ved resize

**Fil størrelse**: 110 linjer
**Dependencies**: message-handler.js, code-detector.js, themes.js
**Pattern**: Single initialization function + DOMContentLoaded
**Globals set**: `chat`, `codeOutput`, `pastedCodeOutput`, `input` (used by message-handler.js)

---

## initializeUI() Function (Linje 3-106)

### Function Declaration (Linje 3)
```javascript
function initializeUI() {
```
- **Called once** on page load
- **Sets up entire UI** - Event listeners, theme, scroll
- **No return value** - Side effects only

---

## DOM Element Initialization (Linje 4-11)

### Get Elements (Linje 5-11)
```javascript
chat = document.getElementById("chat");
codeOutput = document.getElementById("code-output");
pastedCodeOutput = document.getElementById("pasted-code-output");
input = document.getElementById("input");
const send = document.getElementById("send");
const upload = document.getElementById("upload");
const uploadBtn = document.getElementById("uploadBtn");
```

#### Global Variables (Linje 5-8)
```javascript
chat = document.getElementById("chat");
codeOutput = document.getElementById("code-output");
pastedCodeOutput = document.getElementById("pasted-code-output");
input = document.getElementById("input");
```
- **No `const`/`let`** - Creates global variables
- **Why?** Used by `message-handler.js` functions:
  - `appendMessage()` uses `chat`, `codeOutput`
  - `addPastedCode()` uses `pastedCodeOutput`
  - `sendMessage()` uses `input`
- **Implicit global** - Not declared with `var` (works in non-strict mode)

**HTML references:**
```html
<!-- index.html -->
<div id="chat" class="chat"></div>
<div id="code-output" class="code-output"></div>
<textarea id="input"></textarea>
```

#### Local Variables (Linje 9-11)
```javascript
const send = document.getElementById("send");
const upload = document.getElementById("upload");
const uploadBtn = document.getElementById("uploadBtn");
```
- **Local scope** - Only used in this function
- **send** - Send button (registers onclick)
- **upload** - Hidden file input (`<input type="file">`)
- **uploadBtn** - Visible upload button (triggers file input)

---

## Theme Initialization (Linje 13-14)

### Call initThemes()
```javascript
initThemes();
```
- **From themes.js** - Forces Cisco theme
- **Must run early** - Before UI visible
- **Sets CSS variables** - Background, text colors, etc.

---

## Auto-Scroll on Load (Linje 16-29)

### Purpose
When page loads with existing messages (from session), scroll to bottom immediately.

### scrollToBottom Helper (Linje 17-21)
```javascript
const scrollToBottom = () => {
    if (chat) {
        chat.scrollTop = chat.scrollHeight;
    }
};
```

#### How scrollTop Works
- **scrollTop** - Current scroll position (pixels from top)
- **scrollHeight** - Total content height (including overflow)
- **Setting scrollTop = scrollHeight** - Scrolls to bottom

**Example:**
```
chat.scrollHeight = 2000px (total content)
chat.offsetHeight = 600px (visible area)
chat.scrollTop = 2000 (scroll to bottom)
    ↓
Bottom 600px visible, top 1400px hidden
```

#### Guard Clause (Linje 18)
```javascript
if (chat) {
```
- **Prevents error** if chat element missing
- **Graceful failure** - Function doesn't crash

### Multiple Scroll Attempts (Linje 24-28)
```javascript
// Immediate scroll
scrollToBottom();

// Delayed scrolls to handle async content
setTimeout(scrollToBottom, 50);
setTimeout(scrollToBottom, 200);
setTimeout(scrollToBottom, 500);
```

#### Why Multiple Attempts?
- **Linje 24**: Immediate scroll
  - DOM just loaded, might not have final heights
  
- **Linje 27**: 50ms delay
  - CSS finished loading
  - Fonts rendered
  
- **Linje 28**: 200ms delay
  - Images might have loaded
  - Code blocks rendered
  
- **Linje 29**: 500ms delay
  - **Final check** - Everything definitely loaded
  - Prism.js syntax highlighting complete

**Problem solved:**
Without delays, scroll might happen before content fully renders, leaving user mid-page instead of at bottom.

---

## Send Button Handler (Linje 31-32)

### Click Event
```javascript
send.onclick = sendMessage;
```
- **sendMessage** from message-handler.js
- **No parentheses** - Passes function reference (not calling it)
- **Why onclick?** Simple, works everywhere

**Equivalent:**
```javascript
send.addEventListener('click', sendMessage);
```

---

## Enter Key Handler (Linje 34-40)

### Keyboard Event
```javascript
input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});
```

#### Event Type: 'keydown'
- **Why not 'keypress'?** Deprecated
- **Why not 'keyup'?** Fires after key released (slower feel)
- **keydown** - Fires immediately when key pressed

#### Condition (Linje 35)
```javascript
if (e.key === 'Enter' && !e.shiftKey) {
```
- **e.key === 'Enter'** - Enter key pressed
- **!e.shiftKey** - Shift NOT held
  - **Shift+Enter** - Insert newline (default textarea behavior)
  - **Enter alone** - Send message (custom behavior)

#### Prevent Default (Linje 36)
```javascript
e.preventDefault();
```
- **Stops** newline insertion
- **Without this**: Message sent AND newline added to textarea

#### Send Message (Linje 37)
```javascript
sendMessage();
```
- **From message-handler.js**
- Reads textarea value, sends to backend, clears input

**User experience:**
```
User types: "Hello world"
Presses Enter → sendMessage() → Message sent, textarea cleared
Presses Shift+Enter → Default behavior → Newline added
```

---

## Upload Button Handler (Linje 42-45)

### Click Event
```javascript
uploadBtn.onclick = () => {
    if (upload.files.length) uploadScreenshotFile(upload.files[0]);
};
```

#### HTML Structure
```html
<input type="file" id="upload" style="display:none" accept="image/*">
<button id="uploadBtn">📎 Upload Image</button>
```
- **upload** - Hidden file input (browser file picker)
- **uploadBtn** - Visible button (user clicks this)

#### Logic Flow
1. **User clicks uploadBtn** - Visible button
2. **Browser shows file picker** - From hidden `upload` input
3. **User selects file** - `upload.files[0]` populated
4. **uploadBtn.onclick fires** - Check if file selected
5. **If file exists** - Call `uploadScreenshotFile()`

#### File Check (Linje 43)
```javascript
if (upload.files.length)
```
- **upload.files** - FileList object (array-like)
- **length** - Number of files selected (0 if canceled)
- **files[0]** - First file (only one allowed in single file input)

**Edge case:** User clicks button but cancels file picker → length = 0 → Nothing happens

---

## Pasted Code Detection (Linje 47-73)

### Purpose
Show live preview when user pastes code into textarea (before sending).

### State Variable (Linje 48)
```javascript
let lastPreviewedCode = '';
```
- **Prevents duplicate previews** - Only update if changed
- **String comparison** - Exact match check

### Input Event Listener (Linje 49-72)
```javascript
input.addEventListener('input', e => {
```
- **'input' event** - Fires on any textarea change
  - Typing, pasting, deleting, autocomplete
- **e.target.value** - Current textarea content

#### Get Value (Linje 50)
```javascript
const value = e.target.value.trim();
```
- **trim()** - Remove leading/trailing whitespace
- **Why?** Empty spaces shouldn't trigger detection

#### Length Check (Linje 51)
```javascript
if (value.length > 20) {
```
- **20 character minimum** - Prevents false positives
- **Short text** like "Hello world" won't trigger
- **Code snippets** usually longer

#### Detect Language (Linje 52)
```javascript
const detectedLang = detectLanguage(value);
```
- **From code-detector.js** - Returns language or `null`
- **Examples:**
  - `"print('hello')"` → `'python'`
  - `"interface GigabitEthernet0/1"` → `'cisco'`
  - `"Hello world"` → `null`

#### Show Preview (Linje 54-59)
```javascript
if (detectedLang && value !== lastPreviewedCode) {
    // Show live preview of what will be pasted (doesn't affect counter)
    lastPreviewedCode = value;
    document.getElementById('input-panel').classList.add('visible');
```

##### Condition (Linje 55)
- **detectedLang** - Code detected (not regular text)
- **value !== lastPreviewedCode** - Content changed since last check
  - **Prevents** re-showing same preview

##### Update State (Linje 57)
```javascript
lastPreviewedCode = value;
```
- **Remember current value** - For next comparison

##### Show Panel (Linje 58)
```javascript
document.getElementById('input-panel').classList.add('visible');
```
- **input-panel** - Left panel div
- **CSS class 'visible'** - Shows panel (CSS transition)

**CSS (base.css):**
```css
.input-panel {
    opacity: 0;
    transition: opacity 0.3s;
}
.input-panel.visible {
    opacity: 1;
}
```

#### Hide Preview (Linje 59-66)
```javascript
} else if (!detectedLang) {
    // Not code
    lastPreviewedCode = '';
    if (pastedCodeCounter === 0) {
        document.getElementById('input-panel').classList.remove('visible');
    }
}
```

##### Clear State (Linje 61)
```javascript
lastPreviewedCode = '';
```
- **Reset** - No code detected

##### Hide Panel Conditionally (Linje 62-64)
```javascript
if (pastedCodeCounter === 0) {
    document.getElementById('input-panel').classList.remove('visible');
}
```
- **pastedCodeCounter** - From message-handler.js (global)
  - Tracks permanent pasted code blocks
- **Only hide if counter = 0** - No existing pasted code
- **Why?** If user already pasted code (counter > 0), keep panel visible

#### Empty Input (Linje 67-72)
```javascript
} else if (value.length === 0) {
    lastPreviewedCode = '';
    if (pastedCodeCounter === 0) {
        document.getElementById('input-panel').classList.remove('visible');
    }
}
```
- **User cleared textarea** - Hide preview
- **Same logic** as "not code" case

---

## Clipboard Paste Handler (Linje 75-84)

### Purpose
Detect images pasted from clipboard (screenshots, Ctrl+V).

### Document-Level Event (Linje 76)
```javascript
document.addEventListener('paste', e => {
```
- **document-level** - Works anywhere on page
- **Not just textarea** - Can paste image even if not focused

### Clipboard Items (Linje 77)
```javascript
const items = e.clipboardData.items;
```
- **clipboardData** - Browser clipboard API
- **items** - DataTransferItemList (array-like)
  - Multiple items if user copied mixed content

### Loop Through Items (Linje 78-82)
```javascript
for (let item of items) {
    if (item.type.indexOf('image') !== -1) {
        const file = item.getAsFile();
        uploadScreenshotFile(file);
    }
}
```

#### Image Check (Linje 79)
```javascript
if (item.type.indexOf('image') !== -1) {
```
- **item.type** - MIME type string
  - `'image/png'`, `'image/jpeg'`, `'text/plain'`, etc.
- **indexOf('image')** - Check if contains 'image'
  - Returns -1 if not found
  - Returns index if found (any value >= 0)

#### Get File (Linje 80)
```javascript
const file = item.getAsFile();
```
- **Returns**: File object (like from `<input type="file">`)
- **Contains**: Binary image data

#### Upload (Linje 81)
```javascript
uploadScreenshotFile(file);
```
- **From message-handler.js** - Sends to backend
- **User experience**: Paste screenshot → Instantly uploaded → AI analyzes image

**Example flow:**
```
User presses PrtScn (screenshot to clipboard)
    ↓
User presses Ctrl+V in chatbot
    ↓
'paste' event fires
    ↓
Loop finds image/png item
    ↓
Extract File object
    ↓
uploadScreenshotFile() sends to /upload
    ↓
Backend analyzes image with Mistral Vision
```

---

## Focus Input (Linje 86-87)

### Auto-Focus
```javascript
input.focus();
```
- **Sets keyboard focus** to textarea
- **User can type immediately** - No need to click
- **UX best practice** - Chatbot ready to use instantly

---

## Resize Handler (Linje 89-99)

### Purpose
Dynamically adjust code block heights when browser window resizes.

### Window Event (Linje 90)
```javascript
window.addEventListener('resize', () => {
```
- **Fires when** - User drags window edge, maximizes, splits screen
- **Throttling?** No, but resize events naturally limited by browser

### Get Chat Height (Linje 91)
```javascript
const chatHeight = chat.offsetHeight;
```
- **offsetHeight** - Element's rendered height in pixels
- **Includes**: Padding, border (not margin)
- **Why?** Code blocks should fit within chat area (no overflow page)

### Update All Code Blocks (Linje 92-98)
```javascript
document.querySelectorAll('.codeblock').forEach(block => {
    block.style.maxHeight = `${chatHeight}px`;
    const pre = block.querySelector('pre');
    if (pre) {
        pre.style.maxHeight = `${chatHeight - 40}px`;
    }
});
```

#### Find All Code Blocks (Linje 92)
```javascript
document.querySelectorAll('.codeblock')
```
- **Returns**: NodeList of all `.codeblock` elements
- **Created by**: message-handler.js `appendMessage()`

#### Set Block Height (Linje 93)
```javascript
block.style.maxHeight = `${chatHeight}px`;
```
- **Example**: If chat = 600px → `block.style.maxHeight = "600px"`
- **Why maxHeight?** Allows smaller blocks, prevents huge blocks

#### Set Pre Height (Linje 94-97)
```javascript
const pre = block.querySelector('pre');
if (pre) {
    pre.style.maxHeight = `${chatHeight - 40}px`;
}
```
- **pre** - Contains actual code (inside codeblock div)
- **40px less** - Account for code header (language + copy button)
- **Guard clause**: `if (pre)` - Handle missing pre element

**HTML structure:**
```html
<div class="codeblock">
    <div class="code-header">🐍 python [Copy]</div> <!-- ~40px -->
    <pre><code class="language-python">...</code></pre>
</div>
```

**Why needed?**
Without this, a long code block could exceed viewport height, making page scroll awkwardly.

---

## Initialization Timing (Linje 102-106)

### DOM Ready Check
```javascript
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeUI);
} else {
    initializeUI();
}
```

#### readyState Values
- **'loading'** - HTML still being parsed
- **'interactive'** - HTML parsed, but resources (images, CSS) still loading
- **'complete'** - Everything loaded

#### Conditional Init
- **If loading**: Wait for DOMContentLoaded
  - DOM not ready, elements don't exist yet
  - **Safe**: Wait for HTML parse complete
  
- **Else**: Call immediately
  - DOM already ready (script loaded late)
  - **No need to wait**

**Same pattern** as ai-selector.js - ensures reliability regardless of script placement.

---

## Data Flow Diagram

### Page Load:
```
index.html loads
    ↓
<script src="ui-handlers.js">
    ↓
Check document.readyState
    ↓
DOM ready? → initializeUI()
    ↓
Parallel initialization:
    ├─ Cache DOM elements (chat, input, etc.)
    ├─ Call initThemes() → Apply Cisco theme
    ├─ Scroll chat to bottom (4 attempts)
    ├─ Register event listeners:
    │   ├─ Send button click
    │   ├─ Enter key (textarea)
    │   ├─ Upload button click
    │   ├─ Input change (code detection)
    │   ├─ Paste (image detection)
    │   └─ Window resize (code blocks)
    └─ Focus textarea
```

### User Interaction:
```
User pastes code in textarea
    ↓
'input' event fires
    ↓
detectLanguage(value) → 'python'
    ↓
Add 'visible' class to input-panel
    ↓
Left panel slides in (CSS transition)
```

```
User presses Enter
    ↓
'keydown' event fires
    ↓
Check: Enter without Shift?
    ↓
preventDefault() → No newline
    ↓
sendMessage() → Fetch /chat
    ↓
appendMessage() → Render response
    ↓
Resize handler → Adjust code block heights
```

---

## Global Variables Set

### Globals Created
```javascript
// Set in initializeUI() (no var/let/const = implicit global)
chat               // <div id="chat">
codeOutput         // <div id="code-output">
pastedCodeOutput   // <div id="pasted-code-output">
input              // <textarea id="input">
```

### Why Global?
- **Used by message-handler.js** - Must be accessible
- **Alternative**: Could use `window.chat = ...` (more explicit)
- **Risk**: Name collisions (but unlikely with specific names)

### Used In:
```javascript
// message-handler.js
function appendMessage(msg) {
    // Uses: chat, codeOutput (global from ui-handlers.js)
    const block = document.createElement('div');
    chat.appendChild(block);
}

function sendMessage() {
    // Uses: input (global)
    const text = input.value;
}

function addPastedCode(code, lang) {
    // Uses: pastedCodeOutput (global)
    pastedCodeOutput.appendChild(block);
}
```

---

## Event Listeners Summary

### Registered Events:
1. **send.onclick** → sendMessage
2. **input keydown** → Enter key check
3. **uploadBtn.onclick** → File upload trigger
4. **input 'input'** → Pasted code detection
5. **document 'paste'** → Image clipboard detection
6. **window 'resize'** → Code block height adjustment

### Event Propagation:
- **document.addEventListener('paste')** - Capture phase, works everywhere
- **input.addEventListener('input')** - Bubble phase, only on textarea
- **window.addEventListener('resize')** - Global event

---

## Performance Considerations

### Resize Handler
- **Fires often** - Every pixel while dragging
- **Performance**: querySelectorAll + forEach on every resize
- **Optimization**: Could use throttle/debounce
  ```javascript
  let resizeTimeout;
  window.addEventListener('resize', () => {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(() => {
          // Update heights
      }, 100); // Only after 100ms of no resize events
  });
  ```

### Scroll Attempts
- **4 setTimeout calls** - Slight memory overhead
- **Minimal impact** - Only on page load (not repeated)

### Paste Event
- **Document-level** - Fires on any paste
- **Minimal check**: `item.type.indexOf('image')`
- **Fast**: Only processes images

---

## Browser Compatibility

### Clipboard API
- **Chrome 42+**, **Firefox 41+**, **Safari 10.1+**
- **IE**: Partial support (clipboardData exists, but different API)
- **Fallback**: Could detect browser and use execCommand

### classList.add/remove
- **IE 10+**, **All modern browsers**
- **Fallback**: Could use `className += ' visible'`

### addEventListener
- **IE 9+**, **All modern browsers**
- **Universal support** for standard events

---

## Security Considerations

### File Upload
- **No validation** - Accepts any file user selects
- **Backend responsibility** - Must validate file type/size
- **Risk**: User could upload malware (backend should scan)

### Clipboard Access
- **User-initiated** - Paste requires user action (Ctrl+V)
- **No silent clipboard read** - Browser security prevents background access
- **Safe**: Can't steal clipboard data without user knowing

---

## Testing Scenarios

### Test 1: Send Message
```
1. Type message in textarea
2. Click send button
3. Message appears in chat
4. Textarea cleared
→ PASS
```

### Test 2: Enter Key
```
1. Type message
2. Press Enter
3. Message sent (no newline in textarea)
4. Press Shift+Enter
5. Newline added (message not sent)
→ PASS
```

### Test 3: Paste Code Detection
```
1. Paste Python code in textarea
2. Left panel shows preview
3. Clear textarea
4. Panel hides
→ PASS
```

### Test 4: Image Paste
```
1. Take screenshot (PrtScn)
2. Click anywhere in chatbot
3. Press Ctrl+V
4. Image uploaded to backend
5. AI analyzes image
→ PASS
```

### Test 5: Resize
```
1. Send message with code
2. Resize browser window
3. Code block adjusts height
4. No overflow beyond chat area
→ PASS
```

---

## Edge Cases

### Empty Chat on Load
- **scrollToBottom()** still works (scrollTop = 0)
- **No error** - graceful

### Multiple Images Pasted
- **Loop processes all** - `for (let item of items)`
- **All uploaded** - Multiple uploadScreenshotFile() calls
- **Backend handles** - Multiple /upload requests

### Resize During Message Send
- **Race condition?** No - resize handler reads current state
- **No conflict** - Different DOM operations

---

## Konklusion

`ui-handlers.js` is the UI initialization hub:
- **Central setup** - All event listeners registered here
- **Global caching** - DOM elements stored for other modules
- **Smart detection** - Pasted code preview, image clipboard
- **Responsive** - Auto-scroll, resize handling
- **User-friendly** - Auto-focus, Enter to send, Shift+Enter for newline

**Key design decisions:**
- Multiple scroll attempts (handle async content)
- Document-level paste (works anywhere on page)
- Code length threshold (20 chars prevents false positives)
- Resize updates all code blocks (dynamic layout)
- Implicit globals (message-handler.js needs access)

**File size**: 110 lines of essential UI glue code.
