# Light Theme CSS Files - Detaljeret Dokumentation

Dokumentation for de 2 light theme filer der bruger body class og data attribute selectors til at override dark theme styles.

---

## light-theme.css - Standard Light Theme

### Fil Information
- **Størrelse**: 185 linjer
- **Kompleksitet**: Høj (overrider mange base.css regler)
- **Pattern**: `body[data-light-theme="true"]` + `body.light` selectors
- **Watermark**: Light version af Kali dragon

---

## Watermark Override (Linje 2-17)

### Dual Selectors
```css
body.light::before,
body[data-light-theme="true"]::before {
```
- **body.light** - Legacy selector (backwards compatibility)
- **body[data-light-theme="true"]** - Modern data attribute
- **Why both?** Defensive programming (themes.js might use either)

### Watermark Styling (Linje 3-16)
```css
content: "";
position: fixed;
top: 0;
left: 0;
width: 100%;
height: 100%;
background-image: url('/static/images/kali-layers-light2.jpeg');
background-size: cover;
background-position: center;
background-repeat: no-repeat;
opacity: 0.5;
z-index: 1;
pointer-events: none;
```

#### Differences from Dark Theme
- **Image**: `kali-layers-light2.jpeg` (not `kali-layers.png`)
  - **Lighter version** - Visible against white background
  - **.jpeg** - Photo format (not PNG with transparency)
- **Opacity**: `0.5` (50% visible)
  - **vs Dark**: Dark theme uses 0.4 + filters
  - **More visible** - Needs higher opacity on light background
- **No filters** - Dark theme has `grayscale(100%) brightness(0.8) contrast(1.2)`
  - **Why?** Light image already optimized, no filter needed

---

## Body Base (Linje 19-22)

```css
body.light,
body[data-light-theme="true"] {
    background: #f8f9fa;
    color: #2c3e50;
}
```

### Colors
- **Background**: `#f8f9fa` - Very light gray (248,249,250)
  - **Almost white** - Slight gray tint (reduces eye strain vs pure white)
- **Text**: `#2c3e50` - Dark blue-gray (44,62,80)
  - **High contrast**: 12.7:1 against #f8f9fa (WCAG AAA compliant)
  - **Professional**: Not pure black (easier on eyes)

---

## Chat Panel (Linje 24-27)

```css
body.light #left-panel,
body[data-light-theme="true"] #left-panel {
    background: rgba(248, 249, 250, 0.4);
    border-right: 2px solid rgba(189, 195, 199, 0.3);
}
```

### Semi-Transparent Background
- **rgba(248, 249, 250, 0.4)** - 40% opaque white-gray
  - **Allows watermark** - Kali dragon visible through panel
  - **Glassmorphism** - Modern UI trend (translucent layers)

### Border
- **rgba(189, 195, 199, 0.3)** - 30% opaque gray
  - **Subtle separation** - Not harsh line
  - **Gray tone**: (189,195,199) - Mid-gray

---

## Message Bubbles (Linje 29-42)

### User Message (Linje 29-33)
```css
body[data-light-theme="true"] .message.user {
    background: rgba(52, 152, 219, 0.08);
    color: #2c3e50;
    border: 1px solid rgba(52, 152, 219, 0.2);
}
```

#### Blue Background
- **rgba(52, 152, 219, 0.08)** - 8% opaque blue
  - **Base color**: (52,152,219) - Bright blue
  - **Very subtle** - Just a hint of blue
  - **Differentiates** - From assistant (white)

#### Border
- **rgba(52, 152, 219, 0.2)** - 20% opaque blue
  - **More visible** - Border stronger than background
  - **Visual hierarchy** - Clear message boundary

### Assistant Message (Linje 35-40)
```css
body[data-light-theme="true"] .message.assistant {
    background: rgba(255, 255, 255, 0.25);
    color: #2c3e50;
    border: 1px solid rgba(0, 0, 0, 0.1);
    box-shadow: none;
}
```

#### White Background
- **rgba(255, 255, 255, 0.25)** - 25% opaque white
  - **Lighter than user** - Visual distinction
  - **Watermark visible** - Translucent

