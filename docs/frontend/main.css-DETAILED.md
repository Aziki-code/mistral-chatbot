# main.css - Detaljeret Dokumentation

## Overordnet Formål
`main.css` er import hub for hele CSS strukturen. Den:
- Importerer base styles (layout, components)
- Loader alle 9 theme files
- Organiserer import order (base → themes)
- Fungerer som single entry point for index.html

**Fil størrelse**: 23 linjer (kun imports, ingen styles)
**Pattern**: CSS @import cascade
**Load order**: Critical for CSS specificity

---

## CSS @import Direktiv

### Syntax
```css
@import url('file.css');
```

### How it Works
- **Browser request** - Separate HTTP request per import
- **Blocking** - Loads sequentially (not parallel)
- **Cascade** - Later imports override earlier ones (CSS specificity)

### Performance Note
- **Multiple requests** - Can be slow (vs single bundled file)
- **Cache benefit** - Browser caches individual files
- **Development friendly** - Easy to find/edit specific file
- **Production**: Should bundle/minify (webpack, gulp, etc.)

---

## Import Structure

### 1. Base Styles (Linje 4)
```css
@import url('base.css');
```

#### Purpose
- **Foundation** - Layout, structure, components
- **Theme-agnostic** - Works with any theme
- **Loaded first** - Themes override base colors

#### Contains
- Body base styles, watermark
- Chat container, input panel, code output layout
- Message bubbles (user/assistant)
- Code blocks structure
- Buttons, scrollbars, animations

#### Why First?
- **Default values** - Sets base before theme overrides
- **Example**:
  ```css
  /* base.css */
  .message.user { background: gray; }
  
  /* themes/cisco.css (loaded after) */
  .message.user { background: #ff6600; } /* Overrides gray */
  ```

---

### 2. Dark Themes (Linje 7-13)

#### cisco.css (Linje 7)
```css
@import url('themes/cisco.css');
```
- **Default theme** - Orange user messages, gray background
- **Custom Cisco branding** - Company colors
- **Most used** - initThemes() forces this on load

#### vscode.css (Linje 8)
```css
@import url('themes/vscode.css');
```
- **VS Code Dark+** - Microsoft's editor theme
- **Blue accents** - Popular developer choice

#### monokai.css (Linje 9)
```css
@import url('themes/monokai.css');
```
- **Sublime Text classic** - Green on dark gray
- **High contrast** - Good readability

#### dracula.css (Linje 10)
```css
@import url('themes/dracula.css');
```
- **Dracula theme** - Purple/pink accents
- **Popular** - GitHub, VS Code, terminal themes

#### nord.css (Linje 11)
```css
@import url('themes/nord.css');
```
- **Nord palette** - Arctic, cold-inspired colors
- **Blue-gray** - Calm, professional look

#### solarized.css (Linje 12)
```css
@import url('themes/solarized.css');
```
- **Solarized Dark** - Brown/orange tones
- **Low contrast** - Easy on eyes

#### github.css (Linje 13)
```css
@import url('themes/github.css');
```
- **GitHub Dark** - Official GitHub colors
- **Familiar** - Matches GitHub UI

---

### 3. Light Themes (Linje 16-17)

#### light-theme.css (Linje 16)
```css
@import url('themes/light-theme.css');
```
- **Light mode** - White background, dark text
- **162 lines** - Most complex light theme
- **Overrides watermark** - Light version of Kali dragon

#### light-quiet-theme.css (Linje 17)
```css
@import url('themes/light-quiet-theme.css');
```
- **Soft light mode** - Muted purple accents
- **Gentle colors** - Less harsh than pure white

---

### 4. Syntax Highlighting Themes (Linje 20-22)

#### cisco-theme.css (Linje 20)
```css
@import url('themes/cisco-theme.css');
```
- **Prism.js theme** - Cisco-specific code colors
- **Matches Cisco brand** - Orange keywords, cyan strings

#### cisco-light-theme.css (Linje 21)
```css
@import url('themes/cisco-light-theme.css');
```
- **Light version** - For light mode compatibility
- **Dark text on light** - Readable code blocks

