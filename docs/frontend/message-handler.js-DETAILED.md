# message-handler.js - Detaljeret Dokumentation

## Overordnet Formål
`message-handler.js` er kernen i chatbot UI'et. Den håndterer:
- Visning af chat messages (user/assistant)
- Code block creation og rendering med Prism.js
- Pasted code håndtering i left panel
- Scroll og highlight animations
- Communication med backend (/chat, /upload endpoints)
- Clickable code indicators med closure-baseret event handling

**Fil størrelse**: 344 linjer
**Dependencies**: message-parser.js, code-detector.js, Prism.js, ui-handlers.js

---

## Global State (Linje 1-8)

### Code Block Counters (Linje 4-5)
```javascript
let codeBlockCounter = 0;
let pastedCodeCounter = 0;
```
- **Linje 4**: `codeBlockCounter` - Tæller for bot's code outputs (højre panel)
  - Incrementeres hver gang bot sender code
  - Bruges til at generere unikke ID'er: `code-block-1`, `code-block-2`, osv.
  - Bruges i clickable indicators: `📝 Code #1`, `📝 Code #2`
  
- **Linje 5**: `pastedCodeCounter` - Tæller for user's pasted code (venstre panel)
  - Incrementeres hver gang user paster code
  - Genererer ID'er: `pasted-code-1`, `pasted-code-2`
  - Preserverer ALLE pasted codes (tidligere bug: blev overskrevet)

**Hvorfor globale counters?**
- Skal persistere på tværs af function calls
- Sikrer unikke ID'er (undgår ID collisions)
- Gør det muligt at reference specific code blocks

### DOM Element References (Linje 7-8)
```javascript
let chat, codeOutput, pastedCodeOutput, input;
```
- **Declared men ikke initialized** - værdier sættes senere i `ui-handlers.js`
- **chat** - `<div id="chat">` - Main chat container (left panel)
- **codeOutput** - `<div id="code-output">` - Bot code container (right panel)
- **pastedCodeOutput** - `<div id="pasted-code-output">` - User code container (middle panel)
- **input** - `<textarea id="input">` - User text input field

**Hvorfor deklareret her men initialized andet sted?**
- Modulær struktur - ui-handlers.js har ansvar for DOM setup
- Undgår null references - ui-handlers.js sætter værdier når DOM er ready
- Gør det muligt at bruge disse variabler i alle functions i denne fil

---

## appendMessage() Function (Linje 10-143)

### Function Signature (Linje 10)
```javascript
function appendMessage(role, text, isImage = false) {
```
- **role**: String - `'user'` eller `'assistant'`
  - Bruges til CSS class styling (orange/cyan i Cisco theme)
- **text**: String - Message content (kan være plain text eller markdown med code blocks)
- **isImage**: Boolean - Default `false`, `true` hvis text er image URL/blob
  - Used for screenshot display

### Empty Check (Linje 11-12)
```javascript
if (!text || text.trim() === '') return;
```
- **Linje 11**: Guard clause - exit early hvis text er falsy (`null`, `undefined`, `''`)
- `trim()` - Fjerner whitespace (spaces, tabs, newlines)
- Forhindrer tomme message bubbles i chat

