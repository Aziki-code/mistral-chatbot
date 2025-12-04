# base.css - Detaljeret Dokumentation

## Overordnet Formål
`base.css` er CSS fundamentet for hele chatbotten. Den:
- Definerer layout structure (3-panel design)
- Sætter default CSS variables (theme colors)
- Styler alle UI components (messages, code blocks, input)
- Opretter animations (fadeIn, ripple effects)
- Konfigurerer scrollbars, buttons, watermark

**Fil størrelse**: 476 linjer
**Pattern**: Theme-agnostic base styles
**Variables**: CSS custom properties (--bg-darkest, --text-primary, etc.)
**Layout**: Flexbox + absolute positioning

---

## CSS Reset (Linje 3-7)

### Universal Selector
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```

#### Purpose
- **Reset browser defaults** - Removes margin/padding from all elements
- **Consistent box model** - `border-box` includes padding/border in width

#### box-sizing Explained
```css
/* content-box (default): */
width: 300px + padding: 20px + border: 2px = 322px total

/* border-box: */
width: 300px (includes padding + border) = 300px total
```
- **Better for layout** - Easier to calculate widths
- **Predictable** - Width stays as specified

---

## CSS Variables (:root) (Linje 9-23)

### Root Declaration
```css
:root {
    /* Default colors (Cisco theme) */
```
- **:root** - Highest level selector (equivalent to `<html>`)
- **CSS variables** - Can be overridden by themes
- **Global scope** - Accessible everywhere with `var(--variable-name)`

### Variable Categories

#### Background Colors (Linje 10-12)
```css
--bg-darkest: #505050;  /* Body background, darkest shade */
--bg-dark: #505050;     /* Input fields, secondary areas */
--bg-medium: #585858;   /* Headers, buttons */
```
- **Gray scale** - Cisco default theme
- **Darkest → Medium** - Hierarchy for layering

#### Border & Text (Linje 13-16)
```css
--border-color: #707070;      /* Panel borders, input borders */
--text-primary: #00ffff;      /* Main text (cyan) */
--text-secondary: #00d7ff;    /* Secondary text (lighter cyan) */
```
- **Cyan text** - Cisco Matrix-style theme
- **Gray borders** - Subtle separation

#### Accents (Linje 17-18)
```css
--accent-primary: #00ffff;    /* Highlights, active elements */
--accent-secondary: #00d7ff;  /* Secondary highlights */
```
- **Cyan accents** - Theme color
- **Used for**: Code blocks, borders, hover states

#### Buttons (Linje 19-21)
```css
--button-primary: #006b7a;          /* Send button, copy button */
--button-primary-hover: #008a9c;    /* Hover state (lighter) */
--button-secondary: #00ffff;        /* Upload button (bright cyan) */
```
- **Primary**: Dark cyan (less prominent)
- **Hover**: Lighter (visual feedback)
- **Secondary**: Bright cyan (stands out)

#### Scrollbar (Linje 22-23)
```css
--scrollbar-thumb: #707070;        /* Scrollbar handle */
--scrollbar-thumb-hover: #808080;  /* Hover state */
```
- **Custom scrollbar** - Matches theme
- **Gray tones** - Subtle, not distracting

---

## Body Styling (Linje 25-37)

### Base Body Rules
```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: var(--bg-darkest);
    color: var(--text-primary);
    margin: 0;
    padding: 0;
    display: flex;
    justify-content: center;
    height: 100vh;
    overflow: hidden;
    position: relative;
}
```

#### Font Family (Linje 26)
- **Segoe UI** - Windows default (clean, modern)
- **Fallbacks**: Tahoma → Geneva → Verdana → sans-serif
- **Cross-platform** - Works on all OS

#### Background & Color (Linje 27-28)
- **var(--bg-darkest)** - Uses CSS variable (theme-dependent)
- **var(--text-primary)** - Cyan text by default

#### Flexbox Centering (Linje 31-32)
```css
display: flex;
justify-content: center;
```
- **Horizontal centering** - Centers `#chat-container` (800px)
- **Why?** Main chat panel centered in viewport

