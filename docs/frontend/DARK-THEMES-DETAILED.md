# Dark Theme CSS Files - Samlet Dokumentation

Denne dokumentation dækker de 6 simple dark theme filer der alle følger samme mønster: kun CSS variable overrides.

---

## vscode.css - VS Code Dark+ Theme

### Fil Information
- **Størrelse**: 17 linjer
- **Pattern**: CSS variable overrides via `body[data-theme="vscode"]`
- **Inspiration**: Microsoft VS Code Dark+ (default editor theme)

### CSS Variables (Linje 2-16)

```css
body[data-theme="vscode"] {
    --bg-darkest: #1e1e1e;
    --bg-dark: #252526;
    --bg-medium: #2d2d30;
    --border-color: #3e3e42;
    --text-primary: #cccccc;
    --text-secondary: #6a6a6a;
    --accent-primary: #4ec9b0;
    --accent-secondary: #ce9178;
    --button-primary: #0e639c;
    --button-primary-hover: #1177bb;
    --button-secondary: #4ec9b0;
    --scrollbar-thumb: #424242;
    --scrollbar-thumb-hover: #4e4e4e;
}
```

### Color Scheme Analysis

#### Backgrounds
- `--bg-darkest: #1e1e1e` - Nearly black (30,30,30) - Main body background
- `--bg-dark: #252526` - Slightly lighter (37,37,38) - Input fields
- `--bg-medium: #2d2d30` - Medium gray (45,45,48) - Headers, containers
- **Philosophy**: Subtle gradation, minimal contrast jumps

#### Text Colors
- `--text-primary: #cccccc` - Light gray (204,204,204) - Main text
  - **Contrast ratio**: 12.6:1 against #1e1e1e (WCAG AAA compliant)
- `--text-secondary: #6a6a6a` - Medium gray (106,106,106) - Placeholders
  - **Lower contrast**: Indicates secondary importance

#### Accents
- `--accent-primary: #4ec9b0` - Teal/cyan (78,201,176) - **Signature VS Code color**
  - Used for: Highlights, borders, active states
  - **Origin**: VS Code's TypeScript/variable color
- `--accent-secondary: #ce9178` - Peach/orange (206,145,120) - Secondary highlights
  - **Origin**: VS Code's string color

#### Buttons
- `--button-primary: #0e639c` - Blue (14,99,156) - Default buttons
  - **VS Code blue**: Matches editor's button color
- `--button-primary-hover: #1177bb` - Lighter blue (17,119,187) - Hover state
- `--button-secondary: #4ec9b0` - Teal - Secondary actions (matches accent)

#### Scrollbar
- `--scrollbar-thumb: #424242` - Dark gray (66,66,66)
- `--scrollbar-thumb-hover: #4e4e4e` - Slightly lighter (78,78,78)

### Design Philosophy
- **Familiar to developers** - Matches VS Code editor
- **Low contrast** - Easy on eyes during long coding sessions
- **Teal accent** - Instantly recognizable as VS Code
- **Professional** - Microsoft's design language

---

## monokai.css - Monokai Theme

### Fil Information
- **Størrelse**: 17 linjer
- **Inspiration**: Sublime Text's iconic Monokai theme
- **Heritage**: Created by Wimer Hazenberg for Monokai design studio

### CSS Variables

```css
body[data-theme="monokai"] {
    --bg-darkest: #1e1e1e;
    --bg-dark: #272822;
    --bg-medium: #3e3d32;
    --border-color: #49483e;
    --text-primary: #f8f8f2;
    --text-secondary: #75715e;
    --accent-primary: #a6e22e;
    --accent-secondary: #f92672;
    --button-primary: #ae81ff;
    --button-primary-hover: #c49dff;
    --button-secondary: #a6e22e;
    --scrollbar-thumb: #49483e;
    --scrollbar-thumb-hover: #5a5950;
}
```

### Color Scheme Analysis

#### Backgrounds
- `--bg-darkest: #1e1e1e` - Nearly black (30,30,30)
- `--bg-dark: #272822` - Warm dark (39,40,34) - **Slight green tint**
  - **Signature Monokai**: Warm, not pure gray
- `--bg-medium: #3e3d32` - Olive gray (62,61,50) - More pronounced warmth
- `--border-color: #49483e` - Olive border (73,72,62)

#### Text Colors
- `--text-primary: #f8f8f2` - Off-white (248,248,242) - High contrast
  - **Contrast**: 15.8:1 (excellent readability)
- `--text-secondary: #75715e` - Brownish gray (117,113,94) - Comments
  - **Monokai classic**: Comment color