### Message Parsing (Linje 13)
```javascript
const blocks = isImage ? [{type: 'image', content: text}] : parseMessage(text);
```
- **Ternary operator**: `condition ? ifTrue : ifFalse`
- **If image**: Wrap URL i object array `[{type: 'image', content: url}]`
- **If text**: Call `parseMessage(text)` fra `message-parser.js`
  - Returnerer array af blocks: `[{type: 'text', content: '...'}, {type: 'code', language: 'python', content: '...'}]`
  - Parser markdown, detecterer code blocks (```language)

### Block Processing Loop (Linje 15-141)
```javascript
blocks.forEach(block => {
```
- **forEach** - Itererer over alle blocks fra parser
- **block** object structure:
  - `{type: 'text', content: 'Hello world'}`
  - `{type: 'code', language: 'python', content: 'print("hi")'}`
  - `{type: 'image', content: 'blob:http://...'}`

---

### Text Block Handling (Linje 16-22)

#### Create Text Message Bubble (Linje 17-21)
```javascript
if (block.type === 'text') {
    const div = document.createElement('div');
    div.className = `message ${role}`;
    div.innerHTML = escapeHtml(block.content).replace(/\n/g, '<br>');
    chat.appendChild(div);
}
```
- **Linje 17**: Check if block is plain text (not code)
- **Linje 18**: Create new div element
- **Linje 19**: Set CSS classes
  - `message` - Base styling (border, padding, background)
  - `${role}` - `user` eller `assistant`
    - `.message.user` - Right-aligned, orange text (Cisco theme)
    - `.message.assistant` - Left-aligned, cyan text (Cisco theme)
  - Template literal evalueres til: `"message user"` eller `"message assistant"`

- **Linje 20**: Set inner HTML med security og formatting
  - `escapeHtml(block.content)` - Escaper HTML special chars (`<`, `>`, `&`, `"`, `'`)
    - Prevents XSS attacks (user kan ikke injicere `<script>` tags)
    - Function defined i `message-parser.js`
  - `.replace(/\n/g, '<br>')` - Regex replacement
    - `/\n/g` - Find ALL newlines (global flag `g`)
    - Replace med `<br>` - HTML line break tag
    - Preserverer line breaks i text (ellers collapes til single space i HTML)

- **Linje 21**: Append til chat container
  - Tilføjer element til DOM (bliver synlig)

**XSS Security Example:**
```javascript
// WITHOUT escapeHtml - DANGEROUS:
userInput = '<script>alert("hacked")</script>';
div.innerHTML = userInput; // EXECUTES SCRIPT!

// WITH escapeHtml - SAFE:
div.innerHTML = escapeHtml(userInput);
// Result: '&lt;script&gt;alert("hacked")&lt;/script&gt;'
// Displays as text, doesn't execute
```

---

### Code Block Handling (Linje 22-127)

#### Counter and Closure Setup (Linje 24-26)
```javascript
} else if (block.type === 'code') {
    codeBlockCounter++;
    const currentBlockNumber = codeBlockCounter;
```
- **Linje 23**: Check if block is code
- **Linje 24**: **Increment global counter** BEFORE creating elements
  - Sikrer hver code block har unikt nummer
- **Linje 26**: **CRITICAL: Closure capture**
  - `const currentBlockNumber = codeBlockCounter` - Captures CURRENT value
  - Hver iteration af loop får sin egen `currentBlockNumber` constant
  - **Hvorfor nødvendigt?**
    - Uden dette ville onclick handler bruge `codeBlockCounter` variable (ikke value)
    - Alle buttons ville reference samme værdi (den sidste)
    - **BUG FIX**: Tidligere fejl hvor alle buttons scrollede til sidste block

**Closure Example:**
```javascript
// WRONG - Alle buttons scroller til sidste block:
for (let i = 0; i < 3; i++) {
    button.onclick = () => console.log(i); // References variable
}
// All print 3 (final value of i)

// CORRECT - Hver button får sin egen value:
for (let i = 0; i < 3; i++) {
    const captured = i; // Capture current value
    button.onclick = () => console.log(captured);
}
// Print 0, 1, 2 respectively
```

#### Clickable Code Indicator in Chat (Linje 28-52)
```javascript
const indicator = document.createElement('div');
indicator.className = 'message assistant';
const codeTag = document.createElement('span');
codeTag.className = 'code-indicator';
codeTag.textContent = `📝 Code #${currentBlockNumber}`;
codeTag.dataset.targetId = `code-block-${currentBlockNumber}`;
```
- **Linje 28**: Create div for indicator message
- **Linje 29**: Style as assistant message (cyan in Cisco theme)
- **Linje 30**: Create span for clickable button
- **Linje 31**: `.code-indicator` class
  - Styled as button (background, border, hover effect)
  - Orange border/glow in Cisco theme
- **Linje 32**: Button text: `📝 Code #1`, `📝 Code #2`, etc.
  - Emoji + number for visual hierarchy
- **Linje 33**: Store target ID in data attribute
  - `dataset.targetId` → HTML attribute `data-target-id="code-block-1"`
  - Used for debugging/inspection (not currently used in code)

#### Scroll and Highlight Handler (Linje 34-50)
```javascript
codeTag.onclick = () => {
    const targetBlock = document.getElementById(`code-block-${currentBlockNumber}`);
    if (targetBlock) {
        const codeOutput = document.getElementById('code-output');
        const blockOffset = targetBlock.offsetTop - codeOutput.offsetTop;
        codeOutput.scrollTo({
            top: blockOffset,
            behavior: 'smooth'
        });
        
        targetBlock.classList.add('highlight');
        setTimeout(() => {
            targetBlock.classList.remove('highlight');
        }, 1000);
    }
};
```
- **Linje 34**: Arrow function onclick handler
  - **Uses `currentBlockNumber` from closure** - hver button har sin egen value
  
- **Linje 35**: Find target element i DOM
  - `code-block-${currentBlockNumber}` - matches ID created senere (linje 56)
  
- **Linje 36**: Null check - kun scroll hvis element findes
  
- **Linje 37**: Get right panel container
  
- **Linje 38**: **Calculate scroll offset**
  - `targetBlock.offsetTop` - Distance from top of PAGE to target (pixels)
  - `codeOutput.offsetTop` - Distance from top of PAGE to container
  - `blockOffset` = Difference = distance WITHIN container
  - **Why subtract?** offsetTop er absolut position, vi skal have relativ position
  
- **Linje 39-42**: **Smooth scroll animation**
  - `scrollTo()` - Moderne browser API
  - `top: blockOffset` - Scroll position (pixels from top of container)
  - `behavior: 'smooth'` - Animated scroll (default: instant jump)
  - Scrolls right panel til target block er ved top
  
- **Linje 44**: **Add highlight class**
  - CSS `.highlight` animation: orange/cyan glow (box-shadow)
  - Defined i `base.css`: `@keyframes ripple-glow`
  
- **Linje 45-47**: **Remove highlight after 1 second**
  - `setTimeout()` - Async delay (1000ms = 1 second)
  - Arrow function executed after delay
  - Removes class → animation stops
  - **Why remove?** Kan highlights igen ved next click (reusable animation)

#### Append Indicator to Chat (Linje 51-52)
```javascript
indicator.appendChild(document.createTextNode('Code output → '));
indicator.appendChild(codeTag);
chat.appendChild(indicator);
```
- **Linje 51**: Add text before button
  - `createTextNode()` - Safe text (ikke HTML element)
  - `'Code output → '` - Label med arrow emoji
- **Linje 52**: Add clickable button
- **Linje 53**: Add whole indicator to chat
  - Result: "Code output → 📝 Code #1" vises i chat

---

#### Code Block in Right Panel (Linje 55-127)

##### Wrapper Creation (Linje 55-61)
```javascript
const wrapper = document.createElement('div');
wrapper.className = 'codeblock';
wrapper.id = `code-block-${currentBlockNumber}`;

const chatHeight = chat.offsetHeight;
wrapper.style.maxHeight = `${chatHeight}px`;
```
- **Linje 55**: Create container for entire code block
- **Linje 56**: `.codeblock` class
  - Styled with border, background, padding (base.css)
  - Semi-transparent: `rgba(80, 80, 80, 0.5)` - viser dragon watermark through
- **Linje 57**: **Unique ID** - `code-block-1`, `code-block-2`, etc.
  - Used by onclick handler for scrolling (linje 35)
- **Linje 59**: Get chat window height
  - `offsetHeight` - Total height in pixels (includes padding/border)
- **Linje 60**: **Limit max height to chat height**
  - Prevents code block from being taller than viewport
  - User kan scroll INSIDE code block hvis longer
  - `${chatHeight}px` - Template literal evaluated to "500px" (example)

##### Pre and Code Elements (Linje 62-64)
```javascript
const pre = document.createElement('pre');
pre.style.maxHeight = `${chatHeight - 40}px`;
const code = document.createElement('code');
```
- **Linje 62**: `<pre>` - Preformatted text container
  - Preserves whitespace, line breaks, indentation
  - Standard for code display
- **Linje 63**: Set max height **40px less than wrapper**
  - `-40` accounts for header height (language label + copy button)
  - Ensures pre doesn't overflow wrapper
- **Linje 64**: `<code>` - Semantic HTML for code content
  - Goes inside `<pre>`
  - Target for Prism highlighting

##### Language Detection (Linje 66-79)
```javascript
let detectedLang = block.language || '';

if (!detectedLang || detectedLang === 'plaintext' || detectedLang === 'text' || 
    detectedLang === '' || detectedLang === 'bash' || detectedLang === 'shell') {
    const ciscoDetected = detectCiscoInContent(block.content);
    if (ciscoDetected) {
        detectedLang = ciscoDetected;
    } else {
        detectedLang = detectedLang || 'plaintext';
    }
}

const prismLang = getPrismLanguage(detectedLang);
```
- **Linje 66**: Get language from parser
  - `block.language` - Fra markdown: ` ```python`
  - `|| ''` - Fallback til empty string hvis undefined

- **Linje 68-70**: **Cisco override logic**
  - AI often mislabels Cisco config as bash/shell/plaintext
  - Check if "generic" language detected
  - **Conditions for override attempt:**
    - No language specified (`''`)
    - Generic labels: `plaintext`, `text`
    - Shell languages: `bash`, `shell` (Cisco uses `!` comments like bash)

- **Linje 71**: Call `detectCiscoInContent()` from `code-detector.js`
  - Scans content for Cisco patterns:
    - Router/switch prompts: `Router>`, `Switch#`
    - Commands: `interface`, `switchport`, `ip address`
    - Comment lines: `!`
  - Returns `'cisco'`, `'cisco-ios'`, eller `null`

- **Linje 72-76**: Apply detection result
  - If Cisco detected: Use that language
  - If not: Keep original (or fallback to 'plaintext')

- **Linje 79**: **Map to Prism language name**
  - `getPrismLanguage()` from `code-detector.js`
  - Maps custom names to Prism names:
    - `'cisco'` → `'cisco'` (custom Prism language in prism-cisco.js)
    - `'python'` → `'python'`
    - `'javascript'` → `'javascript'`
    - `''` → `'plaintext'`

##### Apply Language Classes (Linje 81-82)
```javascript
pre.className = `language-${prismLang}`;
code.className = `language-${prismLang}`;
```
- **Prism convention**: Classes MUST be `language-*`
- Examples:
  - `class="language-python"`
  - `class="language-cisco"`
  - `class="language-javascript"`
- **Both pre and code need classes**
  - Prism uses these for highlighting rules
  - CSS can style based on language

##### Escape Backticks in Content (Linje 84-85)
```javascript
const safeContent = block.content.replace(/```/g, '``\\`');
code.textContent = safeContent;
```
- **Linje 84**: **Escape triple backticks**
  - `/```/g` - Regex: find all ` ``` ` (markdown code fence)
  - Replace with ` ``\` ` - escaped version
  - **Why?** Code kan indeholde markdown (meta-circular)
    - Bot might explain "use ```python to start code block"
    - Unescaped ``` ville confuse rendering
  
- **Linje 85**: Set text content
  - `textContent` (not innerHTML) - safer, no HTML parsing
  - Assigns code string til element

##### Code Header with Language and Copy (Linje 88-101)
```javascript
const header = document.createElement('div');
header.className = 'code-header';

const langLabel = document.createElement('span');
langLabel.className = 'code-language';
langLabel.textContent = detectedLang.toUpperCase();

const copyBtn = document.createElement('button');
copyBtn.className = 'copy-btn';
copyBtn.textContent = 'Copy';

const feedback = document.createElement('div');
feedback.className = 'copy-feedback';
feedback.textContent = 'Copied!';
```
- **Linje 88-89**: Header container
  - Flexbox layout: label left, button right (CSS)
  
- **Linje 91-93**: Language label
  - Shows detected language: "PYTHON", "CISCO", "JAVASCRIPT"
  - `toUpperCase()` - konsistent styling
  
- **Linje 95-97**: Copy button
  - Text: "Copy" (changes to "Copied!" on click via feedback)
  
- **Linje 99-101**: "Copied!" feedback overlay
  - Hidden by default (CSS: `opacity: 0`)
  - Positioned absolute in center of code block
  - Shows briefly when copy succeeds

##### Copy Functionality (Linje 103-109)
```javascript
copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(block.content)
        .then(() => {
            feedback.classList.add('show');
            setTimeout(() => feedback.classList.remove('show'), 2000);
        });
});
```
- **Linje 103**: Event listener on button
  
- **Linje 104**: **Clipboard API**
  - `navigator.clipboard.writeText()` - Modern browser API
  - Writes `block.content` to clipboard
  - **Returns Promise** - async operation
  - **Requires HTTPS** (or localhost) - security requirement
  
- **Linje 105**: `.then()` - Promise success handler
  - Executes when copy succeeds
  
- **Linje 106**: Show feedback
  - `.add('show')` - CSS class that makes feedback visible
  - CSS animation: fade in, scale up
  
- **Linje 107**: Hide after 2 seconds
  - `setTimeout()` - 2000ms delay
  - Removes 'show' class → fade out animation

##### Assemble Code Block (Linje 111-120)
```javascript
header.appendChild(langLabel);
header.appendChild(copyBtn);