#### Height (Linje 33)
```css
height: 100vh;
```
- **100vh** - 100% of viewport height
- **Full screen** - No scrolling on body (chat scrolls internally)

#### Overflow (Linje 34)
```css
overflow: hidden;
```
- **Prevents body scroll** - Only chat div scrolls
- **Fixed layout** - No page bounce

#### Position (Linje 35)
```css
position: relative;
```
- **Creates stacking context** - For `::before` watermark (z-index 1)

---

## Theme Imports (Linje 39-40)

```css
@import url('themes/light-theme.css');
@import url('themes/light-quiet-theme.css');
```
- **Why here?** Light themes need to override base styles
- **Order matters** - Loaded after base, before main theme selectors
- **Conditional** - Only apply when `body.light-theme` class added

---

## Watermark (body::before) (Linje 42-58)

### Pseudo-Element
```css
body::before {
    content: '';
```
- **::before** - Inserts content before body's content
- **Empty content** - Just for background image

### Positioning (Linje 44-48)
```css
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;
```
- **Fixed** - Stays in viewport (doesn't scroll)
- **Full coverage** - Entire screen

### Background Image (Linje 49-52)
```css
background-image: url('/static/images/kali-layers.png');
background-size: cover;
background-position: center;
background-repeat: no-repeat;
```
- **Kali Linux dragon** - Brand image
- **cover** - Scales to fill, maintains aspect ratio
- **center** - Centered positioning
- **no-repeat** - Single image, no tiling

### Opacity (Linje 53)
```css
opacity: 0.4;
```
- **40% visible** - Subtle, not distracting
- **Watermark effect** - Background decoration

### Z-Index (Linje 54)
```css
z-index: 1;
```
- **Behind content** - `#chat-container` is z-index 10
- **Layering**: Watermark (1) → Content (10)

### Filters (Linje 55)
```css
filter: grayscale(100%) brightness(0.8) contrast(1.2);
```
- **grayscale(100%)** - Remove all color (black & white)
- **brightness(0.8)** - Darker (80% original)
- **contrast(1.2)** - More contrast (120%)
- **Result**: Subdued, professional look

### Pointer Events (Linje 56)
```css
pointer-events: none;
```
- **Can't click** - Mouse passes through to content below
- **No interaction** - Pure decoration

---

## Theme Selector (Linje 60-92)

### Container (Linje 60-66)
```css
#theme-selector {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1000;
    display: flex;
    gap: 10px;
    align-items: center;
}
```
- **Absolute positioning** - Top-right corner
- **z-index 1000** - Above everything
- **Flexbox** - Horizontal layout (label + dropdown + logout)
- **gap: 10px** - Space between items

### Dropdown (Linje 68-81)
```css
#theme-selector select {
    padding: 8px 12px;
    background: var(--bg-medium);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.2s ease;
}

#theme-selector select:hover {
    border-color: var(--accent-primary);
    background: var(--bg-dark);
}
```
- **Styled select** - Custom appearance (not browser default)
- **Hover effect** - Cyan border, darker background
- **Smooth transition** - 0.2s ease (gradual color change)

### Label (Linje 83-87)
```css
#theme-selector label {
    color: var(--text-primary);
    font-size: 14px;
    font-weight: 500;
}
```
- **"Theme:" label** - Medium font weight (500)
- **Theme color** - Matches text

### Logout Button (Linje 89-99)
```css
#logout-btn {
    padding: 8px 16px;
    background: var(--button-primary);
    color: white;
    text-decoration: none;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.2s ease;
    border: 1px solid transparent;
}

#logout-btn:hover {
    background: var(--button-primary-hover);
    border-color: var(--accent-primary);
}
```
- **Link styled as button** - `<a>` tag with button appearance
- **No underline** - `text-decoration: none`
- **Hover state** - Lighter background, cyan border

---

## Chat Container (Linje 101-106)

```css
#chat-container {
    display: flex;
    width: 100%;
    height: 100%;
    position: relative;
    z-index: 10;
}
```
- **Full viewport** - 100% width & height
- **Flexbox** - Contains three panels (input, left, right)
- **z-index 10** - Above watermark (z-index 1)
- **Relative** - Anchor point for absolute-positioned panels

---

## Input Panel (Left Side) (Linje 108-148)

### Container (Linje 108-130)
```css
#input-panel {
    position: absolute;
    right: calc(50% + 400px);
    top: 0;
    bottom: 0;
    left: 0;
    min-width: 300px;
    display: none;
    flex-direction: column;
    border-right: 2px solid var(--border-color);
    background: transparent;
    z-index: 50;
}
```

#### Positioning (Linje 109-113)
- **Absolute** - Positioned within `#chat-container`
- **right: calc(50% + 400px)** - Starts at left edge, ends at left border of chat panel
  - **50%** - Viewport center
  - **+400px** - Half width of chat panel (800px / 2)
  - **Result**: Left panel from left edge to chat panel
- **top/bottom: 0** - Full height
- **left: 0** - Starts at left edge

#### Layout (Linje 114-118)
- **min-width: 300px** - Minimum width (prevents too narrow)
- **display: none** - Hidden by default
- **flex-direction: column** - Vertical layout (header + content)

#### Visibility Toggle (Linje 132-134)
```css
#input-panel.visible {
    display: flex;
}
```
- **Class toggle** - JavaScript adds `.visible` when code detected
- **Shows panel** - `display: flex` makes visible

### Header (Linje 136-143)
```css
#pasted-code-header {
    padding: 10px;
    background: var(--bg-medium);
    border-bottom: 1px solid var(--border-color);
    font-weight: bold;
    color: var(--accent-primary);
    letter-spacing: 0.5px;
}
```
- **"Pasted Code" title** - Header for left panel
- **Cyan color** - Accent primary
- **Letter spacing** - Slightly wider for readability

### Content (Linje 145-152)
```css
#pasted-code-output {
    padding: 10px;
    overflow-x: hidden;
    overflow-y: auto;
    flex-grow: 1;
    font-size: 13px;
    background: transparent;
}
```
- **Scrollable** - Y-axis scroll, no X-axis scroll
- **flex-grow: 1** - Takes remaining space (after header)
- **13px font** - Smaller for code preview

---

## Left Panel (Chat Area) (Linje 154-177)

### Container (Linje 154-167)
```css
#left-panel {
    position: absolute;
    left: calc(50% - 400px);
    width: 800px;
    top: 0;
    bottom: 0;
    display: flex;
    flex-direction: column;
    border-left: 2px solid var(--border-color);
    border-right: 2px solid var(--border-color);
    background: transparent;
    z-index: 10;
}
```

#### Positioning (Linje 155-157)
- **left: calc(50% - 400px)** - Centers 800px panel
  - **50%** - Viewport center
  - **-400px** - Half width (800px / 2)
  - **Result**: Centered 800px panel
- **width: 800px** - Fixed width (main chat area)

#### Borders (Linje 161-162)
- **Both sides** - Left and right borders
- **2px solid** - Visible separation from side panels

### Chat Div (Linje 169-177)
```css
#chat {
    padding: 15px;
    overflow-x: hidden;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    background: transparent;
}
```
- **Scrollable area** - Messages scroll here
- **Flexbox column** - Messages stacked vertically
- **flex-grow: 1** - Takes space above input-container
- **Transparent** - Watermark visible through

---

## Right Panel (Code Output) (Linje 179-202)

### Container (Linje 179-191)
```css
#right-panel {
    position: absolute;
    left: calc(50% + 400px);
    top: 0;
    bottom: 0;
    right: 0;
    display: none;
    flex-direction: column;
    background: transparent;
    z-index: 10;
}
```

#### Positioning (Linje 180-184)
- **left: calc(50% + 400px)** - Starts after chat panel
  - **50%** - Viewport center
  - **+400px** - Half width of chat panel
  - **Result**: Right panel from chat border to right edge
- **right: 0** - Extends to right edge

#### Visibility (Linje 193-195)
```css
#right-panel.visible {
    display: flex;
}
```
- **Hidden by default** - Only shows when code block clicked

### Header (Linje 197-203)
```css
#code-output-header {
    padding: 10px;
    background: var(--bg-medium);
    border-bottom: 1px solid var(--border-color);
    font-weight: bold;
    color: var(--accent-primary);
    letter-spacing: 0.5px;
}
```
- **"Code Output" title** - Same style as pasted-code-header

### Content (Linje 205-211)
```css
#code-output {
    flex-grow: 1;
    padding: 15px;
    overflow: auto;
    background: transparent;
    font-size: 13px;
}
```
- **Scrollable** - Both X and Y axis (for wide code)
- **Takes remaining space** - After header

---

## Message Bubbles (Linje 213-242)

### Base Message (Linje 213-222)
```css
.message {
    margin-bottom: 15px;
    padding: 12px;
    border-radius: 8px;
    max-width: 80%;
    word-wrap: break-word;
    animation: fadeIn 0.3s ease-in;
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.03);
}
```

#### Layout (Linje 214-217)
- **margin-bottom: 15px** - Space between messages
- **padding: 12px** - Inner spacing
- **border-radius: 8px** - Rounded corners
- **max-width: 80%** - Doesn't stretch full width (chat bubble style)

#### Text (Linje 218)
```css
word-wrap: break-word;
```
- **Break long words** - Prevents horizontal overflow
- **URLs, code** - Won't break layout

#### Animation (Linje 219)
```css
animation: fadeIn 0.3s ease-in;
```
- **Fade in on appear** - Smooth entrance (defined linje 224-227)

#### Subtle Styling (Linje 220-221)
- **Semi-transparent border** - `rgba(255, 255, 255, 0.1)` (10% white)
- **Very subtle background** - `rgba(255, 255, 255, 0.03)` (3% white)

### FadeIn Animation (Linje 224-227)
```css
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
```
- **0%**: Invisible, 10px below final position
- **100%**: Fully visible, at final position
- **Effect**: Slides up while fading in

### User Message (Linje 229-235)
```css
.message.user {
    background: rgba(var(--accent-primary-rgb, 0, 255, 255), 0.1);
    border-left: 3px solid var(--accent-primary);
    margin-left: auto;
    text-align: right;
    color: var(--text-primary);
}
```

#### Background (Linje 230)
```css
background: rgba(var(--accent-primary-rgb, 0, 255, 255), 0.1);
```
- **RGB variable** - `--accent-primary-rgb` (if set)
- **Fallback**: `0, 255, 255` (cyan)
- **10% opacity** - Semi-transparent
- **Note**: Requires theme to set RGB values separately

#### Left Border (Linje 231)
- **3px thick** - Visual indicator
- **Accent color** - Cyan by default

#### Alignment (Linje 232-233)
- **margin-left: auto** - Pushes to right (flex property)
- **text-align: right** - Text aligned right

### Assistant Message (Linje 237-242)
```css
.message.assistant {
    background: rgba(255, 255, 255, 0.05);
    border-left: 3px solid var(--accent-secondary);
    margin-right: auto;
    text-align: left;
}
```
- **Left-aligned** - Opposite of user message
- **Different border color** - `--accent-secondary` (lighter cyan)
- **Semi-transparent white** - 5% white background

---

## Code Blocks (Linje 244-349)

### Codeblock Container (Linje 244-253)
```css
.codeblock {
    margin: 10px 0;
    border-radius: 6px;
    overflow: hidden;
    background: rgba(80, 80, 80, 0.5);
    border: 1px solid var(--border-color);
    border-left: 3px solid var(--accent-primary);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
    position: relative;
    z-index: 1;
}
```

#### Styling (Linje 245-247)
- **10px vertical margin** - Space above/below
- **border-radius: 6px** - Rounded corners
- **overflow: hidden** - Clips content to rounded border

#### Background (Linje 248)
```css
background: rgba(80, 80, 80, 0.5);
```
- **Gray with 50% opacity** - Semi-transparent
- **Watermark visible** - Through code block

#### Borders (Linje 249-250)
- **All sides**: 1px gray border
- **Left side**: 3px cyan accent (emphasis)

#### Shadow (Linje 251)
```css
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
```
- **Elevation effect** - Lifts off page
- **Subtle depth** - 30% black shadow

### Code Header (Linje 255-263)
```css
.code-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    background: var(--bg-medium);
    border-bottom: 1px solid var(--border-color);
}
```
- **Flexbox** - Language label on left, copy button on right
- **space-between** - Maximum space between items
- **Darker background** - Separates from code

### Language Label (Linje 265-271)
```css
.code-language {
    font-size: 12px;
    font-weight: 600;
    color: var(--accent-primary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
```
- **Small uppercase** - "PYTHON", "CISCO", "JAVASCRIPT"
- **Cyan color** - Accent primary
- **Bold** - 600 font weight
- **Spaced** - 0.5px letter spacing

### Copy Button (Linje 273-286)
```css
.copy-btn {
    padding: 4px 12px;
    background: var(--button-primary);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-size: 11px;
    font-weight: 600;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.copy-btn:hover {
    background: var(--button-primary-hover);
    transform: translateY(-1px);
}
```
- **Small button** - 11px font
- **Uppercase** - "COPY"
- **Hover lift** - `translateY(-1px)` moves up 1px
- **Color change** - Lighter on hover

### Copy Feedback (Linje 288-307)
```css
.copy-feedback {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: var(--accent-primary);
    color: var(--bg-darkest);
    padding: 12px 24px;
    border-radius: 6px;
    font-weight: 600;
    z-index: 1000;
    opacity: 0;
    pointer-events: none;
    transition: opacity 0.3s ease;
}

.copy-feedback.show {
    opacity: 1;
}
```

#### Positioning (Linje 289-292)
- **Absolute centering** - Middle of code block
- **transform: translate(-50%, -50%)** - Centers relative to own size

#### Styling (Linje 293-297)
- **Cyan background** - Bright accent color
- **Dark text** - High contrast
- **Bold** - 600 font weight

#### Visibility (Linje 298-301)
- **Hidden by default** - `opacity: 0`
- **No interaction** - `pointer-events: none`
- **Smooth fade** - `transition: opacity 0.3s ease`

#### Show State (Linje 303-305)
- **JavaScript adds .show** - When copy succeeds
- **Becomes visible** - `opacity: 1`

### FadeInOut Animation (Linje 309-312)
```css
@keyframes fadeInOut {
    0%, 100% { opacity: 0; }
    50% { opacity: 1; }
}
```
- **0%**: Invisible
- **50%**: Fully visible (midpoint)
- **100%**: Invisible again
- **Used for**: Notifications

### Pre Element (Linje 314-322)
```css
.codeblock pre {
    margin: 0;
    padding: 15px;
    overflow-x: auto;
    background: transparent;
    color: var(--text-primary);
    position: relative;
}
```
- **Contains code** - `<pre><code>...</code></pre>`
- **Scrollable** - Horizontal scroll for long lines
- **Transparent** - Code block background shows through

### Ripple Effect (Linje 324-337)
```css
@keyframes ripple {
    0% {
        box-shadow: 0 0 0 0 var(--accent-primary);
    }
    50% {
        box-shadow: 0 0 20px 10px var(--accent-primary);
    }
    100% {
        box-shadow: 0 0 0 0 var(--accent-primary);
    }
}

.codeblock.highlight {
    animation: ripple 1s ease-out;
    border-color: var(--accent-primary);
}
```

#### Animation Flow
- **0%**: No shadow
- **50%**: Large cyan glow (20px blur, 10px spread)
- **100%**: Shadow fades out
- **Duration**: 1 second

#### Trigger (Linje 339-342)
- **JavaScript adds .highlight** - When code indicator clicked
- **Draws attention** - To specific code block

### Code Element (Linje 344-348)
```css
.codeblock code {
    font-family: 'Courier New', Courier, monospace;
    font-size: 13px;
    line-height: 1.5;
}
```
- **Monospace font** - Fixed-width characters
- **13px** - Readable code size
- **1.5 line height** - Spacing between lines

---

## Screenshot Styling (Linje 350-357)

```css
.screenshot {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    margin: 10px 0;
    border: 2px solid var(--border-color);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}
```
- **Responsive** - Scales to fit container
- **Maintains aspect ratio** - `height: auto`
- **Rounded corners** - 8px radius
- **Border & shadow** - Matches code blocks

---

## Input Container (Linje 359-476)

### Container (Linje 359-363)
```css
#input-container {
    padding: 15px;
    background: var(--bg-medium);
    border-top: 2px solid var(--border-color);
}
```
- **Bottom of chat panel** - Fixed at bottom
- **Darker background** - Separates from chat
- **Top border** - Visual separation

### Input Row (Linje 365-368)
```css
#input-row {
    display: flex;
    gap: 10px;
    margin-bottom: 10px;
}
```
- **Flexbox** - Textarea + buttons horizontal
- **10px gap** - Space between elements

### Textarea (Linje 370-389)
```css
#input {
    flex-grow: 1;
    padding: 12px;
    background: var(--bg-dark);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    font-size: 14px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    resize: vertical;
    transition: border-color 0.2s ease;
}

#input:focus {
    outline: none;
    border-color: var(--accent-primary);
}

#input::placeholder {
    color: var(--text-secondary);
    opacity: 0.6;
}
```

#### Layout (Linje 371-378)
- **flex-grow: 1** - Takes available space (buttons fixed width)
- **resize: vertical** - User can drag to resize height (not width)

#### Focus State (Linje 382-385)
- **No outline** - Removes browser default
- **Cyan border** - Accent primary

#### Placeholder (Linje 387-390)
- **Secondary color** - Lighter cyan
- **60% opacity** - Very subtle

### Send Button (Linje 392-409)
```css
#send {
    padding: 12px 24px;
    background: var(--button-primary);
    color: white;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 600;
    transition: all 0.2s ease;
    white-space: nowrap;
}

#send:hover {
    background: var(--button-primary-hover);
    transform: translateY(-1px);
}
```
- **white-space: nowrap** - Text doesn't wrap ("Send" on one line)
- **Hover lift** - Moves up 1px

### Upload Input (Linje 411-413)
```css
#upload {
    display: none;
}
```
- **Hidden file input** - Browser file picker (triggered by uploadBtn)

### Upload Button (Linje 415-429)
```css
#uploadBtn {
    display: none;
    padding: 10px 20px;
    background: var(--button-secondary);
    color: var(--bg-darkest);
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
    font-weight: 600;
    transition: all 0.2s ease;
}

#uploadBtn:hover {
    opacity: 0.8;
    transform: translateY(-1px);
}
```
- **display: none** - Hidden by default (Mistral Vision feature)
- **Secondary button color** - Bright cyan
- **Dark text** - Contrast against bright background

---

## Custom Scrollbar (Linje 431-447)

### Webkit Scrollbar (Linje 431-447)
```css
::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: transparent;
}

::-webkit-scrollbar-thumb {
    background: var(--scrollbar-thumb);
    border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--scrollbar-thumb-hover);
}
```

#### Scrollbar Parts
- **::-webkit-scrollbar** - Overall scrollbar (10px wide)
- **::-webkit-scrollbar-track** - Background (transparent)
- **::-webkit-scrollbar-thumb** - Draggable handle (gray, rounded)

#### Browser Support
- **Chrome, Safari, Edge** - Full support
- **Firefox** - Doesn't support (uses default scrollbar)
- **Firefox alternative**: `scrollbar-color` and `scrollbar-width`

---

## Code Indicator (Linje 449-461)

```css
.code-indicator {
    display: inline-block;
    padding: 4px 8px;
    margin: 0 4px;
    background: var(--button-primary);
    color: white;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
}

.code-indicator:hover {
    background: var(--button-primary-hover);
    transform: translateY(-1px);
}
```
- **Inline block** - Flows with text
- **Small pill** - "Block #1", "Block #2"
- **Clickable** - Scrolls to code block
- **Hover lift** - Visual feedback

---

## Prism.js Overrides (Linje 463-470)

```css
pre[class*="language-"] {
    margin: 0 !important;
    background: transparent !important;
}

code[class*="language-"] {
    background: transparent !important;
}
```
- **!important** - Overrides Prism's default styles
- **Transparent background** - Uses codeblock background
- **No margin** - Fits within code block perfectly
- **Targets**: Any `class="language-*"` (python, cisco, etc.)

---

## Layout Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Theme Selector                        │ (absolute, top-right)
│                    [Dropdown] [Logout]                   │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ┌───────────┬────────────────┬───────────────┐         │
│  │   Input   │   Left Panel   │  Right Panel  │         │
│  │   Panel   │   (Chat Area)  │ (Code Output) │         │
│  │ (Hidden)  │   800px fixed  │   (Hidden)    │         │
│  │           │                │               │         │
│  │           ├────────────────┤               │         │
│  │  Pasted   │   #chat div    │   Clicked     │         │
│  │   Code    │   (scrollable) │   Code Block  │         │
│  │  Preview  │                │   (scrollable)│         │
│  │           │  Message       │               │         │
│  │           │  Message       │               │         │
│  │           │  Code Block    │               │         │
│  │           │  Message       │               │         │
│  │           │                │               │         │
│  │           ├────────────────┤               │         │
│  │           │ Input Container│               │         │
│  │           │ [Textarea][Send│               │         │
│  └───────────┴────────────────┴───────────────┘         │
│                                                          │
│          Watermark (Kali dragon, z-index 1)             │
└──────────────────────────────────────────────────────────┘

Positioning:
- Input Panel: 0 to calc(50% - 400px) (left edge to chat panel)
- Left Panel: calc(50% - 400px) to calc(50% + 400px) (centered 800px)
- Right Panel: calc(50% + 400px) to 100% (chat panel to right edge)
```

---

## CSS Variables Usage Pattern

### Set in base.css
```css
:root {
    --bg-darkest: #505050;
}
```

### Overridden by themes.js
```javascript
root.style.setProperty('--bg-darkest', '#1a1a1a');
```

### Used throughout CSS
```css
body {
    background: var(--bg-darkest);
}
```

### Result
- **Theme switch** changes one variable
- **All references** update automatically
- **No DOM manipulation** needed

---

## Responsive Considerations

### Fixed 800px Chat Panel
- **Not responsive** - Fixed width
- **Assumption**: Desktop use (1920x1080 or larger)
- **Mobile**: Would need media queries

### Improvement Opportunity
```css
@media (max-width: 1200px) {
    #left-panel {
        width: 90%;
        left: 5%;
    }
}
```

---

## Performance Notes

### Animations
- **GPU-accelerated** - `transform`, `opacity` (not `top`, `left`)
- **Smooth 60fps** - Modern browsers handle well

### Transparency
- **Many rgba() colors** - Slight performance cost
- **Acceptable** - Not noticeable on modern hardware

### Repaints
- **Hover effects** - Minimal (color/transform only)
- **No layout shifts** - Positions fixed

---

## Browser Compatibility

### CSS Variables
- **Chrome 49+**, **Firefox 31+**, **Safari 9.1+**
- **IE**: Not supported (could use Sass fallback)

### Flexbox
- **Chrome 29+**, **Firefox 28+**, **Safari 9+**, **IE 11**
- **Universal** in modern browsers

### CSS Grid (not used)
- Could simplify 3-panel layout
- Flexbox + absolute positioning works fine

### Calc()
- **Chrome 26+**, **Firefox 16+**, **Safari 7+**, **IE 9+**
- **Universal** support

---

## Konklusion

`base.css` is the structural foundation:
- **476 lines** defining entire UI layout
- **CSS variables** for easy theming
- **3-panel layout** (input, chat, code output)
- **Flexbox + absolute positioning** for complex layout
- **Animations** for smooth UX (fadeIn, ripple, hover effects)
- **Custom scrollbars** for Webkit browsers
- **Watermark** via pseudo-element (Kali dragon)
- **Theme-agnostic** - Works with any color scheme

**Key design decisions:**
- Centered 800px chat panel (desktop-focused)
- Transparent backgrounds (watermark visible)
- CSS variables for all colors (theme flexibility)
- Fixed positioning for side panels (no layout shifts)
- Smooth transitions (0.2s ease standard)
- Custom scrollbar styling (brand consistency)

**File size**: 476 lines orchestrating entire chatbot layout and component styling.
