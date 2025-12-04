# code-detector.js - Detaljeret Dokumentation

## Overordnet Formål
`code-detector.js` indeholder utility functions til at detecte og identificere programming languages i tekst. Den bruges til:
- Auto-detection af sprog når AI ikke specificerer (eller fejl-labeler)
- Mapping af language names til Prism.js syntax highlighter names
- Special handling af Cisco IOS config (ofte mislabeled som bash/plaintext)

**Fil størrelse**: 108 linjer
**Dependencies**: Bruges af message-handler.js og message-parser.js
**Exports**: 5 functions (alle global scope)

---

## Function 1: normalizeNewlines() (Linje 3-5)

### Function Signature
```javascript
function normalizeNewlines(src) {
    return src.replace(/\r\n?/g, "\n");
}
```

### Purpose
Konverterer Windows/Mac line endings til Unix format.

### Parameters
- **src** (String) - Input text med mixed line endings

### Return Value
- **String** - Text med normalized `\n` endings

### Line-by-Line Explanation
- **Linje 4**: **Regex replacement**
  - `/\r\n?/g` - Regular expression pattern
    - `\r` - Carriage return (Mac/Windows)
    - `\n?` - Optional linefeed (Windows har `\r\n`, Mac kun `\r`)
    - `g` - Global flag (replace ALL occurrences, not just first)
  - Replace with `"\n"` - Unix standard (LF only)

### Use Cases
```javascript
// Windows CRLF:
normalizeNewlines("Hello\r\nWorld")  // → "Hello\nWorld"

// Old Mac CR:
normalizeNewlines("Hello\rWorld")    // → "Hello\nWorld"

// Unix LF (unchanged):
normalizeNewlines("Hello\nWorld")    // → "Hello\nWorld"
```

### Why Important?
- **Cross-platform compatibility** - Users kan paste text fra Windows, Mac, Linux
- **Consistent parsing** - Regex patterns expect `\n` only
- **Prevents bugs** - `\r` can cause invisible issues in text processing

---

## Function 2: getPrismLanguage() (Linje 7-31)

### Function Signature
```javascript
function getPrismLanguage(lang) {
    const map = {
        // ... language mappings
    };
    return map[lang.toLowerCase()] || 'plaintext';
}
```

### Purpose
Maps common language names og aliases til Prism.js language identifiers.

### Parameters
- **lang** (String) - Language name fra user/AI (kan være: `'python'`, `'py'`, `'Python'`, `''`, etc.)

### Return Value
- **String** - Prism-compatible language name (always lowercase)
- **Default**: `'plaintext'` hvis language ikke findes i map

### Language Mapping Object (Linje 8-28)
```javascript
const map = {
    html: 'markup',       // HTML → Prism's "markup" language
    xml: 'markup',        // XML også mapped til markup
    js: 'javascript',     // Common abbreviation
    py: 'python',         // Python abbreviation
    python: 'python',     // Full name (passthrough)
    cpp: 'cpp',          // C++
    c: 'c',              // C language
    java: 'java',        // Java
    css: 'css',          // CSS
    json: 'json',        // JSON data
    bash: 'bash',        // Bash shell
    sh: 'bash',          // Shell script → bash
    shell: 'bash',       // Generic shell → bash
    sql: 'sql',          // SQL database
    cisco: 'cisco',      // Custom Cisco IOS (prism-cisco.js)
    ios: 'cisco',        // Cisco IOS abbreviation
    plaintext: 'plaintext', // No highlighting
    text: 'plaintext',   // Generic text
    '': 'plaintext'      // Empty string default
};
```

### Lookup Logic (Linje 29)
```javascript
return map[lang.toLowerCase()] || 'plaintext';
```
- **Linje 29**: Chained operations
  1. `lang.toLowerCase()` - Convert til lowercase (`'Python'` → `'python'`)
  2. `map[...]` - Dictionary lookup
  3. `|| 'plaintext'` - Fallback hvis key not found