wrapper.appendChild(header);
wrapper.appendChild(feedback);
pre.appendChild(code);
wrapper.appendChild(pre);
codeOutput.appendChild(wrapper);
document.getElementById('right-panel').classList.add('visible');
```
- **Linje 111-112**: Build header
  - langLabel + copyBtn inside header
  
- **Linje 114**: Add header to wrapper
- **Linje 115**: Add feedback overlay to wrapper
- **Linje 116**: Add code inside pre
- **Linje 117**: Add pre to wrapper
- **Linje 118**: Add complete wrapper to right panel
  
- **Linje 119**: Make right panel visible
  - Starts hidden (CSS: `display: none`)
  - Adding 'visible' class → `display: block`
  - **Why?** Only show panel when there's code to display

**DOM Structure:**
```
wrapper.codeblock#code-block-1
├── header.code-header
│   ├── langLabel.code-language ("PYTHON")
│   └── copyBtn.copy-btn ("Copy")
├── feedback.copy-feedback ("Copied!")
└── pre.language-python
    └── code.language-python (actual code text)
```

##### Prism Syntax Highlighting (Linje 122-127)
```javascript
if (typeof Prism !== 'undefined' && Prism.highlightElement) {
    requestAnimationFrame(() => {
        try {
            Prism.highlightElement(code);
        } catch(e) { /* ignore */ }
    });
}
```
- **Linje 122**: **Safety check**
  - `typeof Prism !== 'undefined'` - Er Prism loaded? (CDN might fail)
  - `Prism.highlightElement` - Er function available?
  
- **Linje 123**: **requestAnimationFrame()**
  - Browser API: wait for next paint cycle
  - **Why?** DOM needs to be rendered før highlighting
  - Ensures element is visible before Prism processes it
  - Prevents blocking main thread
  
- **Linje 124-125**: **Try-catch**
  - `Prism.highlightElement(code)` - Apply syntax highlighting
    - Parses code content
    - Wraps keywords, strings, comments in `<span>` tags
    - Applies CSS classes for colors
  - Wrapped in try-catch - hvis Prism fejler, don't crash app
  
- **Linje 125**: `catch(e) { /* ignore */ }`
  - Empty catch block - silent failure
  - Code displays as plaintext if highlighting fails
  - **Why ignore?** Better to show unstyled code than error

**Prism Example Output:**
```html
<!-- Before Prism: -->
<code class="language-python">def hello(): print("hi")</code>