#### Border
- **rgba(0, 0, 0, 0.1)** - 10% black
  - **Subtle** - Just enough to define edge

#### No Shadow
- **box-shadow: none** - Overrides base.css shadow
  - **Flat design** - Light theme is simpler, less depth

---

## Code Blocks (Linje 42-59)

### Codeblock Container (Linje 42-48)
```css
body[data-light-theme="true"] .codeblock {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(0, 0, 0, 0.1);
    border-left: 3px solid #5a6268;
    box-shadow: none !important;
}
```

#### Background
- **rgba(255, 255, 255, 0.15)** - 15% white
  - **Very subtle** - Almost transparent
  - **Watermark shows** - Through code block

#### Borders
- **All sides**: 1px with 10% black
- **Left side**: 3px solid `#5a6268` (dark gray)
  - **Accent**: Emphasizes code blocks
  - **Matches light theme** - Gray instead of cyan

#### !important Shadow Override
- **box-shadow: none !important** - Forcefully removes shadow
  - **Why !important?** Base.css or Prism might add shadows
  - **Flat aesthetic** - Light theme avoids depth effects

### Code Content (Linje 50-59)
```css
body[data-light-theme="true"] .codeblock pre {
    color: #2c3e50;
    box-shadow: none !important;
}

body[data-light-theme="true"] .codeblock code {
    box-shadow: none !important;
}

body[data-light-theme="true"] pre[class*="language-"] {
    box-shadow: none !important;
}
```
- **Consistent color**: Same dark blue-gray as body text
- **Multiple shadow overrides** - Ensures no shadows from Prism.js

---

## Panel Outputs (Linje 61-64)

```css
body[data-light-theme="true"] #pasted-code-output,
body[data-light-theme="true"] #code-output {
    color: #2c3e50;
}
```
- **Dark text** - Readable on light background
- **Both panels** - Left (pasted) and right (clicked code)

---

## Custom Scrollbar (Linje 66-72)

```css
body[data-light-theme="true"] ::-webkit-scrollbar-thumb {
    background: rgba(189, 195, 199, 0.6);
}

body[data-light-theme="true"] ::-webkit-scrollbar-thumb:hover {
    background: rgba(149, 165, 166, 0.8);
}
```

### Scrollbar Colors
- **Thumb**: `rgba(189, 195, 199, 0.6)` - 60% opaque gray
  - **Visible but subtle** - Not distracting
- **Hover**: `rgba(149, 165, 166, 0.8)` - 80% opaque darker gray
  - **Feedback** - User knows it's interactive

---

## Input Area (Linje 74-82)

### Textarea (Linje 74-78)
```css
body[data-light-theme="true"] #input {
    background: rgba(255, 255, 255, 0.9);
    color: #2c3e50;
    border: 1px solid rgba(0, 0, 0, 0.2);
}
```
- **90% white** - Nearly opaque (slight transparency)
- **20% black border** - Clearly defined

### Placeholder (Linje 80-82)
```css
body[data-light-theme="true"] #input::placeholder {
    color: #95a5a6;
}
```
- **#95a5a6** - Light gray (149,165,166)
- **Lower contrast** - Indicates placeholder text

---

## Theme Selector (Linje 84-94)

### Label (Linje 84-86)
```css
body[data-light-theme="true"] #theme-selector label {
    color: #2c3e50 !important;
}
```
- **Dark text** - Readable against light background
- **!important** - Overrides any other label color rules

### Dropdowns (Linje 88-93)
```css
body[data-light-theme="true"] #theme-selector select,
body[data-light-theme="true"] #ai-model-dropdown {
    background: rgba(255, 255, 255, 0.95);
    color: #2c3e50;
    border: 1px solid rgba(0, 0, 0, 0.2);
}
```
- **95% white** - Nearly solid
- **Both dropdowns** - Theme + AI model

---

## Buttons (Linje 96-139)

### Send Button (Linje 96-107)
```css
body[data-light-theme="true"] #send {
    background: #bdc3c7;
    color: #2c3e50;
    border: 1px solid #95a5a6;
}

body[data-light-theme="true"] #send:hover {
    background: #95a5a6;
    border-color: #7f8c8d;
}
```