#### Accents
- `--accent-primary: #a6e22e` - Lime green (166,226,46) - **Iconic Monokai green**
  - **High visibility**: Vibrant, stands out
  - **Used for**: Functions, keywords in Sublime
- `--accent-secondary: #f92672` - Hot pink/magenta (249,38,114) - **Signature Monokai pink**
  - **Contrast**: Complements green (color theory: opposite ends)

#### Buttons
- `--button-primary: #ae81ff` - Purple (174,129,255) - **Monokai purple**
  - **Origin**: Constant/number color in Sublime
- `--button-primary-hover: #c49dff` - Lighter purple (196,157,255)
- `--button-secondary: #a6e22e` - Lime green (matches accent)

### Design Philosophy
- **High contrast** - Bold colors, clear distinction
- **Warm tones** - Slight green tint in backgrounds (not cold blue)
- **Color theory** - Green + pink complementary pair
- **Developer favorite** - Sublime Text legacy (2008+)
- **Vibrant** - Energetic, not muted

---

## dracula.css - Dracula Theme

### Fil Information
- **Størrelse**: 17 linjer
- **Created by**: Zeno Rocha (2013)
- **Community**: 300+ ports (VS Code, Sublime, iTerm, etc.)
- **Philosophy**: "One dracula for all"

### CSS Variables

```css
body[data-theme="dracula"] {
    --bg-darkest: #1e1f29;
    --bg-dark: #282a36;
    --bg-medium: #343746;
    --border-color: #44475a;
    --text-primary: #f8f8f2;
    --text-secondary: #6272a4;
    --accent-primary: #bd93f9;
    --accent-secondary: #ff79c6;
    --button-primary: #bd93f9;
    --button-primary-hover: #d4b5ff;
    --button-secondary: #50fa7b;
    --scrollbar-thumb: #44475a;
    --scrollbar-thumb-hover: #565869;
}
```

### Color Scheme Analysis

#### Backgrounds
- `--bg-darkest: #1e1f29` - Dark navy (30,31,41) - **Blue-tinted black**
- `--bg-dark: #282a36` - Dark blue-gray (40,42,54) - **Official Dracula background**
- `--bg-medium: #343746` - Medium navy (52,55,70)
- `--border-color: #44475a` - Blue-gray border (68,71,90)
- **Philosophy**: Cool blue undertones (Gothic night sky)

#### Text Colors
- `--text-primary: #f8f8f2` - Off-white (248,248,242) - **Dracula foreground**
  - Same as Monokai (excellent contrast)
- `--text-secondary: #6272a4` - Blue-gray (98,114,164) - **Dracula comment color**
  - **Distinctive**: More blue than typical comment colors

#### Accents
- `--accent-primary: #bd93f9` - Purple (189,147,249) - **Signature Dracula purple**
  - **Origin**: Dracula's most recognizable color
  - **Used for**: Keywords, functions, highlights
  - **Psychology**: Royal, mysterious (vampire theme)
  
- `--accent-secondary: #ff79c6` - Hot pink (255,121,198) - **Dracula pink**
  - **Vibrant**: High saturation
  - **Contrast**: Complements purple (analogous colors)

#### Buttons
- `--button-primary: #bd93f9` - Purple (matches accent)
- `--button-primary-hover: #d4b5ff` - Lighter purple (212,181,255)
- `--button-secondary: #50fa7b` - Cyan/green (80,250,123) - **Dracula cyan**
  - **Origin**: String/success color in Dracula

### Design Philosophy
- **Gothic aesthetic** - Dark, mysterious (vampire/night theme)
- **Purple dominant** - Regal, fantasy colors
- **Cool tones** - Blue undertones (not warm)
- **Pop culture** - Named after Count Dracula
- **Community favorite** - Huge following (GitHub stars: 20k+)

---

## nord.css - Nord Theme

### Fil Information
- **Created by**: Arctic Ice Studio
- **Philosophy**: Arctic, frost-inspired palette
- **Repository**: github.com/arcticicestudio/nord

### CSS Variables

```css
body[data-theme="nord"] {
    --bg-darkest: #1e1e1e;
    --bg-dark: #2e3440;
    --bg-medium: #3b4252;
    --border-color: #4c566a;
    --text-primary: #eceff4;
    --text-secondary: #81a1c1;
    --accent-primary: #88c0d0;
    --accent-secondary: #8fbcbb;
    --button-primary: #5e81ac;
    --button-primary-hover: #81a1c1;
    --button-secondary: #88c0d0;
    --scrollbar-thumb: #4c566a;
    --scrollbar-thumb-hover: #5a6478;
}
```