<!-- After Prism: -->
<code class="language-python">
  <span class="token keyword">def</span> hello():
  <span class="token builtin">print</span>(<span class="token string">"hi"</span>)
</code>
```

---

### Image Block Handling (Linje 128-133)
```javascript
} else if (block.type === 'image') {
    const img = document.createElement('img');
    img.className = 'screenshot';
    img.src = block.content;
    chat.appendChild(img);
}
```
- **Linje 128**: Check if block is image
- **Linje 129**: Create img element
- **Linje 130**: `.screenshot` class - CSS styling (max-width, border)
- **Linje 131**: Set source to blob URL or image path
  - From `uploadScreenshotFile()` - `URL.createObjectURL(file)`
- **Linje 132**: Add to chat
  - Images display inline in conversation

---

### Auto-Scroll to Bottom (Linje 136-139)
```javascript
setTimeout(() => {
    chat.scrollTop = chat.scrollHeight;
}, 50);
```
- **Linje 136**: Delay 50ms
  - **Why?** DOM needs time to render new elements
  - Without delay: scrollHeight not updated yet
  
- **Linje 137**: **Scroll to bottom**
  - `scrollTop` - Current scroll position (readable/writable)
  - `scrollHeight` - Total height of content (read-only)
  - Setting `scrollTop = scrollHeight` → scrolls to bottom
  - **Effect**: New messages always visible, auto-scroll

---

## sendMessage() Function (Linje 145-241)

### Function Overview
Sends user message to backend, handles code detection, displays response.

### Input Validation (Linje 146-147)
```javascript
const msg = input.value.trim();
if (!msg) return;
```
- **Linje 146**: Get text from textarea, remove whitespace
- **Linje 147**: Exit if empty - don't send blank messages

### Code Detection (Linje 149-161)
```javascript
const hasCodeBlock = msg.includes('```');