#### Colors
- **Background**: `#bdc3c7` - Light gray (189,195,199)
- **Text**: `#2c3e50` - Dark blue-gray (high contrast)
- **Hover**: `#95a5a6` - Darker gray (149,165,166)
  - **Visual feedback** - Gets darker

### Upload Button (Linje 109-118)
```css
body[data-light-theme="true"] #uploadBtn {
    background: #5a6268;
    color: white;
    border: 1px solid #495057;
}

body[data-light-theme="true"] #uploadBtn:hover {
    background: #495057;
    border-color: #343a40;
}
```

#### Dark Gray Theme
- **Background**: `#5a6268` - Dark gray (90,98,104)
- **White text** - High contrast
- **Hover**: `#495057` - Darker (73,80,87)
  - **Invert of light buttons** - Secondary actions darker

### Copy Button (Linje 120-129)
```css
body[data-light-theme="true"] .copy-btn {
    background: #5a6268;
    color: white;
    border: 1px solid #495057;
}

body[data-light-theme="true"] .copy-btn:hover {
    background: #495057;
    border-color: #343a40;
}
```
- **Same styling** - Matches upload button
- **Consistency** - All action buttons similar

### Logout Button (Linje 131-140)
```css
body[data-light-theme="true"] #logout-btn {
    background: #5a6268;
    color: white;
    border: 1px solid #495057;
}

body[data-light-theme="true"] #logout-btn:hover {
    background: #495057;
    border-color: #343a40;
}
```
- **Same styling** - Consistent with other buttons

---

## Headers (Linje 142-149)

```css
body[data-light-theme="true"] #pasted-code-header {
    color: #5a6268;
}

body[data-light-theme="true"] #code-output-header {
    color: #5a6268;
}
```
- **Dark gray text** - `#5a6268`
- **Readable** - Against light panel backgrounds

---

## Feedback & Indicators (Linje 151-166)

### Copy Feedback (Linje 151-154)
```css
body[data-light-theme="true"] .copy-feedback {
    background: #5a6268;
    color: white;
}
```
- **Dark background** - Stands out
- **White text** - High contrast

### Code Indicator (Linje 156-165)
```css
body[data-light-theme="true"] .code-indicator {
    background: #5a6268;
    color: white;
    border: 1px solid #495057;
}

body[data-light-theme="true"] .code-indicator:hover {
    background: #495057;
    border-color: #343a40;
}
```
- **Same as buttons** - Consistent design

---

## Ripple Animation (Linje 167-185)

### Custom Light Ripple (Linje 168-178)
```css
@keyframes ripple-light {
    0% {
        box-shadow: 0 0 0 0 rgba(90, 98, 104, 0);
    }
    50% {
        box-shadow: 0 0 25px 12px rgba(90, 98, 104, 0.7);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(90, 98, 104, 0);
    }
}
```

#### Animation Flow
- **0%**: No shadow (transparent)
- **50%**: Gray glow (70% opacity)
  - **25px blur** - Soft glow
  - **12px spread** - Extends beyond element
  - **Color**: rgba(90, 98, 104, 0.7) - Dark gray
- **100%**: Fade out to transparent

#### Differences from Dark Theme
- **Color**: Gray instead of cyan
- **Duration**: 1.5s (dark theme: 1s) - Slower, gentler
- **Opacity**: 70% (dark might be higher)

### Application (Linje 180-184)
```css
body.light .codeblock.highlight,
body[data-light-theme="true"] .codeblock.highlight {
    animation: ripple-light 1.5s ease-out;
    border-color: #5a6268 !important;
    border-width: 2px !important;
}
```

#### Border Override
- **color**: `#5a6268` - Dark gray (matches buttons)
- **width**: `2px` - Thicker than default 1px
- **!important** - Forces override (JavaScript might set inline styles)

---

## light-quiet-theme.css - Purple Light Theme

### Fil Information
- **Størrelse**: 182 linjer
- **Pattern**: Nearly identical to light-theme.css
- **Color philosophy**: Purple/pink instead of blue/gray
- **Watermark**: Different image (`kali-layers-quiet2.jpeg`)

