# message-parser.js - Detaljeret Dokumentation

## Overordnet Formål
`message-parser.js` parser AI responses til strukturerede blocks (text/code). Den:
- Detekterer markdown code fences (```)
- Extraherer language identifiers
- Sikrer XSS protection via HTML escaping
- Bruger state-machine parser (robust mod edge cases)
- Håndterer unclosed code blocks gracefully

**Fil størrelse**: 71 linjer
**Dependencies**: Brugt af `message-handler.js`
**Pattern**: Pure functions (no side effects, testable)

---

## escapeHtml() Function (Linje 3-10)

### Function Declaration
```javascript
function escapeHtml(text) {
```
- **Pure function** - Same input → same output
- **No side effects** - Doesn't modify input
- **Security critical** - Prevents XSS attacks

### HTML Entity Replacement (Linje 4-9)
```javascript
return text.replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
```

#### Linje 4: Ampersand First
```javascript
.replace(/&/g, "&amp;")
```
- **MUST be first** - Otherwise escapes other replacements
- **Example without priority:**
  ```javascript
  "<" → "&lt;" → "&amp;lt;" (double-escaped!)
  ```
- **With priority:**
  ```javascript
  "&" → "&amp;" first
  "<" → "&lt;" (correct)
  ```
- **Regex**: `/&/g` - Global flag (all occurrences)

#### Linje 5: Less Than
```javascript
.replace(/</g, "&lt;")
```
- **Prevents**: `<script>alert('XSS')</script>`
- **Result**: `&lt;script&gt;...` (displayed as text, not executed)
- **Critical for**: Opening tags

#### Linje 6: Greater Than
```javascript
.replace(/>/g, "&gt;")
```
- **Prevents**: `<img src=x onerror=alert(1)>`
- **Result**: Tag becomes visible text
- **Paired with**: `<` for complete tag neutralization

#### Linje 7: Double Quote
```javascript
.replace(/"/g, "&quot;")
```
- **Prevents**: Attribute injection
  ```html
  <div title="Hello">  <!-- Safe -->
  <div title="Hello" onload="alert(1)">  <!-- Attack vector -->
  ```
- **After escaping**: `&quot;` can't break out of attributes

#### Linje 8: Single Quote
```javascript
.replace(/'/g, "&#039;")
```
- **Prevents**: Single-quoted attribute injection
  ```html
  <div onclick='alert("XSS")'>  <!-- Attack -->
  <div onclick='alert(&quot;XSS&quot;)'>  <!-- Escaped, safe -->
  ```
- **HTML entity**: `&#039;` (numeric reference)

### Security Example
**Malicious input:**
```javascript
"<script>alert('XSS')</script>"
```

**After escapeHtml:**
```html
&lt;script&gt;alert(&#039;XSS&#039;)&lt;/script&gt;
```

**Rendered in browser:**
```
<script>alert('XSS')</script>  (visible text, not executed)
```

---

## parseMessage() Function (Linje 12-71)

### Function Declaration (Linje 12)
```javascript
function parseMessage(text) {
```
- **Core parsing logic** - State machine implementation
- **Input**: Raw AI response with markdown
- **Output**: Array of `{type, content, language}` objects

### Return Structure
```javascript
[
    {type: 'text', content: 'This is a paragraph'},
    {type: 'code', language: 'python', content: 'print("hello")'},
    {type: 'text', content: 'More explanation'}
]
```

### State Variables (Linje 14-20)

#### blocks Array (Linje 14)
```javascript
const blocks = [];
```
- **Accumulator** - Final output
- **Empty at start** - Populated during parsing

#### Normalize and Split (Linje 15-16)
```javascript
const src = normalizeNewlines(text);
const lines = src.split('\n');
```
- **Linje 15**: `normalizeNewlines()` from code-detector.js
  - Converts `\r\n` → `\n` (Windows line endings)
  - Ensures consistent parsing across OS
- **Linje 16**: Split into array of lines
  - `['Line 1', 'Line 2', '```python', 'code', '```']`

#### State Machine Variables (Linje 17-20)
```javascript
let inCode = false;
let lang = 'plaintext';
let codeLines = [];
let textBuffer = [];
```

- **inCode** (Linje 17): Current parser state
  - `false` - Parsing text content
  - `true` - Inside code fence (``` ... ```)

- **lang** (Linje 18): Code block language
  - Extracted from opening fence: ` ```python`
  - Default: `'plaintext'` (no highlighting)

- **codeLines** (Linje 19): Accumulates code lines
  - Between opening and closing fences
  - Joined with `\n` before adding to blocks

- **textBuffer** (Linje 20): Accumulates text lines
  - Outside code fences
  - Trimmed and joined before adding to blocks

### flushText() Helper (Linje 22-28)
```javascript
function flushText() {
    if (textBuffer.length) {
        const t = textBuffer.join('\n').trim();
        if (t) blocks.push({type: 'text', content: t});
        textBuffer = [];
    }
}
```

#### Purpose
- **Finalize text block** - Move from buffer to blocks array
- **Called when**: Entering code fence or end of message

#### Logic Breakdown
- **Linje 23**: Check if buffer has content
  - Empty buffer → skip (nothing to flush)
  
- **Linje 24**: Join lines and trim
  - `['Hello', 'World']` → `'Hello\nWorld'`
  - `.trim()` removes leading/trailing whitespace
  
- **Linje 25**: Push if non-empty after trim
  - Prevents empty text blocks
  - `{type: 'text', content: 'Hello\nWorld'}`
  
- **Linje 26**: Clear buffer for next block
  - `textBuffer = []` (fresh start)

### flushCode() Helper (Linje 30-36)
```javascript
function flushCode() {
    if (codeLines.length) {
        blocks.push({type: 'code', language: lang || 'plaintext', content: codeLines.join('\n')});
        codeLines = [];
        lang = 'plaintext';
    }
}
```

#### Purpose
- **Finalize code block** - Move from buffer to blocks array
- **Called when**: Closing fence encountered or end of message

#### Logic Breakdown
- **Linje 31**: Check if buffer has code
  
- **Linje 32**: Create code block object
  - `type: 'code'` - Tells message-handler.js to use code block UI
  - `language: lang || 'plaintext'` - Fallback if lang empty
  - `content: codeLines.join('\n')` - Preserve line breaks
  
- **Linje 33-34**: Reset state
  - `codeLines = []` - Clear buffer
  - `lang = 'plaintext'` - Reset language (for next block)

### Main Parsing Loop (Linje 38-57)

#### Loop Structure (Linje 38)
```javascript
for (let i = 0; i < lines.length; i++) {
```
- **Iterate over lines** - Process one by one
- **Index access** - Allows line number tracking (debugging)

#### Get Current Line (Linje 39)
```javascript
const line = lines[i];
```
- **Each iteration** - One line of text

#### Fence Detection (Linje 40)
```javascript
const fenceMatch = line.match(/^\s*```\s*(.*)$/);
```

##### Regex Breakdown: `/^\s*```\s*(.*)$/`
- **`^`** - Start of line (anchor)
  - **Critical**: Only matches fences at line start
  - Ignores ` ``` ` in middle of text

- **`\s*`** - Optional leading whitespace
  - Allows indented fences (markdown spec)
  - `   ``` python` still matches

- **` ``` `** - Three backticks (literal)
  - Markdown code fence delimiter

- **`\s*`** - Optional space after backticks
  - ` ```python` or ` ``` python` both work

- **`(.*)`** - Capture group 1: language identifier
  - **Greedy**: Captures to end of line
  - Examples:
    - ` ```python` → capture: `'python'`
    - ` ```javascript with comments` → capture: `'javascript with comments'`
    - ` ``` ` → capture: `''` (empty)

- **`$`** - End of line (anchor)
  - Ensures fence is complete line
  - ` ```python # code` would NOT match

##### Match Result
- **If match**: `fenceMatch` is array
  - `fenceMatch[0]` - Full match: `'   ```python'`
  - `fenceMatch[1]` - Capture group: `'python'`
  
- **If no match**: `fenceMatch` is `null`

#### Opening Fence (Linje 42-47)
```javascript
if (fenceMatch) {
    if (!inCode) {
        // opening fence
        flushText();
        lang = (fenceMatch[1] || '').trim();
        inCode = true;
```

- **Linje 43**: Check if NOT in code
  - `!inCode` - Currently parsing text

- **Linje 45**: Finalize previous text block
  - Anything before ` ``` ` becomes text block

- **Linje 46**: Extract language
  - `fenceMatch[1]` - Capture group (language identifier)
  - `|| ''` - Fallback to empty string if undefined
  - `.trim()` - Remove whitespace: `' python '` → `'python'`
  
- **Linje 47**: Enter code state
  - Next lines will go to `codeLines` buffer

**Example:**
```markdown
This is text.
```python      ← Opening fence detected here
print("hello")
```

State change: inCode = false → true, lang = 'python'
```

#### Closing Fence (Linje 48-52)
```javascript
    } else {
        // closing fence
        flushCode();
        inCode = false;
    }
    continue;
```

- **Linje 48**: `else` - Already in code (`inCode === true`)
  - Same fence pattern, different context

- **Linje 50**: Finalize code block
  - All accumulated `codeLines` → blocks array

- **Linje 51**: Exit code state
  - Next lines will go to `textBuffer`

- **Linje 53**: Skip to next line
  - **Don't add fence line itself** to any buffer
  - Fence is metadata, not content

**Example:**
```python
print("hello")  ← In code buffer
```             ← Closing fence detected here
More text.      ← Back to text buffer

State change: inCode = true → false
```

#### Accumulate Code (Linje 54-56)
```javascript
if (inCode) {
    codeLines.push(line);
```
- **If in code state** - Add line to code buffer
- **Includes**: Empty lines, indented lines, everything between fences
- **No trimming** - Preserve exact formatting

#### Accumulate Text (Linje 57-59)
```javascript
} else {
    textBuffer.push(line);
}
```
- **If in text state** - Add line to text buffer
- **Includes**: Paragraphs, markdown (*, #, etc.)
- **Trimmed later** - When flushed

### Final Flush (Linje 62-68)
```javascript
// Flush any remaining content
if (inCode) {
    // Unclosed code fence: treat remaining as code
    flushCode();
} else {
    flushText();
}
```

#### Handle Unclosed Fence (Linje 62-65)
```javascript
if (inCode) {
    flushCode();
}
```
- **Scenario**: AI forgot closing fence
  ```markdown
  Here's the code:
  ```python
  print("hello")
  # No closing ``` ← Unclosed fence
  ```

- **Behavior**: Treat rest as code block
  - **Graceful**: Doesn't crash or lose content
  - **Reasonable**: User can see code (even if malformed)

#### Handle Remaining Text (Linje 66-68)
```javascript
} else {
    flushText();
}
```
- **Scenario**: Text after last code block
  ```markdown
  ```python
  print("hello")
  ```
  This is more explanation.  ← Remaining text
  ```

- **Behavior**: Create final text block

### Return (Linje 70)
```javascript
return blocks;
```
- **Array of block objects** - Ready for rendering
- **Structured data** - Easy to process in message-handler.js

---

## State Machine Diagram

### States:
```
┌──────────┐         ┌──────────┐
│   TEXT   │ ←──────→│   CODE   │
└──────────┘         └──────────┘
    │   ↑               │   ↑
    │   └───────────────┘   │
    │     ``` fence         │
    │                       │
    └───────────────────────┘
        End of input
```

### State Transitions:
```
Start → TEXT state
  ↓
Encounter ``` fence → Flush text, enter CODE state
  ↓
Encounter ``` fence → Flush code, enter TEXT state
  ↓
End of input → Flush remaining buffer
  ↓
Return blocks array
```

---

## Parsing Example

### Input:
```markdown
This is an introduction.

```python
def hello():
    print("world")
```

And here's some more text.
```

### Execution Trace:

#### Line 0: "This is an introduction."
- `inCode = false`
- No fence match
- `textBuffer.push("This is an introduction.")`
- State: `textBuffer = ["This is an introduction."]`

#### Line 1: "" (empty)
- `inCode = false`
- No fence match
- `textBuffer.push("")`
- State: `textBuffer = ["This is an introduction.", ""]`

#### Line 2: "```python"
- `fenceMatch = ["```python", "python"]`
- `!inCode` is `true`
- Call `flushText()`:
  - Join: `"This is an introduction.\n"`
  - Trim and push to blocks
  - Clear buffer
- Extract language: `lang = "python"`
- `inCode = true`
- `continue` (skip line)
- State: `blocks = [{type: 'text', content: 'This is an introduction.'}]`

#### Line 3: "def hello():"
- `inCode = true`
- No fence match
- `codeLines.push("def hello():")`
- State: `codeLines = ["def hello():"]`

#### Line 4: "    print(\"world\")"
- `inCode = true`
- No fence match
- `codeLines.push("    print(\"world\")")`
- State: `codeLines = ["def hello():", "    print(\"world\")"]`

#### Line 5: "```"
- `fenceMatch = ["```", ""]`
- `inCode` is `true` (else branch)
- Call `flushCode()`:
  - Join: `"def hello():\n    print(\"world\")"`
  - Push to blocks
  - Clear buffer
- `inCode = false`
- `continue` (skip line)
- State: `blocks = [..., {type: 'code', language: 'python', content: 'def hello():\n    print("world")'}]`

#### Line 6: "" (empty)
- `inCode = false`
- No fence match
- `textBuffer.push("")`
- State: `textBuffer = [""]`

#### Line 7: "And here's some more text."
- `inCode = false`
- No fence match
- `textBuffer.push("And here's some more text.")`
- State: `textBuffer = ["", "And here's some more text."]`

#### End of input:
- `inCode = false` (else branch)
- Call `flushText()`:
  - Join: `"\nAnd here's some more text."`
  - Trim: `"And here's some more text."`
  - Push to blocks
- Return `blocks`

### Output:
```javascript
[
    {type: 'text', content: 'This is an introduction.'},
    {type: 'code', language: 'python', content: 'def hello():\n    print("world")'},
    {type: 'text', content: "And here's some more text."}
]
```

---

## Edge Cases

### Case 1: Unclosed Code Fence
**Input:**
```markdown
Text here.
```python
print("hello")
```

**Behavior:**
- `inCode = true` at end of input
- `flushCode()` called in final flush
- All code after opening fence becomes one block

**Output:**
```javascript
[
    {type: 'text', content: 'Text here.'},
    {type: 'code', language: 'python', content: 'print("hello")'}
]
```

### Case 2: Fence in Middle of Line (Ignored)
**Input:**
```markdown
This is text with ``` in the middle.
```

**Behavior:**
- Regex requires `^` (line start)
- Middle ``` doesn't match
- Treated as regular text

**Output:**
```javascript
[
    {type: 'text', content: 'This is text with ``` in the middle.'}
]
```

### Case 3: Empty Code Block
**Input:**
```markdown
```python
```
```

**Behavior:**
- Opening fence: `inCode = true`, `lang = 'python'`
- Closing fence: `codeLines = []` (empty)
- `flushCode()` checks `if (codeLines.length)` → `false`
- **No code block added** (empty)

**Output:**
```javascript
[] // Empty array (no blocks)
```

### Case 4: No Language Specified
**Input:**
```markdown
```
print("hello")
```
```

**Behavior:**
- `fenceMatch[1] = ""` (empty capture)
- `(fenceMatch[1] || '').trim()` → `""`
- `lang || 'plaintext'` in flushCode → `'plaintext'`

**Output:**
```javascript
[
    {type: 'code', language: 'plaintext', content: 'print("hello")'}
]
```

### Case 5: Nested Fences (Not Supported in Markdown)
**Input:**
```markdown
```python
def outer():
    ```python
    def inner():
        pass
    ```
```
```

**Behavior:**
- First ` ``` ` opens code block
- Second ` ``` ` **closes** it (no nesting in state machine)
- Third ` ``` ` opens new block
- Fourth ` ``` ` closes it

**Output:**
```javascript
[
    {type: 'code', language: 'python', content: 'def outer():\n    '},
    {type: 'text', content: 'def inner():\n        pass'},
    {type: 'code', language: 'plaintext', content: ''}
]
```
*Not ideal, but markdown doesn't support nested fences anyway*

---

## Integration with message-handler.js

### Usage in appendMessage()
```javascript
// message-handler.js (approx line 16-22)
const blocks = parseMessage(msg.text);
blocks.forEach(block => {
    if (block.type === 'text') {
        // Create text element
    } else if (block.type === 'code') {
        // Create code block with language: block.language
    }
});
```

### Data Flow:
```
AI response:
"Here's the code:\n```python\nprint('hello')\n```\nThat's it!"
    ↓
parseMessage(text)
    ↓
[
    {type: 'text', content: "Here's the code:"},
    {type: 'code', language: 'python', content: "print('hello')"},
    {type: 'text', content: "That's it!"}
]
    ↓
message-handler.js loops and renders each block
    ↓
DOM: <div class="message">
       <span>Here's the code:</span>
       <div class="codeblock">...</div>
       <span>That's it!</span>
     </div>
```

---

## Security Considerations

### XSS Prevention
- **escapeHtml()** neutralizes HTML injection
- **Used on**: Text blocks only (code uses `<pre>` which is safe)
- **Attack vectors blocked**:
  - Script injection: `<script>alert(1)</script>`
  - Event handlers: `<img onerror=alert(1)>`
  - Attribute breaking: `" onload=alert(1) "`

### innerHTML vs textContent
- **Text blocks**: Use `escapeHtml()` then `innerHTML`
  - Allows Markdown rendering (if added later)
- **Code blocks**: Use `textContent` (safer)
  - Preserves exact formatting
  - No interpretation of HTML

---

## Performance

### Time Complexity
- **parseMessage()**: O(n) where n = number of lines
  - Single pass through lines
  - No backtracking or nested loops

### Space Complexity
- **O(n)** for blocks array and buffers
- **No memory leaks** - buffers cleared after flush

### Optimization Opportunities
- **Minimal**: Already very efficient
- **Possible**: Regex compilation caching (negligible gain)

---

## Browser Compatibility

### String.prototype.replace()
- **IE 5.5+**, **All modern browsers**
- **Global flag**: `/g` supported everywhere

### String.prototype.match()
- **IE 4+**, **All modern browsers**
- **Regex features**: Basic regex syntax (widely supported)

### Array methods
- **forEach, push, join**: ES3 (IE 5.5+)
- **Universal support**

---

## Testing Scenarios

### Test 1: Simple Text
```javascript
parseMessage("Hello world")
→ [{type: 'text', content: 'Hello world'}]
```

### Test 2: Single Code Block
```javascript
parseMessage("```python\nprint('hi')\n```")
→ [{type: 'code', language: 'python', content: "print('hi')"}]
```

### Test 3: Mixed Content
```javascript
parseMessage("Text\n```js\ncode\n```\nMore text")
→ [
    {type: 'text', content: 'Text'},
    {type: 'code', language: 'js', content: 'code'},
    {type: 'text', content: 'More text'}
]
```

### Test 4: XSS Attempt
```javascript
escapeHtml("<script>alert('XSS')</script>")
→ "&lt;script&gt;alert(&#039;XSS&#039;)&lt;/script&gt;"
```

---

## Konklusion

`message-parser.js` provides robust markdown parsing:
- **State machine** - Handles complex fence patterns
- **Security first** - XSS prevention built-in
- **Edge case handling** - Unclosed fences, empty blocks
- **Pure functions** - Easy to test and reason about
- **Efficient** - O(n) single-pass parsing

**Key design decisions:**
- Line-start fence matching (prevents false positives)
- Separate text/code buffers (clear state management)
- Flush helpers (DRY principle)
- Graceful unclosed fence handling (don't crash)
- Language fallback to 'plaintext' (always valid)

**File size**: 71 lines of critical parsing logic.