const lowerMsg = msg.toLowerCase();
const isCiscoConfig = (msg.match(/^[\w.-]+[#>]/m) || 
                      lowerMsg.includes('interface ') || 
                      lowerMsg.includes('switchport ') ||
                      lowerMsg.includes('ip address') ||
                      (lowerMsg.includes('vlan') && msg.includes('!'))) &&
                      msg.split('\n').length > 3;
```
- **Linje 149**: Check for markdown code fence
  - `includes('```')` - user formatted code with backticks
  
- **Linje 151**: Lowercase for case-insensitive checks
  
- **Linje 152-158**: **Cisco auto-detection**
  - **Linje 152**: Regex `/^[\w.-]+[#>]/m`
    - `^` - Start of line (multiline mode: `m`)
    - `[\w.-]+` - Word chars, dots, hyphens (hostname)
    - `[#>]` - Router prompt (# = privileged, > = user)
    - Example matches: `Router#`, `Switch>`, `SW-01#`
  
  - **Linje 153-156**: Keyword detection
    - Common Cisco commands: `interface`, `switchport`, `ip address`
    - VLAN config with `!` comments
  
  - **Linje 157**: Multi-line check
    - `split('\n').length > 3` - More than 3 lines
    - Single line commands → normal message
    - Config blocks → code

### Code Handling Branch (Linje 163-198)
```javascript
if (hasCodeBlock || isCiscoConfig) {
    pastedCodeCounter++;
    const detectedLang = detectLanguage(msg);
    addPastedCode(msg, detectedLang, pastedCodeCounter);
    document.getElementById('input-panel').classList.add('visible');
    
    const currentPastedNumber = pastedCodeCounter;
```
- **Linje 163**: If ANY code detected
- **Linje 164**: **Increment pasted counter**
  - BEFORE creating elements (like bot code)
- **Linje 165**: Detect language from `code-detector.js`
- **Linje 166**: Add code to left panel (function defined senere)
- **Linje 167**: Show left panel (hidden by default)
- **Linje 169**: **Closure capture** - hver paste får unikt nummer

#### Clickable Indicator for Pasted Code (Linje 171-197)
```javascript
const indicator = document.createElement('div');
indicator.className = 'message user';

const codeTag = document.createElement('span');
codeTag.className = 'code-indicator';
codeTag.textContent = `📝 Code #${currentPastedNumber}`;
codeTag.dataset.targetId = `pasted-code-${currentPastedNumber}`;
codeTag.onclick = () => {
    const targetBlock = document.getElementById(`pasted-code-${currentPastedNumber}`);
    if (targetBlock) {
        const pastedOutput = document.getElementById('pasted-code-output');
        const blockOffset = targetBlock.offsetTop - pastedOutput.offsetTop;
        pastedOutput.scrollTo({
            top: blockOffset,
            behavior: 'smooth'
        });
        
        targetBlock.classList.add('highlight');
        setTimeout(() => {
            targetBlock.classList.remove('highlight');
        }, 1000);
    }
};

indicator.appendChild(document.createTextNode('Code input ← '));
indicator.appendChild(codeTag);
chat.appendChild(indicator);
```
- **Same structure as bot code indicator**
- **Differences:**
  - `message user` class → orange styling (Cisco theme)
  - Text: `'Code input ← '` (arrow points left to panel)
  - Scrolls `pastedCodeOutput` panel (not `codeOutput`)
  - Target ID: `pasted-code-${number}` (not `code-block-`)

### Normal Text Branch (Linje 198-201)
```javascript
} else {
    appendMessage('user', msg);
}
input.value = '';
```
- **Linje 199**: If NOT code → display as normal text message
- **Linje 201**: Clear textarea
  - Ready for next input
  - Happens AFTER message sent (not before) - preserves msg reference

### AI Model Selection (Linje 203-205)
```javascript
const aiModelDropdown = document.getElementById('ai-model-dropdown');
const selectedModel = aiModelDropdown ? aiModelDropdown.value : 'mistral';
```
- **Linje 203**: Get dropdown element
- **Linje 204**: Get selected value
  - `aiModelDropdown.value` - `'mistral'` or `'github-copilot'`
  - Ternary: fallback to `'mistral'` if dropdown not found

### Backend Request (Linje 207-241)

#### Timeout Setup (Linje 209-211)
```javascript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 300000);
```
- **Linje 209**: **AbortController** - Modern API for canceling fetch
- **Linje 210**: Set 5 minute timeout (300,000ms)
  - Calls `abort()` after 5 min
  - Cancels pending request

#### Fetch Request (Linje 213-221)
```javascript
const res = await fetch('/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        message: msg,
        ai_model: selectedModel
    }),
    signal: controller.signal
});
```
- **Linje 213**: **POST to /chat endpoint**
  - `await` - pauses function until response
  
- **Linje 214**: POST method
  
- **Linje 215**: Headers
  - `Content-Type: application/json` - tells backend format
  
- **Linje 216-219**: Request body
  - `JSON.stringify()` - convert object to JSON string
  - `message` - user's text
  - `ai_model` - selected provider
  
- **Linje 220**: Attach abort signal
  - Controller kan cancel request

#### Response Handling (Linje 223-233)
```javascript
clearTimeout(timeoutId);