### Examples
```javascript
getPrismLanguage('Python')      // → 'python'
getPrismLanguage('py')          // → 'python'
getPrismLanguage('javascript')  // → 'javascript'
getPrismLanguage('js')          // → 'javascript'
getPrismLanguage('HTML')        // → 'markup'
getPrismLanguage('cisco-ios')   // → 'plaintext' (not in map)
getPrismLanguage('')            // → 'plaintext'
getPrismLanguage('unknown')     // → 'plaintext'
```

### Why Mapping Needed?
1. **Prism naming conventions** - HTML er "markup", ikke "html"
2. **Abbreviations** - Users skriver "py", "js", "cpp"
3. **Case insensitivity** - "Python" vs "python" vs "PYTHON"
4. **Empty/unknown handling** - Graceful fallback til plaintext

---

## Function 3: detectCiscoConfig() (Linje 33-50)

### Function Signature
```javascript
function detectCiscoConfig(value) {
```

### Purpose
Detecterer om text er Cisco IOS configuration (router/switch commands).

### Parameters
- **value** (String) - Text content to analyze

### Return Value
- **Boolean** - `true` if Cisco config detected, `false` otherwise

### Detection Strategy
Tre-lags check: **Prompt** OR (**Commands** AND **Keywords**)

#### Layer 1: Prompt Detection (Linje 36)
```javascript
const hasPrompt = value.match(/^[\w.-]+[#>]\s/m);
```
- **Regex**: `/^[\w.-]+[#>]\s/m`
  - `^` - Start of line (multiline mode: `m` flag)
  - `[\w.-]+` - One or more word chars, dots, hyphens
    - Matches hostname: `Router`, `SW-Core-01`, `R1.lab`
  - `[#>]` - Either `#` (privileged mode) eller `>` (user mode)
  - `\s` - Whitespace after prompt
  - **Examples:**
    - `Router#` ✓
    - `Switch>` ✓
    - `R1-Core.lab#` ✓
    - `# comment` ✗ (no hostname før #)

#### Layer 2: Config Commands (Linje 37)
```javascript
const hasConfigCommands = value.match(/^(interface|switchport|ip address|router|crypto|access-list|!\s|vlan|hostname|enable|line vty|line console)/m);
```
- **Regex**: Start of line commands
  - `^` - Line start (multiline)
  - `(interface|switchport|...)` - Alternation (OR)
  - **Commands:**
    - `interface` - Interface config mode
    - `switchport` - Switch port commands
    - `ip address` - IP assignment
    - `router` - Routing protocol
    - `crypto` - Encryption/VPN
    - `access-list` - ACL rules
    - `!\s` - Comment lines (Cisco standard)
    - `vlan` - VLAN config
    - `hostname` - Device name
    - `enable` - Enable password
    - `line vty` - Telnet/SSH lines
    - `line console` - Console access

#### Layer 3: Keyword Detection (Linje 40-47)
```javascript
const lowerValue = value.toLowerCase();
const hasCiscoKeywords = (
    lowerValue.includes('interface ') ||
    lowerValue.includes('switchport ') ||
    lowerValue.includes('ip address') ||
    lowerValue.includes('gigabitethernet') ||
    lowerValue.includes('fastethernet') ||
    (lowerValue.includes('vlan') && value.includes('!'))
);
```
- **Case-insensitive checks** med `toLowerCase()`
- **Keywords:**
  - `'interface '` - Trailing space (not "interface" as part of word)
  - `'switchport '` - Layer 2 commands
  - `'ip address'` - IP config
  - `'gigabitethernet'` - Modern interfaces (Gi0/0)
  - `'fastethernet'` - Legacy interfaces (Fa0/1)
  - `'vlan'` AND `'!'` - VLAN config with comments (both present)

#### Final Decision (Linje 49)
```javascript
return (hasPrompt && hasConfigCommands) || (hasConfigCommands && hasCiscoKeywords);
```
- **Logic**: `(A AND B) OR (B AND C)`
  - **Option 1**: Prompt + Commands (clear config output)
  - **Option 2**: Commands + Keywords (config without prompts)
- **Prevents false positives**:
  - Text mentioning "cisco" without actual config → false
  - Single line like "interface description" → false (needs multiple indicators)

### Examples

#### ✓ Detected as Cisco:
```
Router#show running-config
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 switchport mode access
!
```
- Has prompt: `Router#` ✓
- Has commands: `interface`, `ip address`, `switchport` ✓
- Has keywords: `gigabitethernet`, `interface `, `ip address` ✓

#### ✗ NOT Detected:
```
To configure Cisco, use the interface command
```
- No prompt ✗
- Has "interface" but not as command (not at line start) ✗
- Keyword match but no config structure ✗

---

## Function 4: detectLanguage() (Linje 52-87)

### Function Signature
```javascript
function detectLanguage(value) {
```

### Purpose
Auto-detect programming language from code content. Returns `null` if plain text (not code).

### Parameters
- **value** (String) - Text content to analyze

### Return Value
- **String** - Language name (`'cisco'`, `'python'`, `'html'`, `'css'`, `'sql'`) or `null`
- **null** - Indicates plain text, NOT code

### Detection Flow

#### Step 1: Initialize (Linje 54)
```javascript
let detectedLang = null; // null = not code, just text
```
- **null default** - Assume plain text unless proven otherwise
- **Why null?** Distinguishes between "unknown code" and "not code"

#### Step 2: Code Fence Check (Linje 56-57)
```javascript
const hasCodeFence = /^\s*```/m.test(value);
```
- **Regex**: `/^\s*```/m`
  - `^` - Start of line (multiline: `m`)
  - `\s*` - Optional whitespace (indentation)
  - ` ``` ` - Triple backticks (markdown code fence)
  - `.test()` - Returns boolean (true/false)
- **Purpose**: Check if user explicitly marked as code block

#### Step 3: Parse Explicit Code Fence (Linje 59-64)
```javascript
if (hasCodeFence) {
    const blocks = parseMessage(value);
    if (blocks.length > 0 && blocks[0].type === 'code') {
        detectedLang = blocks[0].language || 'javascript';
    }
}
```
- **Linje 60**: Call `parseMessage()` fra message-parser.js
  - Parses markdown: ` ```python\ncode\n``` `
  - Returns: `[{type: 'code', language: 'python', content: 'code'}]`
  
- **Linje 61**: Check if first block is code
  - `blocks.length > 0` - Array not empty
  - `blocks[0].type === 'code'` - First block is code (not text)
  
- **Linje 62**: Use parsed language or default to JavaScript
  - `blocks[0].language` - From ` ```python` → `'python'`
  - `|| 'javascript'` - Fallback if language not specified (` ``` ` without language)

#### Step 4: Auto-Detection (Linje 65-84)
```javascript
} else {
    const lowerValue = value.toLowerCase();
    
    if (detectCiscoConfig(value)) {
        detectedLang = 'cisco';
    }
    // ... other checks
}
```

**Detection Priority (most specific → least specific):**

##### 1. Cisco Config (Linje 68-70)
```javascript
if (detectCiscoConfig(value)) {
    detectedLang = 'cisco';
}
```
- **First priority** - Cisco ofte mislabeled
- Uses `detectCiscoConfig()` function

##### 2. HTML (Linje 72-74)
```javascript
else if (lowerValue.includes('<!doctype') || lowerValue.includes('<html') || 
         lowerValue.includes('<head') || lowerValue.includes('</html>')) {
    detectedLang = 'html';
}
```
- **Very specific tags** - unmistakable HTML markers
- Case-insensitive: `<!DOCTYPE>` or `<!doctype>`

##### 3. CSS (Linje 75-76)
```javascript
else if (value.match(/[#\.]\w+\s*\{/) || 
         (value.includes('{') && value.includes('}') && value.includes(':') && 
          value.includes(';') && value.split('\n').length > 2)) {
    detectedLang = 'css';
}
```
- **Linje 75**: **Regex for selectors**
  - `/[#\.]\w+\s*\{/` - Matches `#id {` or `.class {`
  - `[#\.]` - Hash or dot (ID/class selector)
  - `\w+` - Selector name
  - `\s*` - Optional whitespace
  - `\{` - Opening brace

- **Linje 76**: **Multi-rule heuristic**
  - Has `{` and `}` - CSS blocks
  - Has `:` and `;` - CSS property syntax
  - More than 2 lines - Not just inline style

##### 4. Python (Linje 77-78)
```javascript
else if ((value.includes('def ') && value.includes(':')) || 
         (value.includes('import ') && !value.includes('import {')) || 
         value.includes('print(') || value.includes('self.')) {
    detectedLang = 'python';
}
```
- **Multiple Python indicators:**
  - `def ` + `:` - Function definition (`def foo():`)
  - `import ` without `{` - Python import (not JS `import { ... }`)
  - `print(` - Print function
  - `self.` - Class methods

##### 5. SQL (Linje 79-80)
```javascript
else if (value.includes('SELECT ') || value.includes('INSERT INTO') || 
         value.includes('CREATE TABLE')) {
    detectedLang = 'sql';
}
```
- **SQL keywords** - uppercase convention
- Common commands: SELECT, INSERT, CREATE

#### Step 5: Return (Linje 83)
```javascript
return detectedLang;
```
- Returns detected language string or `null`

### Detection Examples

#### Example 1: Explicit Fence
```javascript
detectLanguage(`
\`\`\`python
def hello():
    print("Hi")
\`\`\`
`)
// → 'python' (from parseMessage)
```

#### Example 2: Cisco Auto-Detect
```javascript
detectLanguage(`
Router#show run
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
!
`)
// → 'cisco' (detectCiscoConfig returns true)
```

#### Example 3: Python Auto-Detect
```javascript
detectLanguage(`
def calculate(x):
    return x * 2

print(calculate(5))
`)
// → 'python' (has 'def ' and ':')
```

#### Example 4: Plain Text
```javascript
detectLanguage(`
This is just a normal message
asking about configuration
`)
// → null (no code indicators)
```

---

## Function 5: detectCiscoInContent() (Linje 89-108)

### Function Signature
```javascript
function detectCiscoInContent(content) {
```

### Purpose
Specialized Cisco detection FOR CODE BLOCKS that already exist but might be mislabeled. Used in `message-handler.js` to override AI's language label.

### Parameters
- **content** (String) - Code block content (NOT full message)

### Return Value
- **String** - `'cisco'` if detected, `null` otherwise

### Difference from detectCiscoConfig()
- **detectCiscoConfig()** - Used for **user input** (full message text)
- **detectCiscoInContent()** - Used for **existing code blocks** (AI response already parsed)

### Detection Logic (Linje 92-102)
```javascript
const lowerContent = content.toLowerCase();

if (lowerContent.match(/^[\w.-]+[#>]/m) || 
    lowerContent.includes('interface ') || 
    lowerContent.includes('switchport ') ||
    lowerContent.includes('ip address') ||
    lowerContent.includes('gigabitethernet') ||
    lowerContent.includes('fastethernet') ||
    lowerContent.includes('ethernet') ||
    (lowerContent.includes('vlan') && content.includes('!'))) {
    return 'cisco';
}

return null;
```

**Conditions (ANY match → cisco):**
1. **Prompt pattern**: `Router#`, `Switch>`
2. **Keywords**: `interface `, `switchport `, `ip address`
3. **Interface names**: `gigabitethernet`, `fastethernet`, `ethernet`
4. **VLAN with comments**: Both `vlan` AND `!` present

### Why More Aggressive?
- **AI often mislabels** Cisco as `bash`, `shell`, `plaintext`, `text`
- **Comment syntax**: Cisco uses `!` like bash uses `#`
- **Already in code block** - safe to override
- **Single keyword enough** - Don't need multiple indicators like detectCiscoConfig()

### Usage in message-handler.js
```javascript
// In appendMessage() for bot code:
let detectedLang = block.language || '';

if (!detectedLang || detectedLang === 'plaintext' || 
    detectedLang === 'bash' || detectedLang === 'shell') {
    const ciscoDetected = detectCiscoInContent(block.content);
    if (ciscoDetected) {
        detectedLang = ciscoDetected; // Override to 'cisco'
    }
}
```

### Example Override
```javascript
// AI labeled this as bash:
const block = {
    type: 'code',
    language: 'bash',  // WRONG
    content: `
interface GigabitEthernet0/0
 ip address 192.168.1.1 255.255.255.0
 switchport mode access
!
    `
};

detectCiscoInContent(block.content);
// → 'cisco'  (overrides 'bash' label)
```

---

## Function Dependencies

### Call Graph
```
message-handler.js
    ├─ appendMessage()
    │   ├─ getPrismLanguage() ✓
    │   └─ detectCiscoInContent() ✓
    │
    ├─ sendMessage()
    │   └─ detectLanguage() ✓
    │
    └─ addPastedCode()
        └─ getPrismLanguage() ✓

message-parser.js
    └─ parseMessage()
        └─ normalizeNewlines() ✓
```

---

## Design Patterns

### 1. Dictionary Mapping Pattern
```javascript
const map = { key: 'value' };
return map[input] || 'default';
```
- **Fast O(1) lookup**
- **Fallback handling** with `||`
- Used in: `getPrismLanguage()`

### 2. Multi-Layer Detection
```javascript
if (strongIndicator) return true;
if (mediumIndicator && supportingEvidence) return true;
return false;
```
- **Priority-based** - Check specific patterns first
- **Combined evidence** - Require multiple weak signals
- Used in: `detectCiscoConfig()`, `detectLanguage()`

### 3. Null vs Default Pattern
```javascript
let result = null;  // null = not detected
// ... detection logic
return result;  // Can be null or string
```
- **Tri-state logic**: `null` (not code), `'language'` (detected), `'plaintext'` (code but unknown)
- Used in: `detectLanguage()`

---

## Performance Considerations

### Regex Efficiency
- **Multiline flag `m`** - Checks each line start (not entire string)
- **Early exit** - Returns on first match
- **Simple patterns** - No backtracking

### String Operations
- **`toLowerCase()` once** - Cached in variable, reused
- **`includes()` over regex** - Faster for simple substring checks
- **Short-circuit OR** - Stops at first true condition

---

## Security Notes

### No Code Execution
- **Pure detection** - No `eval()` or code execution
- **Safe patterns** - Regex doesn't allow injection
- **Read-only** - Doesn't modify input

### XSS Prevention
- **Returns language name** - Not HTML/JavaScript code
- **Used for CSS classes** - Sanitized by Prism

---

## Testing Scenarios

### Edge Cases
1. **Empty string**: `getPrismLanguage('')` → `'plaintext'`
2. **Mixed content**: "Here's some cisco: `Router#`" → depends on context
3. **Ambiguous**: `!comment` could be bash or cisco → needs more context
4. **Case variations**: `PYTHON`, `Python`, `python` → all work

### False Positives
- **Cisco description text** - Not actual config → detectCiscoConfig() returns false
- **Python in prose** - "use def to define" → needs `def ` with space

### False Negatives
- **Incomplete config** - Single line → might not detect
- **Uncommon languages** - Rust, Go, etc. → fallback to plaintext

---

## Konklusion

`code-detector.js` er en kritisk utility library for:
- **Language identification** - Auto-detect når AI fejler eller bruger ikke specificerer
- **Cisco special handling** - Kompenserer for hyppig AI mislabeling
- **Prism integration** - Mapper sprog til highlighter-kompatible navne

**Key strengths:**
- Multi-layer detection (prompt + commands + keywords)
- Aggressive Cisco override (fixes AI errors)
- Fast dictionary lookups
- Graceful fallbacks

**File size**: 108 lines of essential detection logic.