---

## Key Differences from Standard Light

### Watermark (Linje 2-16)
```css
body[data-theme="light-quiet"]::before {
    background-image: url('/static/images/kali-layers-quiet2.jpeg');
}
```
- **Different image** - "quiet" version (presumably purple-tinted)

### Body Colors (Linje 18-21)
```css
body[data-theme="light-quiet"] {
    background: #f5f0f5;
    color: #4a3a4a;
}
```
- **Background**: `#f5f0f5` - Light purple-pink (245,240,245)
  - **vs Standard**: #f8f9fa (neutral gray)
  - **Purple tint**: Soft, feminine
- **Text**: `#4a3a4a` - Dark purple-gray (74,58,74)
  - **vs Standard**: #2c3e50 (blue-gray)
  - **Warmer**: Purple undertones

### Panel Background (Linje 23-26)
```css
body[data-theme="light-quiet"] #left-panel {
    background: rgba(240, 230, 240, 0.4);
    border-right: 2px solid rgba(150, 120, 150, 0.3);
}
```
- **Background**: rgba(240, 230, 240, 0.4) - Light purple
- **Border**: rgba(150, 120, 150, 0.3) - Purple-gray
- **Consistent theme** - All colors purple-shifted

### User Message (Linje 28-32)
```css
body[data-theme="light-quiet"] .message.user {
    background: rgba(180, 140, 200, 0.08);
    color: #4a3a4a;
    border: 1px solid rgba(150, 120, 180, 0.2);
}
```
- **Background**: rgba(180, 140, 200, 0.08) - Lavender (purple-blue)
  - **vs Standard**: Blue (52,152,219)
- **Border**: Purple-tinted

### Assistant Message (Linje 34-39)
```css
body[data-theme="light-quiet"] .message.assistant {
    background: rgba(255, 240, 245, 0.35);
    color: #4a3a4a;
    border: 1px solid rgba(200, 150, 180, 0.15);
    box-shadow: none;
}
```
- **Background**: rgba(255, 240, 245, 0.35) - Pink-white
- **Border**: Pink-purple

### Code Block Accent (Linje 41-46)
```css
body[data-theme="light-quiet"] .codeblock {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(139, 123, 155, 0.2);
    border-left: 3px solid #8b7b9b;
    box-shadow: none !important;
}
```
- **Border-left**: `#8b7b9b` - Purple-gray (139,123,155)
  - **vs Standard**: #5a6268 (neutral gray)

### Buttons (Throughout)
All buttons use similar gray scheme as standard light theme:
- **Background**: `#8b7b9b` - Purple-gray
- **Hover**: `#7a6a8a` - Darker purple-gray

### Ripple Animation
```css
@keyframes ripple-light-quiet {
    /* Purple-tinted glow instead of gray */
    box-shadow: 0 0 25px 12px rgba(139, 123, 155, 0.7);
}
```

---

## Comparison Table: Light Themes

