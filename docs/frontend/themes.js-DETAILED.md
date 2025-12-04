# themes.js - Detaljeret Dokumentation

## Overordnet Formål
`themes.js` håndterer theme switching for hele chatbot UI'et. Den styrer:
- CSS custom properties (CSS variables) for farver
- Prism.js syntax highlighting themes
- Light/dark mode watermark filters
- Browser theme color (address bar farve)
- LocalStorage persistence (disabled - always defaults til Cisco)

**Fil størrelse**: 260 linjer
**Dependencies**: Bruges af index.html, påvirker alle CSS filer
**Global exports**: `themes` object, `applyTheme()`, `initThemes()`

---

## Theme Definitions Object (Linje 3-152)

### Structure Overview
```javascript
const themes = {
    themeName: {
        '--css-variable': '#hexcolor',
        prismTheme: 'prism-theme-name',
        lightTheme: true/false (optional)
    }
}
```

### CSS Custom Properties
Hver theme definerer 13 CSS variables:
1. `--bg-darkest` - Darkest background (main bg, browser theme color)
2. `--bg-dark` - Dark background (panels)
3. `--bg-medium` - Medium background (hover states)
4. `--border-color` - Borders and dividers
5. `--text-primary` - Main text color
6. `--text-secondary` - Secondary/muted text
7. `--accent-primary` - Primary accent (links, highlights)
8. `--accent-secondary` - Secondary accent
9. `--button-primary` - Primary button color
10. `--button-primary-hover` - Button hover state
11. `--button-secondary` - Secondary button
12. `--scrollbar-thumb` - Scrollbar color
13. `--scrollbar-thumb-hover` - Scrollbar hover

### Special Properties
- **prismTheme** - Prism.js theme name for syntax highlighting
- **lightTheme** - Boolean flag for light modes (affects watermark filter)

---

## Theme 1: VS Code Dark (Linje 4-18)

```javascript
vscode: {
    '--bg-darkest': '#1e1e1e',     // Very dark gray (VS Code bg)
    '--bg-dark': '#252526',         // Slightly lighter panels
    '--bg-medium': '#2d2d30',       // Hover states
    '--border-color': '#3e3e42',    // Subtle borders
    '--text-primary': '#cccccc',    // Light gray text
    '--text-secondary': '#6a6a6a',  // Muted gray
    '--accent-primary': '#4ec9b0',  // Teal (VS Code highlight)
    '--accent-secondary': '#ce9178', // Orange (strings)
    '--button-primary': '#0e639c',  // Blue button
    '--button-primary-hover': '#1177bb', // Lighter blue hover
    '--button-secondary': '#4ec9b0', // Teal secondary
    '--scrollbar-thumb': '#424242',  // Gray scrollbar
    '--scrollbar-thumb-hover': '#4e4e4e', // Lighter hover
    prismTheme: 'tomorrow'          // Prism Tomorrow Night theme
}
```

**Color Scheme**: Dark gray base with teal/orange accents (matches VS Code)

---

## Theme 2: Monokai (Linje 19-33)

```javascript
monokai: {
    '--bg-darkest': '#1e1e1e',     // Same as VS Code (compatibility)
    '--bg-dark': '#272822',         // Monokai signature dark brown
    '--bg-medium': '#3e3d32',       // Brown-gray
    '--border-color': '#49483e',    // Olive border
    '--text-primary': '#f8f8f2',    // Almost white
    '--text-secondary': '#75715e',  // Brown-gray (comments)
    '--accent-primary': '#a6e22e',  // Bright green (keywords)
    '--accent-secondary': '#f92672', // Hot pink (special)
    '--button-primary': '#ae81ff',  // Purple button
    '--button-primary-hover': '#c49dff', // Lighter purple
    '--button-secondary': '#a6e22e', // Green secondary
    '--scrollbar-thumb': '#49483e',  // Olive scrollbar
    '--scrollbar-thumb-hover': '#5a5950',
    prismTheme: 'okaidia'           // Prism Okaidia (Monokai-like)
}
```

**Color Scheme**: Dark brown-black base with green/pink/purple accents

---

## Theme 3: Dracula (Linje 34-48)