### Color Scheme Analysis

#### Backgrounds (Nord Polar Night)
- `--bg-darkest: #1e1e1e` - Nearly black
- `--bg-dark: #2e3440` - **Nord0** - Darkest polar night
- `--bg-medium: #3b4252` - **Nord1** - Dark polar night
- `--border-color: #4c566a` - **Nord3** - Light polar night
- **Name**: "Polar Night" (official Nord terminology)
- **Inspiration**: Arctic winter darkness

#### Text Colors (Nord Snow Storm)
- `--text-primary: #eceff4` - **Nord6** - Bright snow storm
  - **RGB**: (236,239,244) - Very light blue-gray
- `--text-secondary: #81a1c1` - **Nord9** - Frost blue
  - **Calming**: Soft blue (not harsh white)

#### Accents (Nord Frost)
- `--accent-primary: #88c0d0` - **Nord8** - Glacier blue
  - **RGB**: (136,192,208) - Ice blue
  - **Nature**: Frozen water color
  
- `--accent-secondary: #8fbcbb` - **Nord7** - Frost cyan
  - **Subtle difference**: Slightly more cyan than Nord8

#### Buttons (Nord Frost)
- `--button-primary: #5e81ac` - **Nord10** - Arctic blue
  - **Deeper**: More saturated frost color
- `--button-primary-hover: #81a1c1` - **Nord9** - Lighter frost
- `--button-secondary: #88c0d0` - Nord8 (glacier)

### Design Philosophy
- **Arctic inspiration** - Ice, snow, northern lights
- **Calm palette** - Low saturation, soothing
- **Blue spectrum** - Cold tones exclusively
- **Nature-based** - Real Arctic colors
- **Consistent**: All colors from 16-color palette

---

## solarized.css - Solarized Dark Theme

### Fil Information
- **Created by**: Ethan Schoonover (2011)
- **Philosophy**: Precision colors based on HSB color wheel
- **Science**: Lab-tested for optimal contrast and eye strain reduction

### CSS Variables

```css
body[data-theme="solarized"] {
    --bg-darkest: #001e1e;
    --bg-dark: #002b36;
    --bg-medium: #073642;
    --border-color: #586e75;
    --text-primary: #839496;
    --text-secondary: #586e75;
    --accent-primary: #b58900;
    --accent-secondary: #cb4b16;
    --button-primary: #268bd2;
    --button-primary-hover: #4ca3e8;
    --button-secondary: #2aa198;
    --scrollbar-thumb: #586e75;
    --scrollbar-thumb-hover: #657b83;
}
```

### Color Scheme Analysis

#### Backgrounds (Solarized Base)
- `--bg-darkest: #001e1e` - Near black with teal tint
- `--bg-dark: #002b36` - **Base03** - Darkest Solarized background
  - **RGB**: (0,43,54) - Deep blue-green
- `--bg-medium: #073642` - **Base02** - Background highlights
  - **RGB**: (7,54,66) - Slightly lighter blue-green
- `--border-color: #586e75` - **Base01** - Optional emphasized content
  - **Contrast**: Visible against Base02/03

#### Text Colors (Solarized Content)
- `--text-primary: #839496` - **Base0** - Body text
  - **RGB**: (131,148,150) - Neutral gray-blue
  - **Science**: Tested for minimum eye strain
  
- `--text-secondary: #586e75` - **Base01** - Comments, secondary
  - **Lower contrast**: Less prominent

#### Accents (Solarized Accent Colors)
- `--accent-primary: #b58900` - **Yellow** - Primary accent
  - **RGB**: (181,137,0) - Warm yellow
  - **Unique**: Most Solarized themes use this for keywords
  
- `--accent-secondary: #cb4b16` - **Orange** - Secondary accent
  - **RGB**: (203,75,22) - Earthy orange

#### Buttons (Solarized Accents)
- `--button-primary: #268bd2` - **Blue** - Solarized blue
  - **RGB**: (38,139,210) - Vibrant blue
- `--button-primary-hover: #4ca3e8` - Lighter blue
- `--button-secondary: #2aa198` - **Cyan** - Solarized cyan
  - **RGB**: (42,161,152) - Teal-cyan

### Design Philosophy
- **Scientific approach** - HSB color wheel precision
- **Eye strain reduction** - Lab-tested contrasts
- **Warm accents** - Yellow/orange (not cool blues)
- **Unique**: Brown/orange tones unusual for dark themes
- **Symmetric**: Light/dark versions use same accent colors

---

## github.css - GitHub Dark Theme