| Aspect | Standard Light | Light Quiet |
|--------|---------------|-------------|
| **Background** | #f8f9fa (neutral) | #f5f0f5 (purple tint) |
| **Text** | #2c3e50 (blue-gray) | #4a3a4a (purple-gray) |
| **Accent** | Blue (#3498db) | Purple (#b48cc8) |
| **Aesthetic** | Professional, clean | Soft, feminine, calm |
| **Use case** | General purpose | Gentle on eyes, creative work |

---

## Design Philosophy

### Standard Light Theme
- **Professional** - Business/corporate feel
- **Neutral** - Blue accent (universal)
- **High contrast** - Good readability
- **Versatile** - Works for all content types

### Light Quiet Theme
- **Calming** - Purple/pink psychology (creativity, calm)
- **Gentle** - Lower contrast than standard
- **Aesthetic** - More decorative watermark
- **Niche** - For users who prefer softer colors

---

## Common Patterns (Both Themes)

### 1. Extensive !important Usage
```css
box-shadow: none !important;
```
- **Why?** Overriding base.css and Prism.js
- **Trade-off**: Harder to override later, but ensures light theme wins

### 2. rgba() Transparency
```css
background: rgba(255, 255, 255, 0.15);
```
- **Glassmorphism** - Modern UI trend
- **Watermark visible** - Through all panels
- **Depth** - Layered appearance

### 3. Dual Selectors
```css
body.light::before,
body[data-light-theme="true"]::before {
```
- **Backwards compatibility** - Supports old class names
- **Defensive** - Works with multiple activation methods

### 4. No CSS Variables
Unlike dark themes, light themes don't define CSS variables. Instead:
- **Direct color values** - Hardcoded hex/rgba
- **Why?** Light theme is special case (most users prefer dark)
- **Simpler** - No variable management

---

## Watermark Strategy

### Dark Theme (base.css)
```css
body::before {
    background-image: url('kali-layers.png');
    filter: grayscale(100%) brightness(0.8) contrast(1.2);
    opacity: 0.4;
}
```
- **PNG** - Transparency support
- **Filters** - Desaturate and darken
- **Low opacity** - Very subtle

### Light Theme
```css
body[data-light-theme="true"]::before {
    background-image: url('kali-layers-light2.jpeg');
    /* No filters */
    opacity: 0.5;
}
```
- **JPEG** - Photo format (light version pre-processed)
- **No filters** - Image already optimized
- **Higher opacity** - 50% (needs to show on light background)

### Light Quiet Theme
```css
body[data-theme="light-quiet"]::before {
    background-image: url('kali-layers-quiet2.jpeg');
    opacity: 0.5;
}
```
- **Different image** - Purple-tinted version
- **Same opacity** - 50%

---

## Browser Compatibility

### rgba() Colors
- **IE 9+**, **All modern browsers**
- **Fallback**: Could add hex colors before rgba()
  ```css
  background: #f8f9fa; /* Fallback */
  background: rgba(248, 249, 250, 0.4); /* Modern browsers */
  ```

### ::before Pseudo-Element
- **IE 8+** (with :: or : syntax)
- **Universal support**

### !important
- **All browsers** - CSS1 feature (1996)

### @keyframes Animations
- **IE 10+**, **All modern browsers**
- **Degradation**: Animation won't play, but layout works

---

## Performance Notes

### Transparency Overhead
- **Many rgba() rules** - Compositing cost
- **Impact**: Minimal on modern hardware
- **GPU acceleration** - Browsers optimize

### Watermark Image
- **light2.jpeg / quiet2.jpeg** - ~200KB each
- **Loaded once** - Cached by browser
- **Background** - Loads after critical content

### CSS Specificity
- **Long selectors** - `body[data-light-theme="true"] #element`
- **Performance**: Negligible (CSS parsing is fast)

---

## Usage in themes.js

### Activation
```javascript
// themes.js
function applyTheme(themeName) {
    if (themeName === 'light-theme') {
        document.body.setAttribute('data-light-theme', 'true');
        document.body.classList.add('light');
    } else if (themeName === 'light-quiet-theme') {
        document.body.setAttribute('data-theme', 'light-quiet');
    }
}
```

### Watermark Filter Toggle
```javascript
// themes.js
if (lightTheme) {
    document.body.setAttribute('data-light-theme', 'true');
} else {
    document.body.removeAttribute('data-light-theme');
}
```

---

## Konklusion

Light theme files demonstrate advanced CSS override techniques:
- **185 lines** (standard) + **182 lines** (quiet) of overrides
- **Extensive specificity** - Long selectors to beat base.css
- **!important liberally** - Ensures light theme wins
- **rgba() transparency** - Modern glassmorphism effect
- **Custom watermarks** - Light versions of Kali dragon
- **Dual activation** - Supports multiple selector patterns

**Design philosophy:**
- Light themes are special cases (minority preference)
- Override everything with high specificity
- Provide two variants (neutral blue vs calming purple)
- Maintain consistent button/interaction design
- Use transparency to show watermark everywhere

**Maintenance note:** These files are harder to maintain due to !important and specificity. Changes to base.css might not propagate. Consider refactoring to use CSS variables in future.