```javascript
dracula: {
    '--bg-darkest': '#21222c',     // Dark purple-blue
    '--bg-dark': '#282a36',         // Dracula signature bg
    '--bg-medium': '#343746',       // Lighter purple
    '--border-color': '#44475a',    // Subtle purple border
    '--text-primary': '#f8f8f2',    // Almost white
    '--text-secondary': '#6272a4',  // Blue-gray (comments)
    '--accent-primary': '#8be9fd',  // Cyan (functions)
    '--accent-secondary': '#ff79c6', // Pink (keywords)
    '--button-primary': '#bd93f9',  // Purple button
    '--button-primary-hover': '#caa7ff', // Lighter purple
    '--button-secondary': '#50fa7b', // Green secondary
    '--scrollbar-thumb': '#44475a',  // Purple scrollbar
    '--scrollbar-thumb-hover': '#565869',
    prismTheme: 'okaidia'           // Okaidia close enough
}
```

**Color Scheme**: Dark purple base with cyan/pink/purple accents (Dracula palette)

---

## Theme 4: Nord (Linje 49-63)

```javascript
nord: {
    '--bg-darkest': '#2e3440',     // Nord dark blue-gray
    '--bg-dark': '#3b4252',         // Slightly lighter
    '--bg-medium': '#434c5e',       // Medium blue-gray
    '--border-color': '#4c566a',    // Blue border
    '--text-primary': '#eceff4',    // Almost white (snow storm)
    '--text-secondary': '#616e88',  // Muted blue-gray
    '--accent-primary': '#88c0d0',  // Frost blue (cyan)
    '--accent-secondary': '#d08770', // Aurora orange
    '--button-primary': '#5e81ac',  // Frost blue button
    '--button-primary-hover': '#81a1c1', // Lighter frost
    '--button-secondary': '#a3be8c', // Aurora green
    '--scrollbar-thumb': '#4c566a',  // Blue-gray scrollbar
    '--scrollbar-thumb-hover': '#5a6680',
    prismTheme: 'twilight'          // Prism Twilight (bluish)
}
```

**Color Scheme**: Cool blue-gray (Nordic winter palette)

---

## Theme 5: Solarized Dark (Linje 64-78)

```javascript
solarized: {
    '--bg-darkest': '#002b36',     // Solarized dark blue
    '--bg-dark': '#073642',         // Slightly lighter blue
    '--bg-medium': '#094656',       // Medium blue
    '--border-color': '#0d5766',    // Teal border
    '--text-primary': '#839496',    // Gray-blue text
    '--text-secondary': '#586e75',  // Muted gray
    '--accent-primary': '#2aa198',  // Cyan accent
    '--accent-secondary': '#cb4b16', // Orange accent
    '--button-primary': '#268bd2',  // Blue button
    '--button-primary-hover': '#3a9ce3', // Lighter blue
    '--button-secondary': '#859900', // Green secondary
    '--scrollbar-thumb': '#0d5766',  // Teal scrollbar
    '--scrollbar-thumb-hover': '#11697a',
    prismTheme: 'solarizedlight'    // Confusingly named (works for dark)
}
```

**Color Scheme**: Dark blue-teal base (Solarized Dark palette)

---

## Theme 6: GitHub Dark (Linje 79-93)

```javascript
github: {
    '--bg-darkest': '#0d1117',     // GitHub dark bg
    '--bg-dark': '#161b22',         // Panel background
    '--bg-medium': '#21262d',       // Hover states
    '--border-color': '#30363d',    // Subtle gray border
    '--text-primary': '#c9d1d9',    // Light gray text
    '--text-secondary': '#8b949e',  // Muted gray
    '--accent-primary': '#58a6ff',  // Blue (links)
    '--accent-secondary': '#f85149', // Red (errors)
    '--button-primary': '#238636',  // Green button (GitHub style)
    '--button-primary-hover': '#2ea043', // Lighter green
    '--button-secondary': '#58a6ff', // Blue secondary
    '--scrollbar-thumb': '#30363d',  // Gray scrollbar
    '--scrollbar-thumb-hover': '#484f58',
    prismTheme: 'tomorrow'          // Tomorrow Night
}
```

**Color Scheme**: Dark gray-blue (GitHub dark mode palette)

---

## Theme 7: Cisco (Linje 94-114) - DEFAULT