if (!res.ok) {
    const errorText = await res.text();
    throw new Error(`HTTP ${res.status}: ${errorText || res.statusText}`);
}

const data = await res.json();
appendMessage('assistant', data.response);
```
- **Linje 223**: Cancel timeout
  - Response received, don't need timeout anymore
  
- **Linje 225**: Check HTTP status
  - `res.ok` - true if status 200-299
  - false if 400+ (error)
  
- **Linje 226-227**: Handle errors
  - Get error text from body
  - Throw Error with status code
  
- **Linje 230**: Parse JSON response
  - `await res.json()` - parse body as JSON
  - `data.response` - bot's message text
  
- **Linje 231**: Display response
  - Calls `appendMessage()` → parses → displays

#### Error Handling (Linje 232-240)
```javascript
} catch(err) {
    if (err.name === 'AbortError') {
        appendMessage('assistant', '⏱️ Request timeout - The AI is taking too long to respond. Please try again with a shorter message.');
    } else {
        appendMessage('assistant', `❌ Error: ${err.message || 'Failed to connect to server'}`);
    }
}
```
- **Linje 232**: Catch ALL errors (network, timeout, JSON parse)
  
- **Linje 233**: Check error type
  - `AbortError` - thrown by `controller.abort()`
  - Specific timeout message
  
- **Linje 236**: Other errors
  - Network failure, server error, etc.
  - Display error message in chat
  - `err.message` - error details

---

## uploadScreenshotFile() Function (Linje 243-274)

### Function Signature (Linje 243)
```javascript
async function uploadScreenshotFile(file) {
```
- **file** - File object from `<input type="file">`
- Called from `ui-handlers.js` when user selects image

### FormData Upload (Linje 244-246)
```javascript
const formData = new FormData();
formData.append('screendump', file);
```
- **FormData** - API for multipart/form-data (file uploads)
- `append('screendump', file)` - add file with field name
  - Backend expects `request.files['screendump']`

### User Feedback (Linje 248)
```javascript
appendMessage('user', '[Uploaded screenshot]');
```
- Show placeholder in chat
- Actual image displayed later (linje 270)

### Timeout and Request (Linje 250-259)
```javascript
const controller = new AbortController();
const timeoutId = setTimeout(() => controller.abort(), 120000);

const res = await fetch('/upload', {
    method: 'POST',
    body: formData,
    signal: controller.signal
});
```
- **2 minute timeout** (120,000ms) - images take longer than text
- **POST to /upload endpoint**
- **No Content-Type header** - browser sets automatically for FormData
  - `multipart/form-data; boundary=...`

### Response Processing (Linje 264-271)
```javascript
const data = await res.json();
appendMessage('assistant', data.response);

const blobUrl = URL.createObjectURL(file);
appendMessage('assistant', blobUrl, true);
```
- **Linje 264**: Get AI's analysis text
- **Linje 265**: Display as message
  
- **Linje 267**: **Create blob URL**
  - `URL.createObjectURL(file)` - generates temporary URL
  - Format: `blob:http://localhost:5000/abc123...`
  - Points to file in memory (not server)
  
- **Linje 268**: Display image
  - `isImage = true` parameter
  - Uses image block handler (linje 128-133)

### Error Handling (Linje 272-274)
```javascript
} catch(err) {
    if (err.name === 'AbortError') {
        appendMessage('assistant', 'Upload timed out after 2 minutes. Please try again.');
    } else {
        appendMessage('assistant', 'Upload error: ' + err.message);
    }
}
```
- Similar to sendMessage errors
- Specific timeout message for uploads

---

## addPastedCode() Function (Linje 276-344)

### Function Signature (Linje 276)
```javascript
function addPastedCode(content, language, counter) {
```
- **content** - Raw code text
- **language** - Detected language string
- **counter** - Unique number for this code block
- Called from `sendMessage()` (linje 166)

### Wrapper Setup (Linje 277-284)
```javascript
const wrapper = document.createElement('div');
wrapper.className = 'codeblock';
wrapper.id = `pasted-code-${counter}`;
wrapper.style.marginBottom = '15px';

const chatHeight = chat.offsetHeight;
wrapper.style.maxHeight = `${chatHeight}px`;
```
- **Same structure as bot code**
- **ID**: `pasted-code-1`, `pasted-code-2`, etc.
- **Margin**: 15px spacing between multiple pasted codes
- **Max height**: Limited to chat height

### Header Creation (Linje 286-298)
```javascript
const header = document.createElement('div');
header.className = 'code-header';

const langLabel = document.createElement('span');
langLabel.className = 'code-language';
langLabel.textContent = `#${counter} ${(language || 'plaintext').toUpperCase()}`;

const copyBtn = document.createElement('button');
copyBtn.className = 'copy-btn';
copyBtn.textContent = 'Copy';

const feedback = document.createElement('div');
feedback.className = 'copy-feedback';
feedback.textContent = 'Copied!';
```
- **Language label includes counter**: `#1 CISCO`, `#2 PYTHON`
- **Same copy button structure** as bot code

### Copy Functionality (Linje 300-307)
```javascript
copyBtn.addEventListener('click', () => {
    navigator.clipboard.writeText(content)
        .then(() => {
            feedback.classList.add('show');
            setTimeout(() => feedback.classList.remove('show'), 2000);
        });
});
```
- Identical to bot code copy (linje 103-109)

### Assemble Header (Linje 309-310)
```javascript
header.appendChild(langLabel);
header.appendChild(copyBtn);
```

### Code Element Setup (Linje 312-319)
```javascript
const pre = document.createElement('pre');
pre.style.maxHeight = `${chatHeight - 40}px`;
const code = document.createElement('code');

const prismLang = getPrismLanguage(language || '');
pre.className = `language-${prismLang}`;
code.className = `language-${prismLang}`;
code.textContent = content;
```
- **No Cisco override logic** - language already detected in `sendMessage()`
- Direct mapping via `getPrismLanguage()`

### Assemble and Add to DOM (Linje 321-326)
```javascript
pre.appendChild(code);
wrapper.appendChild(header);
wrapper.appendChild(feedback);
wrapper.appendChild(pre);
pastedCodeOutput.appendChild(wrapper);
```
- Build complete structure
- Add to LEFT panel (`pastedCodeOutput`, not `codeOutput`)

### Prism Highlighting (Linje 328-334)
```javascript
if (typeof Prism !== 'undefined' && Prism.highlightElement) {
    requestAnimationFrame(() => {
        try {
            Prism.highlightElement(code);
        } catch(e) { /* ignore */ }
    });
}
```
- **Same highlighting logic** as bot code
- Comment: "Use same highlighting method as right panel for consistency"

### Auto-Scroll (Linje 336-337)
```javascript
pastedCodeOutput.scrollTop = pastedCodeOutput.scrollHeight;
```
- Scroll LEFT panel to bottom
- New pasted code always visible

---

## Key Design Patterns

### 1. Closure-Based Event Handlers
**Problem**: Loop variables referenced in callbacks get final value.
**Solution**: Capture current value in constant before creating handler.
```javascript
for (let i = 0; i < 3; i++) {
    const captured = i; // Closure
    button.onclick = () => console.log(captured);
}
```

### 2. Requestanimationframe for DOM Updates
**Problem**: Prism needs rendered DOM to highlight.
**Solution**: Defer highlighting to next paint cycle.
```javascript
requestAnimationFrame(() => {
    Prism.highlightElement(code);
});
```

### 3. Try-Catch for External Dependencies
**Problem**: Prism or browser APIs might fail.
**Solution**: Silent fallback - app continues working.
```javascript
try {
    Prism.highlightElement(code);
} catch(e) { /* ignore - show plaintext */ }
```

### 4. Global Counters for Unique IDs
**Problem**: Need unique identifiers for code blocks.
**Solution**: Increment global counter, capture value in closure.
```javascript
let counter = 0;
// ...
counter++;
const current = counter; // Capture for closure
element.id = `block-${current}`;
```

### 5. Async/Await with Timeout
**Problem**: Long-running requests need timeout.
**Solution**: AbortController + setTimeout.
```javascript
const controller = new AbortController();
setTimeout(() => controller.abort(), 300000);
await fetch(url, { signal: controller.signal });
```

---

## Data Flow Diagram

### User Sends Message:
```
User types → sendMessage()
    ↓
Detect code? → hasCodeBlock || isCiscoConfig
    ├─ YES → addPastedCode() → Left panel
    │         appendMessage('user', indicator) → Chat
    └─ NO → appendMessage('user', text) → Chat
    ↓
Clear input
    ↓
Fetch /chat endpoint
    ↓
Parse response → parseMessage()
    ↓
appendMessage('assistant', blocks)
    ├─ Text blocks → Chat
    └─ Code blocks → Right panel + indicator in Chat
```

### Bot Returns Code:
```
appendMessage('assistant', response)
    ↓
parseMessage(response) → [{type:'text'}, {type:'code'}]
    ↓
For each code block:
    ├─ codeBlockCounter++
    ├─ Capture: const current = counter
    ├─ Create indicator with onclick (uses current)
    ├─ Add indicator to chat
    ├─ Create code wrapper with ID: code-block-${current}
    ├─ Detect language (Cisco override)
    ├─ Add to right panel
    └─ Prism.highlightElement()
```

---

## Security Considerations

1. **XSS Prevention**: `escapeHtml()` on all user text
2. **Content Security**: `textContent` instead of `innerHTML` for code
3. **Backtick Escaping**: Prevents markdown injection
4. **HTTPS Required**: Clipboard API security requirement
5. **Blob URLs**: Temporary, memory-only (not server paths)

---

## Performance Optimizations

1. **requestAnimationFrame**: Non-blocking Prism highlighting
2. **setTimeout for scroll**: Allows DOM to render first
3. **Try-catch**: Doesn't block on Prism errors
4. **Abort controller**: Prevents memory leaks from pending requests
5. **Max height limits**: Prevents huge code blocks from lagging scroll

---

## Konklusion

`message-handler.js` er kernen i chatbot interaktionen. Den håndterer:
- **Messaging**: Display af user/assistant messages
- **Code rendering**: Prism syntax highlighting, copy functionality
- **Interactive UI**: Clickable indicators, smooth scroll, highlight animations
- **Backend communication**: Async fetch with timeout handling
- **File uploads**: Multipart form data, blob URLs
- **Language detection**: Auto-detect Cisco, override AI mislabeling

**Critical bugs fixed:**
- Closure capture for code buttons (alle buttons highlightede sidste block)
- Preserved pasted codes (tidligere blev overskrevet)

**File size**: 344 lines of essential frontend logic.