### Fil Information
- **Inspiration**: GitHub's official dark mode (2020+)
- **Modern**: Introduced with GitHub redesign

### CSS Variables

```css
body[data-theme="github"] {
    --bg-darkest: #0a0c0f;
    --bg-dark: #0d1117;
    --bg-medium: #161b22;
    --border-color: #30363d;
    --text-primary: #c9d1d9;
    --text-secondary: #8b949e;
    --accent-primary: #58a6ff;
    --accent-secondary: #79c0ff;
    --button-primary: #238636;
    --button-primary-hover: #2ea043;
    --button-secondary: #58a6ff;
    --scrollbar-thumb: #484f58;
    --scrollbar-thumb-hover: #6e7681;
}
```

### Color Scheme Analysis

#### Backgrounds
- `--bg-darkest: #0a0c0f` - Almost pure black (10,12,15)
  - **Darkest**: More black than other themes
- `--bg-dark: #0d1117` - **GitHub canvas-default** - Main background
  - **RGB**: (13,17,23) - Very dark blue-black
- `--bg-medium: #161b22` - **GitHub canvas-subtle** - Elevated surfaces
- `--border-color: #30363d` - **GitHub border-default** - Subtle borders

#### Text Colors
- `--text-primary: #c9d1d9` - **GitHub fg-default** - Main text
  - **RGB**: (201,209,217) - Light blue-gray
- `--text-secondary: #8b949e` - **GitHub fg-muted** - Secondary text
  - **RGB**: (139,148,158) - Muted gray

#### Accents
- `--accent-primary: #58a6ff` - **GitHub accent-fg** - Links, highlights
  - **RGB**: (88,166,255) - Bright blue
  - **Signature**: GitHub's blue (recognizable)
  
- `--accent-secondary: #79c0ff` - **GitHub accent-emphasis** - Lighter blue
  - **Usage**: Hover states, emphasized items

#### Buttons
- `--button-primary: #238636` - **GitHub success-emphasis** - Green
  - **RGB**: (35,134,54) - GitHub green
  - **Used for**: Primary actions (like commit button)
- `--button-primary-hover: #2ea043` - Lighter green
- `--button-secondary: #58a6ff` - Blue (matches accent)

### Design Philosophy
- **Familiar**: Matches github.com dark mode exactly
- **Brand colors**: GitHub green for primary actions
- **Minimal distraction**: Very dark, high contrast
- **Professional**: Corporate design language
- **Modern**: Introduced with 2020 redesign

---

## Theme Comparison Table

| Theme | Primary Accent | Philosophy | Inspiration |
|-------|---------------|------------|-------------|
| **VS Code** | Teal (#4ec9b0) | Professional, familiar | Microsoft editor |
| **Monokai** | Lime green (#a6e22e) | Vibrant, high contrast | Sublime Text |
| **Dracula** | Purple (#bd93f9) | Gothic, mysterious | Vampire theme |
| **Nord** | Glacier blue (#88c0d0) | Arctic, calm | Frozen nature |
| **Solarized** | Yellow (#b58900) | Scientific, warm | Lab-tested colors |
| **GitHub** | Bright blue (#58a6ff) | Clean, professional | GitHub website |

---

## Usage Pattern (All Themes)

### Activation
```javascript
// themes.js
function applyTheme(themeName) {
    document.body.setAttribute('data-theme', themeName);
}
```

### CSS Cascade
```
1. base.css defines :root variables (Cisco defaults)
2. User selects theme → themes.js calls applyTheme()
3. body[data-theme="vscode"] selector matches
4. CSS variables override :root values
5. All var(--variable) references update instantly
6. UI recolors without re-render
```

### Why body[data-theme] vs body.theme-name?
- **Consistency**: All dark themes use same pattern
- **CSS specificity**: `body[data-theme="x"]` beats `:root`
- **JavaScript**: `setAttribute` cleaner than `classList.add`
- **Semantic**: data-theme is descriptive attribute

---

## Konklusion

Alle 6 dark theme filer følger identisk struktur:
- **15-17 linjer** hver
- **CSS variables only** - No style rules
- **body[data-theme="name"]** selector
- **Instant theme switching** - No page reload
- **Community themes** - Beloved by developers globally

**Design diversity:**
- Cool tones: VS Code, Nord, GitHub (blues/cyans)
- Warm tones: Monokai, Solarized (greens/yellows)
- Fantasy: Dracula (purples/pinks)

**Shared philosophy:**
- Dark backgrounds (easier on eyes)
- High contrast text (readability)
- Vibrant accents (visual interest)
- Professional appearance (not garish)