```javascript
cisco: {
    '--bg-darkest': '#505050',     // Medium gray (not pure black)
    '--bg-dark': '#505050',         // Same as darkest
    '--bg-medium': '#585858',       // Slightly lighter gray
    '--border-color': '#707070',    // Light gray border
    '--text-primary': '#00ffff',    // Bright cyan (signature)
    '--text-secondary': '#00d7ff',  // Slightly darker cyan
    '--accent-primary': '#00ffff',  // Cyan accent
    '--accent-secondary': '#00d7ff', // Cyan secondary
    '--button-primary': '#006b7a',  // Dark cyan button
    '--button-primary-hover': '#008a9c', // Lighter cyan hover
    '--button-secondary': '#00ffff', // Bright cyan secondary
    '--scrollbar-thumb': '#707070',  // Gray scrollbar
    '--scrollbar-thumb-hover': '#808080',
    prismTheme: 'tomorrow'          // Tomorrow Night
}
```

**Color Scheme**: Gray base with bright cyan text (Cisco terminal style)
**Special**: User messages use orange (#ffaa33) via CSS override in cisco.css

---

## Theme 8: Light (Linje 115-131)

```javascript
light: {
    '--bg-darkest': '#ffffff',     // Pure white
    '--bg-dark': '#f5f5f5',         // Off-white panels
    '--bg-medium': '#e8e8e8',       // Light gray hover
    '--border-color': '#d0d0d0',    // Gray borders
    '--text-primary': '#2c3e50',    // Dark blue-gray text
    '--text-secondary': '#7f8c8d',  // Medium gray
    '--accent-primary': '#3498db',  // Blue accent
    '--accent-secondary': '#e74c3c', // Red accent
    '--button-primary': '#3498db',  // Blue button
    '--button-primary-hover': '#2980b9', // Darker blue
    '--button-secondary': '#2ecc71', // Green secondary
    '--scrollbar-thumb': '#bdc3c7',  // Light gray scrollbar
    '--scrollbar-thumb-hover': '#95a5a6',
    prismTheme: 'solarizedlight',   // Light syntax theme
    lightTheme: true                // Flag for watermark filter
}
```

**Color Scheme**: White base with blue/red/green accents (standard light mode)
**Special**: `lightTheme: true` triggers lighter dragon watermark

---

## Theme 9: Light Quiet (Linje 132-149)

```javascript
'light-quiet': {
    '--bg-darkest': '#f5f0f5',     // Very light purple tint
    '--bg-dark': '#f0e8f0',         // Lighter purple panels
    '--bg-medium': '#e8dce8',       // Medium purple
    '--border-color': '#c8b8c8',    // Muted purple border
    '--text-primary': '#4a3a4a',    // Dark purple-gray text
    '--text-secondary': '#8b7b9b',  // Medium purple-gray
    '--accent-primary': '#b08bc0',  // Purple accent
    '--accent-secondary': '#d88ba8', // Pink accent
    '--button-primary': '#b8a8c8',  // Muted purple button
    '--button-primary-hover': '#9b8bab', // Darker purple
    '--button-secondary': '#c8a8d8', // Light purple secondary
    '--scrollbar-thumb': '#b4a4c4',  // Purple scrollbar
    '--scrollbar-thumb-hover': '#9688a6',
    prismTheme: 'quietlight',       // Custom quiet theme
    lightTheme: true                // Light watermark
}
```

**Color Scheme**: Soft purple-tinted light mode (easier on eyes than pure white)

---

## applyTheme() Function (Linje 154-248)

### Function Signature (Linje 154)
```javascript
function applyTheme(themeName) {
```

### Purpose
Applies selected theme by:
1. Setting CSS custom properties
2. Adding body class for special styling
3. Managing watermark filter (light/dark)
4. Updating browser UI color
5. Switching Prism.js theme
6. Re-highlighting all code blocks
7. Saving to localStorage

### Parameter Validation (Linje 155-156)
```javascript
const theme = themes[themeName];
if (!theme) return;
```
- **Linje 155**: Lookup theme in themes object
- **Linje 156**: Guard clause - exit if theme not found

### Apply CSS Variables (Linje 158-164)
```javascript
const root = document.documentElement;
Object.keys(theme).forEach(key => {
    if (key !== 'prismTheme' && key !== 'lightTheme') {
        root.style.setProperty(key, theme[key]);
    }
});
```
- **Linje 158**: Get `:root` element (`<html>`)
  - CSS variables defined on root are global
  
- **Linje 159**: `Object.keys(theme)` - Get all property names
  - Returns: `['--bg-darkest', '--bg-dark', ..., 'prismTheme']`
  
- **Linje 160**: Skip non-CSS properties
  - `prismTheme` - Not a CSS variable
  - `lightTheme` - Boolean flag, not CSS
  
- **Linje 161**: **Set CSS custom property**
  - `root.style.setProperty('--bg-darkest', '#1e1e1e')`
  - Updates CSS variable dynamically
  - **Immediately** affects ALL CSS using `var(--bg-darkest)`

**CSS Variable Example:**
```css
/* In base.css: */
body {
    background: var(--bg-darkest);  /* Reads current value */
}

/* JavaScript changes value: */
root.style.setProperty('--bg-darkest', '#ffffff');
/* → Body background instantly updates to white */
```

### Add Body Class (Linje 167)
```javascript
document.body.className = themeName;
```
- **Replaces ALL existing classes** with theme name
- **Purpose**: Theme-specific CSS overrides
  - Example: `body.cisco .message.user { color: #ffaa33; }`
  - Allows CSS files to target specific themes

### Watermark Filter Handling (Linje 169-177)
```javascript
const watermark = document.querySelector('body::before') || document.body;
if (theme.lightTheme) {
    document.body.setAttribute('data-light-theme', 'true');
} else {
    document.body.removeAttribute('data-light-theme');
}
```
- **Linje 170**: Query `body::before` pseudo-element (watermark)
  - **Note**: Can't actually select pseudo-elements via querySelector
  - Fallback to body (watermark styled via CSS)
  
- **Linje 171-173**: Light theme
  - Set `data-light-theme="true"` attribute
  - CSS selector: `body[data-light-theme="true"]::before`
  - Light watermark: darker dragon on white bg
  
- **Linje 174-176**: Dark theme
  - Remove attribute
  - CSS selector: `body::before` (default)
  - Dark watermark: lighter dragon with grayscale filter

**CSS Integration:**
```css
/* base.css - Dark theme watermark: */
body::before {
    background-image: url('kali-layers.png');
    filter: grayscale(100%) brightness(0.8);  /* Light dragon */
}

/* light-theme.css - Light theme watermark: */
body[data-light-theme="true"]::before {
    background-image: url('kali-layers-light2.jpeg');
    filter: none;  /* Dark dragon, no filter */
}
```

### Browser Theme Color (Linje 179-204)

#### Remove Old Meta Tags (Linje 181-182)
```javascript
const oldMetaTags = document.querySelectorAll('meta[name="theme-color"], meta[name="msapplication-navbutton-color"]');
oldMetaTags.forEach(tag => tag.remove());
```
- **Linje 181**: Select ALL theme-color meta tags
  - Standard `theme-color` (Chrome, Firefox, Safari)
  - IE/Edge `msapplication-navbutton-color`
  
- **Linje 182**: Remove all found tags
  - **Why remove?** Some browsers ignore `setAttribute` updates
  - Creating fresh tags ensures update works

#### Get Theme Color (Linje 184)
```javascript
const themeColor = theme['--bg-darkest'];
```
- Use darkest background as browser UI color
- Matches main app background

#### Create Fresh Meta Tags (Linje 186-201)
```javascript
const head = document.querySelector('head');

const metaThemeColor = document.createElement('meta');
metaThemeColor.name = 'theme-color';
metaThemeColor.content = themeColor;
head.appendChild(metaThemeColor);

const metaMsNav = document.createElement('meta');
metaMsNav.name = 'msapplication-navbutton-color';
metaMsNav.content = themeColor;
head.appendChild(metaMsNav);
```
- **Linje 189-192**: Standard theme-color meta tag
  - Colors browser address bar on mobile (Chrome, Firefox)
  - Colors title bar on desktop PWA
  
- **Linje 195-198**: Microsoft-specific tag
  - Colors navigation bar in IE/Edge
  - Legacy support

#### Update Body Background (Linje 203-204)
```javascript
document.body.style.backgroundColor = themeColor;
document.documentElement.style.backgroundColor = themeColor;
```
- **Linje 203**: Set body background color
  - Backup for areas not covered by CSS
  
- **Linje 204**: Set html (root) background
  - Ensures entire viewport colored
  - Visible during scrolling bounce on mobile

### Prism Theme Switching (Linje 206-232)

#### Get Prism Elements (Linje 207-209)
```javascript
const prismLink = document.querySelector('link[href*="prism"]');
const ciscoTheme = document.getElementById('cisco-prism-theme');
const quietLightTheme = document.getElementById('quiet-light-prism-theme');
```
- **Linje 207**: CDN Prism CSS link
  - `<link href="https://...prism-tomorrow.min.css">`
  
- **Linje 208**: Inline Cisco theme style tag
  - `<style id="cisco-prism-theme" disabled>@import ...</style>`
  
- **Linje 209**: Inline Quiet Light theme
  - `<style id="quiet-light-prism-theme" disabled>...</style>`

#### Cisco Theme Branch (Linje 211-216)
```javascript
if (themeName === 'cisco' && ciscoTheme) {
    if (prismLink) prismLink.disabled = true;
    if (ciscoTheme) ciscoTheme.disabled = false;
    if (quietLightTheme) quietLightTheme.disabled = true;
}
```
- **Enable custom Cisco Prism theme**
- Disable CDN theme and Quiet Light
- Custom theme in `/static/css/themes/cisco-theme.css`

#### Quiet Light Branch (Linje 217-222)
```javascript
else if (themeName === 'light-quiet' && quietLightTheme) {
    if (prismLink) prismLink.disabled = true;
    if (ciscoTheme) ciscoTheme.disabled = true;
    if (quietLightTheme) quietLightTheme.disabled = false;
}
```
- **Enable Quiet Light Prism theme**
- Disable others
- Custom theme for soft light mode

#### Standard Themes Branch (Linje 223-232)
```javascript
else {
    if (ciscoTheme) ciscoTheme.disabled = true;
    if (quietLightTheme) quietLightTheme.disabled = true;
    if (prismLink) {
        prismLink.disabled = false;
        prismLink.href = `https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-${theme.prismTheme}.min.css`;
    }
}
```
- **Disable custom themes**
- **Enable CDN Prism link**
- **Update href dynamically**
  - Template literal: `prism-tomorrow.min.css`
  - Loads different Prism theme from CDN
  - Examples:
    - `prism-tomorrow.min.css` (dark)
    - `prism-okaidia.min.css` (Monokai-like)
    - `prism-solarizedlight.min.css` (light)

### Re-highlight Code Blocks (Linje 234-247)
```javascript
setTimeout(() => {
    if (typeof Prism !== 'undefined') {
        document.querySelectorAll('pre code').forEach(block => {
            block.removeAttribute('class');
            block.className = block.parentElement.className.replace('line-numbers', '').trim();
            
            if (Prism.highlightElement) {
                Prism.highlightElement(block);
            }
        });
    }
}, 150);
```
- **Linje 234**: **Delay 150ms**
  - Gives browser time to load new Prism CSS
  - CSS must be loaded before highlighting applies
  
- **Linje 235**: Check if Prism loaded
  
- **Linje 236**: Query all code blocks
  - `pre code` - All code elements inside pre tags
  
- **Linje 237-238**: **Reset classes**
  - Remove old classes (from previous theme)
  - Copy parent (pre) classes to code
  - Remove `line-numbers` plugin class
  
- **Linje 240-242**: **Re-apply highlighting**
  - `Prism.highlightElement(block)` - Re-parse and color
  - Applies new theme colors

**Why re-highlight?**
- Prism adds `<span>` tags with color classes
- Different themes use different classes
- Must re-parse to apply new color scheme

### Save to LocalStorage (Linje 249-250)
```javascript
localStorage.setItem('chatbot-theme', themeName);
```
- **Persist theme preference**
- Key: `'chatbot-theme'`
- Value: `'cisco'`, `'vscode'`, etc.
- **Note**: Currently ignored by `initThemes()` (always resets to Cisco)

---

## initThemes() Function (Linje 253-260)

### Function Signature (Linje 253)
```javascript
function initThemes() {
```

### Purpose
Initialize theme system on page load:
1. Get theme dropdown element
2. Force default to Cisco (ignore saved theme)
3. Apply Cisco theme
4. Setup change event listener

### Get Dropdown (Linje 254)
```javascript
const themeDropdown = document.getElementById('theme-dropdown');
```
- References `<select id="theme-dropdown">` in index.html

### Force Cisco Default (Linje 256-258)
```javascript
const defaultTheme = 'cisco';
themeDropdown.value = defaultTheme;
applyTheme(defaultTheme);
```
- **Linje 256**: Hardcoded to `'cisco'`
  - **Comment says**: "Always reset to Cisco theme on page load (ignore saved theme)"
  - **Why?** Design decision - Cisco is brand theme
  - localStorage value ignored (saved but not loaded)
  
- **Linje 257**: Set dropdown selection to Cisco
  
- **Linje 258**: Apply Cisco theme CSS

### Event Listener (Linje 260-262)
```javascript
themeDropdown.addEventListener('change', (e) => {
    applyTheme(e.target.value);
});
```
- **Listen for dropdown changes**
- `e.target.value` - Selected option value (`'vscode'`, `'dracula'`, etc.)
- Call `applyTheme()` with new theme

---

## Data Flow Diagram

### Page Load:
```
index.html loads
    ↓
<script src="themes.js"> executes
    ↓
themes object defined (global)
    ↓
ui-handlers.js calls initThemes()
    ↓
Force Cisco theme:
    ├─ themeDropdown.value = 'cisco'
    └─ applyTheme('cisco')
        ├─ Set CSS variables
        ├─ Add body.cisco class
        ├─ Remove data-light-theme attribute
        ├─ Update browser theme-color
        ├─ Enable Cisco Prism theme
        └─ Save to localStorage
```

### User Changes Theme:
```
User selects dropdown → 'change' event
    ↓
applyTheme(e.target.value)
    ↓
Parallel updates:
    ├─ CSS variables → Instant color change
    ├─ Body class → Theme-specific CSS
    ├─ Watermark filter → Light/dark dragon
    ├─ Browser UI color → Address bar
    ├─ Prism theme → Syntax colors
    └─ Re-highlight code → Apply new colors
```

---

## CSS Variable Integration

### How It Works:
```css
/* base.css defines placeholders: */
body {
    background: var(--bg-darkest);
    color: var(--text-primary);
}

/* JavaScript injects actual values: */
document.documentElement.style.setProperty('--bg-darkest', '#1e1e1e');
document.documentElement.style.setProperty('--text-primary', '#cccccc');

/* → CSS instantly evaluates to: */
body {
    background: #1e1e1e;
    color: #cccccc;
}
```

### Benefits:
1. **Single source of truth** - Color defined once in JS
2. **Instant updates** - No CSS reload needed
3. **Global scope** - All elements update automatically
4. **Theme-able** - Easy to add new themes

---

## LocalStorage Pattern

### Save (applyTheme):
```javascript
localStorage.setItem('chatbot-theme', themeName);
```

### Load (initThemes):
```javascript
// DISABLED - Not currently used:
// const savedTheme = localStorage.getItem('chatbot-theme');
// Always use Cisco instead:
const defaultTheme = 'cisco';
```

### Why Disabled?
- **Design choice** - Cisco is brand identity
- **Consistency** - Every user sees Cisco on load
- **User can still switch** - Just not persisted across sessions

---

## Performance Considerations

### CSS Variables
- **Native browser feature** - Very fast
- **No layout thrashing** - Pure color changes
- **GPU accelerated** - Hardware rendering

### Prism Re-highlight
- **Delayed 150ms** - Prevents blocking
- **Only on theme change** - Not during typing
- **Selective parsing** - Only existing code blocks

### Meta Tag Recreation
- **Removes old tags first** - Prevents duplicates
- **Fresh creation** - Ensures browser updates
- **Minimal DOM changes** - Only 2 tags

---

## Browser Compatibility

### CSS Variables
- **Chrome 49+**, **Firefox 31+**, **Safari 9.1+**, **Edge 15+**
- **IE 11**: Not supported (fallback to default colors)

### Theme-Color Meta
- **Mobile**: Chrome, Firefox, Safari (iOS 15+)
- **Desktop**: Limited support, mostly PWA
- **Graceful degradation**: Doesn't break if not supported

### Prism.js
- **All modern browsers**
- **CDN fallback**: If CDN fails, no highlighting (code still readable)

---

## Security Notes

### XSS Prevention
- **Hex colors only** - No user input in color values
- **Predefined themes** - Can't inject malicious CSS
- **localStorage** - Only theme name stored (validated against themes object)

### Safe DOM Manipulation
- **createElement over innerHTML** - No HTML parsing
- **setAttribute** - Properly escaped attributes
- **textContent** - Not used here, but good practice

---

## Konklusion

`themes.js` provides a robust theme system with:
- **9 predefined themes** (7 dark, 2 light)
- **CSS variable-based** coloring (instant updates)
- **Prism integration** for syntax highlighting
- **Browser UI integration** (theme-color meta tags)
- **Light/dark watermark** handling
- **LocalStorage persistence** (currently disabled, defaults to Cisco)

**Key design decisions:**
- Force Cisco theme on load (brand identity)
- CSS variables for dynamic theming (no page reload)
- Re-highlight code blocks on theme change (consistent colors)
- Remove/recreate meta tags (browser compatibility)

**File size**: 260 lines of essential theming logic.