#### quiet-light-theme.css (Linje 22)
```css
@import url('themes/quiet-light-theme.css');
```
- **Soft syntax colors** - Muted highlighting
- **Less distraction** - Gentle on eyes

---

## Load Order Diagram

```
Browser loads index.html
    ↓
<link rel="stylesheet" href="main.css">
    ↓
main.css @imports (sequential):
    ↓
1. base.css (foundation)
    ├─ Body, layout, watermark
    ├─ Chat container structure
    ├─ Message bubbles (default colors)
    ├─ Code blocks structure
    └─ Animations, scrollbars
    ↓
2. cisco.css (theme override)
    ├─ --bg-darkest: #1a1a1a
    ├─ --text-primary: #e0e0e0
    ├─ .message.user: #ff6600
    └─ Overrides base.css colors
    ↓
3. vscode.css (loaded but not active)
    └─ CSS rules exist, but not applied (body.vscode-theme required)
    ↓
4. monokai.css, dracula.css, nord.css... (all loaded but inactive)
    ↓
5. light-theme.css (special body.light-theme activation)
    ↓
6. cisco-theme.css (Prism.js code colors)
    ↓
Page renders with combined CSS
```

---

## CSS Specificity & Override Strategy

### Base CSS (Low Specificity)
```css
/* base.css */
.message.user {
    background: #2a2a2a; /* Default gray */
}
```

### Theme CSS (Same Specificity, Later in Cascade)
```css
/* themes/cisco.css */
.message.user {
    background: var(--user-msg-bg); /* Orange via CSS variable */
}
```

### Result
- **Later rule wins** - cisco.css loaded after base.css
- **Theme overrides base** - Orange replaces gray

### Body Class Toggle
```css
/* themes/light-theme.css */
body.light-theme .message.user {
    background: #007bff; /* Blue for light mode */
}
```
- **Higher specificity** - `body.light-theme .message.user` beats `.message.user`
- **Conditional** - Only applies when `<body class="light-theme">`

---

## Theme Activation Flow

### Default (Page Load)
```
1. All CSS loaded (base + 9 themes)
2. themes.js runs → initThemes()
3. Force Cisco theme: applyTheme('cisco')
4. Body class: <body class="cisco-theme">
5. CSS variables injected: root.style.setProperty('--bg-darkest', '#1a1a1a')
6. Result: Cisco colors applied
```

### User Switches Theme
```
1. User selects "Dracula" from dropdown
2. themes.js → applyTheme('dracula')
3. Remove old class: body.classList.remove('cisco-theme')
4. Add new class: body.classList.add('dracula-theme')
5. Update CSS variables: root.style.setProperty('--bg-darkest', '#282a36')
6. Result: Dracula colors applied instantly
```

---

## File Paths

### Relative URLs
```css
@import url('base.css');               /* Same directory as main.css */
@import url('themes/cisco.css');       /* Subdirectory */
```

### Resolved Paths
```
/static/css/main.css                   ← Entry point
/static/css/base.css                   ← Base styles
/static/css/themes/cisco.css           ← Theme file
/static/css/themes/vscode.css
...
```

### HTML Reference
```html
<!-- index.html -->
<link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
```
- **Flask url_for** - Generates `/static/css/main.css`
- **Browser loads** - Then processes @imports

---

## Cache Strategy

### Individual Files
- **Advantage**: Change one theme file → Only that file re-downloaded
- **Browser cache**: Unchanged files (base.css, other themes) cached

### Cache Busting
```html
<!-- Current approach: No versioning -->
<link rel="stylesheet" href="/static/css/main.css">

<!-- Better approach: Version query string -->
<link rel="stylesheet" href="/static/css/main.css?v=7.2">
```
- **Query param**: `?v=7.2` forces new download when incremented
- **Currently**: Browser might cache old CSS (requires hard refresh)

---

## Performance Analysis

### Load Time (Development)
```
main.css:          ~5ms   (download)
  ├─ base.css:     ~50ms  (476 lines)
  ├─ cisco.css:    ~10ms  (43 lines)
  ├─ vscode.css:   ~10ms
  ├─ monokai.css:  ~10ms
  ├─ dracula.css:  ~10ms
  ├─ nord.css:     ~10ms
  ├─ solarized.css:~10ms
  ├─ github.css:   ~10ms
  ├─ light-theme:  ~30ms  (162 lines)
  ├─ light-quiet:  ~15ms
  ├─ cisco-theme:  ~15ms
  ├─ cisco-light:  ~15ms
  └─ quiet-light:  ~15ms
Total: ~215ms (13 HTTP requests)
```

### Optimization Options

#### 1. Bundling (Webpack/Vite)
```javascript
// webpack.config.js
entry: './static/css/main.css',
output: 'bundle.css'  // Single file
```
- **Result**: 1 HTTP request instead of 13
- **Faster**: ~20ms total load time

#### 2. Critical CSS Inline
```html
<style>
/* Inline critical base styles */
body { background: #1a1a1a; }
</style>
<link rel="stylesheet" href="main.css">
```
- **Instant render** - No FOUC (Flash of Unstyled Content)

#### 3. Preload Hints
```html
<link rel="preload" href="/static/css/base.css" as="style">
```
- **Parallel download** - Browser fetches earlier

---

## Why This Structure?

### Advantages
1. **Modularity** - Each theme in separate file
2. **Maintainability** - Easy to find/edit specific theme
3. **Development** - Change one theme without affecting others
4. **Reusability** - Themes could be shared across projects

### Disadvantages
1. **Performance** - Multiple HTTP requests
2. **No tree-shaking** - All themes loaded (even unused ones)
3. **Cache invalidation** - Harder without versioning

### Better Production Approach
```
Development:  main.css → @imports (easy to edit)
Build step:   Concatenate → Minify → bundle.min.css
Production:   Single file (fast load)
```

---

## Theme Loading Logic

### All Themes Loaded, But...
- **CSS rules exist** for all 9 themes
- **Not all active** - Body class determines which applies

### Example:
```css
/* All loaded in browser: */

/* cisco.css */
body.cisco-theme .message.user { background: orange; }

/* dracula.css */
body.dracula-theme .message.user { background: purple; }

/* vscode.css */
body.vscode-theme .message.user { background: blue; }
```

### Active Theme:
```html
<body class="cisco-theme">
  <!-- Only cisco.css rules apply (body.cisco-theme selector matches) -->
```

### Switch Theme:
```javascript
body.classList.remove('cisco-theme');
body.classList.add('dracula-theme');
// Now dracula.css rules apply (body.dracula-theme selector matches)
```

---

## @import vs <link> (HTML)

### Current Approach (CSS @import):
```css
/* main.css */
@import url('base.css');
```

### Alternative (HTML <link>):
```html
<link rel="stylesheet" href="/static/css/base.css">
<link rel="stylesheet" href="/static/css/themes/cisco.css">
...
```

### Comparison:
| Aspect | @import | <link> |
|--------|---------|--------|
| **Requests** | Sequential | Parallel |
| **Speed** | Slower | Faster |
| **Maintainability** | One file (main.css) | Multiple HTML lines |
| **Cache** | Per-file | Per-file |
| **Best for** | Development | Production |

---

## Dependency Graph

```
index.html
    └─ main.css (entry)
        ├─ base.css (required)
        │   └─ Defines: .message, .codeblock, .chat, etc.
        │
        ├─ Theme CSS files (override base colors)
        │   ├─ cisco.css → body.cisco-theme
        │   ├─ vscode.css → body.vscode-theme
        │   ├─ monokai.css → body.monokai-theme
        │   ├─ dracula.css → body.dracula-theme
        │   ├─ nord.css → body.nord-theme
        │   ├─ solarized.css → body.solarized-theme
        │   ├─ github.css → body.github-theme
        │   ├─ light-theme.css → body.light-theme
        │   └─ light-quiet-theme.css → body.light-quiet-theme
        │
        └─ Prism themes (syntax highlighting)
            ├─ cisco-theme.css → .token.keyword, .token.string, etc.
            ├─ cisco-light-theme.css
            └─ quiet-light-theme.css
```

---

## CSS Variables Integration

### Base CSS Defines Variables
```css
/* base.css */
:root {
    --bg-darkest: #1a1a1a;
    --text-primary: #e0e0e0;
}
```

### Themes Override Variables
```css
/* themes/cisco.css */
/* (Actually set via themes.js, not in CSS file directly) */
:root {
    --bg-darkest: #1a1a1a;
    --text-primary: #e0e0e0;
    --user-msg-bg: #ff6600;
}
```

### Usage in Base CSS
```css
/* base.css */
.message.user {
    background: var(--user-msg-bg);
    color: var(--text-primary);
}
```

### Result
- **Theme switch** changes variables
- **Base CSS** automatically updates (references variables)
- **No re-render** needed (instant color change)

---

## Browser Compatibility

### @import Support
- **IE 5.5+**, **All modern browsers**
- **Universal support**

### CSS Variables (var())
- **IE**: Not supported
- **Chrome 49+**, **Firefox 31+**, **Safari 9.1+**
- **Fallback**: Could use Sass variables (compile-time)

### CSS Cascade
- **Universal** - All browsers understand cascade order

---

## Testing Scenarios

### Test 1: Base Loads First
```
1. Temporarily remove @import url('base.css');
2. Load page
3. Result: No layout, themes don't work
→ Confirms base.css is foundation
```

### Test 2: Theme Override
```
1. Inspect .message.user element
2. Computed style shows: background: #ff6600 (orange)
3. CSS source: cisco.css (not base.css)
→ Confirms theme overrides base
```

### Test 3: Multiple @imports
```
1. Check Network tab in DevTools
2. See 13 CSS requests (main + 12 imports)
3. Check waterfall: Sequential loading
→ Confirms @import behavior
```

### Test 4: Cache
```
1. Load page (all CSS downloaded)
2. Reload page (Cmd+R)
3. Network tab shows: "from cache" for CSS files
→ Confirms browser caching
```

---

## File Size Breakdown

```
main.css:              23 lines   (0.5 KB)
base.css:             476 lines  (12.0 KB)
cisco.css:             43 lines   (1.2 KB)
vscode.css:            43 lines   (1.2 KB)
monokai.css:           43 lines   (1.2 KB)
dracula.css:           43 lines   (1.2 KB)
nord.css:              43 lines   (1.2 KB)
solarized.css:         43 lines   (1.2 KB)
github.css:            43 lines   (1.2 KB)
light-theme.css:      162 lines   (4.5 KB)
light-quiet-theme.css: 43 lines   (1.2 KB)
cisco-theme.css:       50 lines   (1.5 KB)
cisco-light-theme.css: 50 lines   (1.5 KB)
quiet-light-theme.css: 50 lines   (1.5 KB)
────────────────────────────────────────
Total:               1154 lines  (31.2 KB)
```

### Gzipped
- **~8 KB** total (75% compression)
- **Fast load** even on slow connections

---

## Migration to Build System (Future)

### Current (Manual @imports)
```css
@import url('base.css');
@import url('themes/cisco.css');
...
```

### Future (PostCSS/Vite)
```javascript
// vite.config.js
export default {
  css: {
    preprocessorOptions: {
      css: {
        additionalData: `@import "./base.css";`
      }
    }
  }
}
```
- **Build time**: Combines files → Single output
- **Runtime**: One HTTP request
- **Auto prefixing**: Vendor prefixes added automatically

---

## Konklusion

`main.css` is the CSS orchestrator:
- **Import hub** - Single entry point for all styles
- **Ordered loading** - Base → Themes → Syntax highlighting
- **Theme-ready** - All 9 themes preloaded
- **Modular** - Each concern in separate file
- **Development-friendly** - Easy to edit individual themes

**Key design decisions:**
- CSS @import for modularity (not performance optimized)
- Base styles first (foundation before overrides)
- All themes loaded (body class activates specific one)
- Separate Prism themes (syntax highlighting independent)
- No cache busting (could add ?v= versioning)

**File size**: 23 lines orchestrating 1154 lines of CSS across 13 files.

**Next step**: Document base.css (476 lines - foundation of entire layout).
