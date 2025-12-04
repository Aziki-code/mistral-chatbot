# Prism Syntax Highlighting Themes - Detaljeret Dokumentation

Dokumentation for de 3 Prism.js CSS filer der styler code blocks med syntax highlighting for forskellige programmeringssprog (især Cisco IOS konfig).

---

## cisco-theme.css - Cisco SecureCRT Colors (Dark Theme)

### Fil Information
- **Størrelse**: 88 linjer
- **Formål**: Exact color matching af Cisco SecureCRT terminal
- **Base**: "Kasper-Cisco Words for BlackBckgrd.ini" SecureCRT config
- **Anvendes på**: Cisco IOS commands i dark themes

---

## Header Comment (Linje 1)
```css
/* Cisco SecureCRT exact color matching from Kasper-Cisco Words for BlackBckgrd.ini */
```
- **SecureCRT** - Professionel terminal emulator (Cisco admins' favorit)
- **BlackBckgrd.ini** - Config file med color scheme
- **Exact matching** - Farver kopieret 1:1 fra SecureCRT

---

## Base Colors (Linje 3-7)

```css
code[class*="language-"],
pre[class*="language-"] {
    color: #00ffff;
    background: transparent;
}
```

### Cyan Default Text
- **#00ffff** - Bright cyan (0,255,255)
  - **RGB**: Full green + blue, no red
  - **Matches**: SecureCRT foreground color
  - **Professional**: Terminal aesthetic
- **background: transparent** - Uses parent's background (codeblock in base.css)

### Wildcard Selector
- **class*="language-"** - Matches all Prism language classes
  - `language-python`, `language-cisco`, `language-html`, etc.

---

## Cisco Prompts (Linje 9-13)

### Enable Mode Prompt (Linje 10)
```css
code[class*="language-"] .token.prompt-enable { 
    color: #ffff00; 
    font-weight: bold; 
}
```
- **#ffff00** - Bright yellow (255,255,0)
- **Enable mode** - Privileged exec (`Router#`)
- **Bold** - Indicates elevated privileges
- **SecureCRT color**: #00ffff00 (ABGR format) = #ffff00 (RGB)

### User Mode Prompt (Linje 12-13)
```css
code[class*="language-"] .token.prompt-user { 
    color: #7fffd4; 
}
```
- **#7fffd4** - Aquamarine (127,255,212)
  - **Light green-cyan** - Less important than enable mode
  - **User exec** - Limited privileges (`Router>`)
- **SecureCRT**: #00d4ff7f (ABGR) = #7fffd4 (RGB)

---

## Interface Keywords (Linje 15-17)

```css
code[class*="language-"] .token.interface { color: #ff8800; }
code[class*="language-"] .token.class-name { color: #ff8800; }
```
- **#ff8800** - Bright orange (255,136,0)
- **Tokens**: `.interface`, `.class-name`
- **Examples**:
  ```cisco
  interface GigabitEthernet0/1
  interface Vlan10
  ```
- **Why orange?** Stands out (interfaces are structural elements)

---

## Numbers & Addresses (Linje 19-30)

### IP Addresses (Linje 20)
```css
code[class*="language-"] .token.number { color: #00ff7f; }
```
- **#00ff7f** - Spring green (0,255,127)
- **Examples**: `192.168.1.1`, `10.0.0.0`, `255.255.255.0`
- **SecureCRT**: #007fff00 (ABGR) = #00ff7f (RGB)

### Subnet Masks (Linje 23)
```css
code[class*="language-"] .token.subnet { color: #adff2f; }
```
- **#adff2f** - Green-yellow (173,255,47)
- **Examples**: `/24`, `/30`, `255.255.255.252`
- **SecureCRT**: #002fffad (ABGR) = #adff2f (RGB)

### MAC Addresses (Linje 26)
```css
code[class*="language-"] .token.builtin { color: #ffd700; }
```
- **#ffd700** - Gold (255,215,0)
- **Examples**: `00:1a:2b:3c:4d:5e`, `aabb.ccdd.eeff`
- **SecureCRT**: #0000d7ff (ABGR) = #ffd700 (RGB)

---

## Version Info (Linje 29)

```css
code[class*="language-"] .token.version { color: #ff8c00; }
```
- **#ff8c00** - Dark orange (255,140,0)
- **Examples**: `IOS Version 15.2(4)M3`, `12.4(24)T`
- **SecureCRT**: #00008cff (ABGR) = #ff8c00 (RGB)

---

## Good vs Bad Words (Linje 32-35)

### Good Words (Linje 32)
```css
code[class*="language-"] .token.inserted { color: #00ff40; }
```
- **#00ff40** - Bright green (0,255,64)
- **Examples**: `yes`, `permit`, `up`, `running`
- **Psychology**: Green = OK, allowed, active
- **SecureCRT**: #0040ff00 (ABGR) = #00ff40 (RGB)

### Bad Words (Linje 35-36)
```css
code[class*="language-"] .token.deleted { color: #ff0000; }
code[class*="language-"] .token.keyword.bad { color: #ff0000; }
```
- **#ff0000** - Pure red (255,0,0)
- **Examples**: `no`, `deny`, `down`, `shutdown`, `trunk`
- **Psychology**: Red = stop, forbidden, disabled
- **SecureCRT**: #000000ff (ABGR) = #ff0000 (RGB)

---

## Misc & Important (Linje 38-44)

### Misc Words (Linje 39)
```css
code[class*="language-"] .token.property { color: #ffa500; }
```
- **#ffa500** - Orange (255,165,0)
- **Examples**: `class`, `policy`, `version`, `ID`
- **SecureCRT**: #0000a5ff (ABGR) = #ffa500 (RGB)

### Important Words (Linje 42-43)
```css
code[class*="language-"] .token.important { 
    color: #ff0000; 
    font-weight: bold; 
}
```
- **Red + Bold** - Maximum attention
- **Examples**: `erase`, `delete`, `confirm`
- **Warning**: Destructive commands

---

## Comments & Keywords (Linje 46-49)

### Comments (Linje 47)
```css
code[class*="language-"] .token.comment { color: #00ff7f; }
```
- **#00ff7f** - Spring green (same as IP addresses)
- **Examples**: `! This is a comment`, `remark Allow HTTP`

### Keywords (Linje 50)
```css
code[class*="language-"] .token.keyword { color: #00ffff; }
```
- **#00ffff** - Cyan (default text color)
- **Examples**: `interface`, `switchport`, `description`

---

## Strings (Linje 53)

```css
code[class*="language-"] .token.string { color: #00d7ff; }
```
- **#00d7ff** - Sky blue (0,215,255)
- **Examples**: `"description Sales VLAN"`, `'hostname Router1'`
- **SecureCRT**: #0000d7ff (ABGR) = #00d7ff (RGB)

---

## Operators & Punctuation (Linje 56-58)

```css
code[class*="language-"] .token.operator { color: #00ffff; }
code[class*="language-"] .token.punctuation { color: #00ffff; }
```
- **Cyan** - Same as default text
- **Low importance** - Blends in

---

## Functions (Linje 61)

```css
code[class*="language-"] .token.function { color: #00ffff; }
```
- **Cyan** - For programming languages (not Cisco IOS)

---

## ACLs (Linje 64)

```css
code[class*="language-"] .token.acl { color: #ff8c00; }
```
- **Dark orange** - Access Control Lists
- **Examples**: `access-list 10 permit 192.168.1.0 0.0.0.255`

---

## Security Tokens (Linje 67-69)

```css
code[class*="language-"] .token.credential { color: #ff7f50; }
```
- **#ff7f50** - Coral (255,127,80)
- **Examples**: `username admin password cisco123`, `key 7 encrypted`
- **SecureCRT**: #00507fff (ABGR) = #ff7f50 (RGB)

### WWN (Linje 72)
```css
code[class*="language-"] .token.wwn { color: #ff7f50; }
```
- **WWN** - World Wide Name (Fibre Channel addressing)
- **Same color** - Security-related

---

## Security Zones (Linje 75-84)

### Outside (Linje 76)
```css
code[class*="language-"] .token.outside { color: #00ff40; }
```
- **Bright green** - Internet-facing interface
- **Examples**: `nameif outside`, `security-level 0`

### Inside (Linje 79)
```css
code[class*="language-"] .token.inside { color: #80ff00; }
```
- **#80ff00** - Chartreuse green (128,255,0)
- **Internal network** - Trusted zone
- **SecureCRT**: #0000ff80 (ABGR) = #80ff00 (RGB)

### DMZ (Linje 82)
```css
code[class*="language-"] .token.dmz { color: #00ff00; }
```
- **#00ff00** - Pure green (0,255,0)
- **Demilitarized Zone** - Semi-trusted (web servers)

### Management (Linje 85)
```css
code[class*="language-"] .token.mgmt { color: #53acac; }
```
- **#53acac** - Gray-green (83,172,172)
- **Management interface** - Admin access
- **Muted color** - Less critical
- **SecureCRT**: #00acac53 (ABGR) = #53acac (RGB)

---

## Hitcounts (Linje 88-92)

### Zero Hits (Linje 89)
```css
code[class*="language-"] .token.hitcount-zero { color: #ffffff; }
```
- **White** - Unused ACL entries
- **Warning sign** - Might be misconfigured

### Active Hits (Linje 92)
```css
code[class*="language-"] .token.hitcount-active { color: #ff7f50; }
```
- **Coral** - ACL actively matching traffic

---

## Security Lines (Linje 95)

```css
code[class*="language-"] .token.security { color: #ff7f50; }
```
- **Coral** - Username/password configuration lines

---

## cisco-light-theme.css - Light Theme Variant

### Fil Information
- **Størrelse**: 97 linjer
- **Formål**: Cisco syntax for light backgrounds
- **Pattern**: `code[class*="language-cisco"]` selector (more specific)
- **Strategy**: Darker versions of bright colors

---

## Why Separate File?

### Dark Theme Problem
```css
/* Dark theme - bright colors on black */
color: #00ffff; /* Bright cyan - reads well on black */
```

### Light Theme Solution
```css
/* Light theme - dark colors on white */
color: #006699; /* Dark teal - reads well on white */
```

---

## Color Translation Philosophy

| Dark Theme (cisco-theme.css) | Light Theme (cisco-light-theme.css) | Logic |
|-------------------------------|-------------------------------------|-------|
| #ffff00 (bright yellow) | #cc6600 (dark orange) | Reduce lightness |
| #00ffff (cyan) | #006699 (dark teal) | Darken, reduce saturation |
| #ff0000 (red) | #cc0000 (dark red) | Slight darken |
| #00ff7f (spring green) | #008800 (dark green) | Major darken |

---

## Enable Mode Prompt (Linje 3-7)

```css
code[class*="language-cisco"] .token.prompt-enable,
pre[class*="language-cisco"] .token.prompt-enable { 
    color: #cc6600; 
    font-weight: bold; 
}
```

### Dark Orange
- **#cc6600** - (204,102,0)
- **vs Dark theme**: #ffff00 (bright yellow)
- **Readable** - Dark enough on white background
- **Still bold** - Indicates privilege

---

## User Mode Prompt (Linje 10-13)

```css
code[class*="language-cisco"] .token.prompt-user,
pre[class*="language-cisco"] .token.prompt-user { 
    color: #007766; 
}
```
- **#007766** - Dark teal (0,119,102)
- **vs Dark theme**: #7fffd4 (aquamarine)
- **Muted** - Lower importance than enable mode

---

## Interface Names (Linje 16-21)

```css
code[class*="language-cisco"] .token.interface,
code[class*="language-cisco"] .token.class-name,
pre[class*="language-cisco"] .token.interface,
pre[class*="language-cisco"] .token.class-name { 
    color: #cc5500; 
}
```
- **#cc5500** - Burnt orange (204,85,0)
- **vs Dark theme**: #ff8800
- **Stands out** - But readable on white

---

## IP Addresses (Linje 24-27)

```css
code[class*="language-cisco"] .token.number,
pre[class*="language-cisco"] .token.number { 
    color: #008800; 
}
```
- **#008800** - Dark green (0,136,0)
- **vs Dark theme**: #00ff7f (spring green)
- **High contrast** - Readable against white

---

## Subnet Masks (Linje 30-33)

```css
code[class*="language-cisco"] .token.subnet,
pre[class*="language-cisco"] .token.subnet { 
    color: #669900; 
}
```
- **#669900** - Olive green (102,153,0)
- **vs Dark theme**: #adff2f (green-yellow)
- **Distinct from IPs** - Different green hue

---

## MAC Addresses (Linje 36-39)

```css
code[class*="language-cisco"] .token.builtin,
pre[class*="language-cisco"] .token.builtin { 
    color: #996600; 
}
```
- **#996600** - Dark gold (153,102,0)
- **vs Dark theme**: #ffd700 (gold)
- **Earthy tone** - Professional

---

## IOS Version (Linje 42-45)

```css
code[class*="language-cisco"] .token.version,
pre[class*="language-cisco"] .token.version { 
    color: #cc5500; 
}
```
- **Same as interfaces** - Burnt orange

---

## Good Words (Linje 48-51)

```css
code[class*="language-cisco"] .token.inserted,
pre[class*="language-cisco"] .token.inserted { 
    color: #006600; 
}
```
- **#006600** - Dark forest green (0,102,0)
- **vs Dark theme**: #00ff40 (bright green)
- **Psychology**: Green still means "good"

---

## Bad Words (Linje 54-59)

```css
code[class*="language-cisco"] .token.deleted,
code[class*="language-cisco"] .token.keyword.bad,
pre[class*="language-cisco"] .token.deleted,
pre[class*="language-cisco"] .token.keyword.bad { 
    color: #cc0000; 
}
```
- **#cc0000** - Dark red (204,0,0)
- **vs Dark theme**: #ff0000 (pure red)
- **Psychology**: Red still means "bad"

---

## Misc Words (Linje 62-65)

```css
code[class*="language-cisco"] .token.property,
pre[class*="language-cisco"] .token.property { 
    color: #996633; 
}
```
- **#996633** - Brown (153,102,51)
- **vs Dark theme**: #ffa500 (orange)

---

## Important Words (Linje 68-72)

```css
code[class*="language-cisco"] .token.important,
pre[class*="language-cisco"] .token.important { 
    color: #cc0000; 
    font-weight: bold; 
}
```
- **Dark red + bold** - Maximum warning
- **Same as bad words** - Consistency

---

## Comments (Linje 75-79)

```css
code[class*="language-cisco"] .token.comment,
pre[class*="language-cisco"] .token.comment { 
    color: #008800; 
    font-style: italic;
}
```
- **Dark green** - Same as IP addresses
- **Italic** - Visual distinction from code

---

## Keywords (Linje 82-85)

```css
code[class*="language-cisco"] .token.keyword,
pre[class*="language-cisco"] .token.keyword { 
    color: #0066cc; 
}
```
- **#0066cc** - Dark blue (0,102,204)
- **vs Dark theme**: #00ffff (cyan)
- **Professional** - Blue for commands

---

## Strings (Linje 88-91)

```css
code[class*="language-cisco"] .token.string,
pre[class*="language-cisco"] .token.string { 
    color: #006699; 
}
```
- **#006699** - Dark teal (0,102,153)
- **vs Dark theme**: #00d7ff (sky blue)

---

## Default Cisco Text (Linje 94-97)

```css
code[class*="language-cisco"],
pre[class*="language-cisco"] {
    color: #006699;
}
```
- **Dark teal** - Base color for all Cisco code
- **vs Dark theme**: #00ffff (cyan)

---

## quiet-light-theme.css - VS Code Quiet Light + Cisco

### Fil Information
- **Størrelse**: 171 linjer
- **Formål**: VS Code Quiet Light colors for Python/HTML + Cisco colors for Cisco code
- **Strategy**: Import cisco-light-theme.css, override for other languages
- **Complexity**: Highest (language-specific selectors)

---

## Import Strategy (Linje 3-4)

```css
/* Import Cisco light theme for Cisco code */
@import url('cisco-light-theme.css');
```
- **Loads first** - Cisco colors as base
- **Then override** - For Python, HTML, JavaScript, etc.
- **Advantage**: Reuse Cisco styles, don't repeat

---

## Base Colors (Linje 6-10)

```css
code[class*="language-"],
pre[class*="language-"] {
    color: #333333;
    background: transparent;
}
```
- **#333333** - Dark gray (51,51,51)
- **Default for all** - Then overridden per language
- **vs Cisco**: #006699 (teal) only for Cisco code

---

## VS Code Quiet Light Philosophy

### What is "Quiet Light"?
- **Built-in VS Code theme** - Professional light theme
- **"Quiet"** - Lower contrast than standard light themes
- **Pastel tones** - Gentle on eyes
- **Microsoft design** - Optimized for readability

### Color Palette
- **Comments**: Dark green (#006600)
- **Keywords**: Dark blue (#0000cc)
- **Strings**: Dark red/brown (#8b0000)
- **Numbers**: Dark teal (#076d46)
- **Functions**: Dark yellow/brown (#5f4c1e)

---

## Comments (Linje 15-28)

```css
code[class*="language-python"] .token.comment,
code[class*="language-html"] .token.comment,
code[class*="language-javascript"] .token.comment,
code[class*="language-css"] .token.comment,
code[class*="language-markup"] .token.comment,
pre[class*="language-python"] .token.comment,
pre[class*="language-html"] .token.comment,
pre[class*="language-javascript"] .token.comment,
pre[class*="language-css"] .token.comment,
pre[class*="language-markup"] .token.comment {
    color: #006600;
    font-style: italic;
}
```

### Dark Green Comments
- **#006600** - Dark forest green (0,102,0)
- **Applies to**: Python, HTML, JavaScript, CSS, Markup
- **Not Cisco** - Cisco uses own colors from cisco-light-theme.css
- **Italic** - Visual distinction

### Why Multiple Selectors?
- **Language-specific** - Different Prism language classes
- **Redundancy** - `code` vs `pre` (inline vs block)
- **Ensures coverage** - Works in all contexts

---

## Keywords (Linje 31-41)

```css
code[class*="language-python"] .token.keyword,
code[class*="language-html"] .token.keyword,
code[class*="language-javascript"] .token.keyword,
code[class*="language-markup"] .token.keyword,
pre[class*="language-python"] .token.keyword,
pre[class*="language-html"] .token.keyword,
pre[class*="language-javascript"] .token.keyword,
pre[class*="language-markup"] .token.keyword {
    color: #0000cc;
    font-weight: normal;
}
```

### Dark Blue Keywords
- **#0000cc** - Dark blue (0,0,204)
- **Examples (Python)**: `def`, `class`, `if`, `for`, `import`
- **Examples (JavaScript)**: `function`, `const`, `let`, `var`
- **font-weight: normal** - Not bold (unlike some themes)

---

## Strings (Linje 44-53)

```css
code[class*="language-python"] .token.string,
code[class*="language-html"] .token.string,
code[class*="language-javascript"] .token.string,
code[class*="language-markup"] .token.string,
pre[class*="language-python"] .token.string,
pre[class*="language-html"] .token.string,
pre[class*="language-javascript"] .token.string,
pre[class*="language-markup"] .token.string {
    color: #8b0000;
}
```

### Dark Red Strings
- **#8b0000** - Dark red (139,0,0)
- **Examples**: `"Hello, world!"`, `'api_key'`, `` `template` ``
- **Distinct** - Stands out from keywords

---

## Numbers (Linje 56-65)

```css
code[class*="language-python"] .token.number,
code[class*="language-html"] .token.number,
code[class*="language-javascript"] .token.number,
code[class*="language-markup"] .token.number,
pre[class*="language-python"] .token.number,
pre[class*="language-html"] .token.number,
pre[class*="language-javascript"] .token.number,
pre[class*="language-markup"] .token.number {
    color: #076d46;
}
```

### Dark Teal Numbers
- **#076d46** - Dark teal (7,109,70)
- **Examples**: `42`, `3.14`, `0x1A`, `0b1010`
- **Distinct from IPs** - Different color in Cisco code

---

## Functions (Linje 68-77)

```css
code[class*="language-python"] .token.function,
code[class*="language-html"] .token.function,
code[class*="language-javascript"] .token.function,
code[class*="language-markup"] .token.function,
pre[class*="language-python"] .token.function,
pre[class*="language-html"] .token.function,
pre[class*="language-javascript"] .token.function,
pre[class*="language-markup"] .token.function {
    color: #5f4c1e;
}
```

### Dark Yellow/Brown Functions
- **#5f4c1e** - Dark olive brown (95,76,30)
- **Examples**: `print()`, `len()`, `fetch()`, `addEventListener()`

---

## Classes (Linje 80-89)

```css
code[class*="language-python"] .token.class-name,
code[class*="language-html"] .token.class-name,
code[class*="language-javascript"] .token.class-name,
code[class*="language-markup"] .token.class-name,
pre[class*="language-python"] .token.class-name,
pre[class*="language-html"] .token.class-name,
pre[class*="language-javascript"] .token.class-name,
pre[class*="language-markup"] .token.class-name {
    color: #1e667a;
}
```

### Dark Teal Classes
- **#1e667a** - Dark teal (30,102,122)
- **Examples**: `ChatBot`, `HttpRequest`, `EventEmitter`

---

## Operators (Linje 92-101)

```css
code[class*="language-python"] .token.operator,
code[class*="language-html"] .token.operator,
code[class*="language-javascript"] .token.operator,
code[class*="language-markup"] .token.operator,
pre[class*="language-python"] .token.operator,
pre[class*="language-html"] .token.operator,
pre[class*="language-javascript"] .token.operator,
pre[class*="language-markup"] .token.operator {
    color: #000000;
}
```

### Black Operators
- **#000000** - Pure black
- **Examples**: `+`, `-`, `*`, `/`, `==`, `&&`, `||`
- **Low importance** - Just syntax

---

## Punctuation (Linje 104-113)

```css
code[class*="language-python"] .token.punctuation,
code[class*="language-html"] .token.punctuation,
code[class*="language-javascript"] .token.punctuation,
code[class*="language-markup"] .token.punctuation,
pre[class*="language-python"] .token.punctuation,
pre[class*="language-html"] .token.punctuation,
pre[class*="language-javascript"] .token.punctuation,
pre[class*="language-markup"] .token.punctuation {
    color: #262626;
}
```

### Dark Gray Punctuation
- **#262626** - Very dark gray (38,38,38)
- **Examples**: `(`, `)`, `{`, `}`, `[`, `]`, `,`, `;`
- **Slightly lighter** - Than operators (barely visible difference)

---

## HTML-Specific (Linje 116-150)

### HTML Tags (Linje 118-122)
```css
code[class*="language-html"] .token.tag,
code[class*="language-markup"] .token.tag,
pre[class*="language-html"] .token.tag,
pre[class*="language-markup"] .token.tag {
    color: #660000;
}
```
- **#660000** - Dark maroon (102,0,0)
- **Examples**: `<div>`, `<span>`, `<p>`, `<a>`

### Tag Punctuation (Linje 124-128)
```css
code[class*="language-html"] .token.tag .token.punctuation,
code[class*="language-markup"] .token.tag .token.punctuation,
pre[class*="language-html"] .token.tag .token.punctuation,
pre[class*="language-markup"] .token.tag .token.punctuation {
    color: #660000;
}
```
- **Same color** - `<`, `>`, `</`, `/>`
- **Unified look** - Tag and brackets same

### HTML Attributes (Linje 131-135)
```css
code[class*="language-html"] .token.attr-name,
code[class*="language-markup"] .token.attr-name,
pre[class*="language-html"] .token.attr-name,
pre[class*="language-markup"] .token.attr-name {
    color: #cc0000;
}
```
- **#cc0000** - Bright red (204,0,0)
- **Examples**: `class`, `id`, `href`, `src`
- **Brighter than tags** - More important

### Attribute Values (Linje 138-142)
```css
code[class*="language-html"] .token.attr-value,
code[class*="language-markup"] .token.attr-value,
pre[class*="language-html"] .token.attr-value,
pre[class*="language-markup"] .token.attr-value {
    color: #0000cc;
}
```
- **#0000cc** - Dark blue (same as keywords)
- **Examples**: `"container"`, `"button"`, `"https://..."`

### Doctype (Linje 145-150)
```css
code[class*="language-html"] .token.doctype,
code[class*="language-markup"] .token.doctype,
pre[class*="language-html"] .token.doctype,
pre[class*="language-markup"] .token.doctype {
    color: #666666;
    font-style: italic;
}
```
- **#666666** - Medium gray (102,102,102)
- **Example**: `<!DOCTYPE html>`
- **Italic** - Less important (boilerplate)

---

## Builtins (Linje 153-159)

```css
code[class*="language-python"] .token.builtin,
code[class*="language-javascript"] .token.builtin,
code[class*="language-markup"] .token.builtin,
pre[class*="language-python"] .token.builtin,
pre[class*="language-javascript"] .token.builtin,
pre[class*="language-markup"] .token.builtin {
    color: #005a9a;
}
```
- **#005a9a** - Dark blue (0,90,154)
- **Examples (Python)**: `str`, `int`, `list`, `dict`, `True`, `False`
- **Examples (JS)**: `Array`, `Object`, `Math`, `console`

---

## Python Decorators (Linje 162-165)

```css
code[class*="language-python"] .token.decorator,
pre[class*="language-python"] .token.decorator {
    color: #5f4c1e;
}
```
- **Dark yellow/brown** - Same as functions
- **Examples**: `@app.route`, `@staticmethod`, `@property`

---

## Language Specificity Strategy

### Why So Many Selectors?
```css
code[class*="language-python"] .token.keyword,  /* Inline code */
pre[class*="language-python"] .token.keyword    /* Block code */
```
- **code** - Inline snippets (`this is inline code`)
- **pre** - Code blocks (multi-line)
- **Redundancy** - Ensures coverage

### Prism Language Classes
- **language-python** - `.py` files, Python code
- **language-javascript** - `.js` files, JavaScript code
- **language-html** / **language-markup** - HTML files
- **language-css** - CSS files
- **language-cisco** - Cisco IOS configs (custom)

---

## Comparison: All 3 Prism Themes

| Token Type | cisco-theme.css (Dark) | cisco-light-theme.css (Light) | quiet-light-theme.css (Light) |
|------------|------------------------|-------------------------------|-------------------------------|
| **Default text** | #00ffff (cyan) | #006699 (dark teal) | #333333 (dark gray) |
| **Keywords** | #00ffff (cyan) | #0066cc (dark blue) | #0000cc (dark blue) |
| **Strings** | #00d7ff (sky blue) | #006699 (teal) | #8b0000 (dark red) |
| **Numbers** | #00ff7f (spring green) | #008800 (dark green) | #076d46 (dark teal) |
| **Comments** | #00ff7f (spring green) | #008800 (dark green) | #006600 (dark green) |
| **Functions** | #00ffff (cyan) | #0066cc (dark blue) | #5f4c1e (olive brown) |
| **Scope** | All languages | Cisco only (`language-cisco`) | Python/HTML/JS (non-Cisco) |

---

## Design Philosophy

### cisco-theme.css
- **Purpose**: Exact SecureCRT terminal emulation
- **Target**: Network engineers familiar with Cisco CLI
- **Aesthetic**: Professional terminal, high contrast
- **Psychology**: Colors indicate command types (green=good, red=bad)

### cisco-light-theme.css
- **Purpose**: Cisco syntax for light themes
- **Target**: Same engineers, but prefer light backgrounds
- **Strategy**: Darken all colors for readability
- **Consistency**: Maintains same semantic meaning (orange=interface)

### quiet-light-theme.css
- **Purpose**: VS Code Quiet Light for Python/JS, Cisco for network code
- **Target**: Multi-language developers
- **Strategy**: Import Cisco theme, override for other languages
- **Complexity**: Highest (language-specific rules)

---

## Prism.js Integration

### How Prism Works
1. **JavaScript** - prism-cisco.js tokenizes code
2. **CSS** - These theme files color the tokens
3. **HTML** - `<pre><code class="language-cisco">...</code></pre>`

### Token Creation Example (Python)
```javascript
// prism-cisco.js
Prism.languages.cisco = {
    'prompt-enable': /^.*#/m,
    'interface': /interface\s+\S+/,
    'number': /\d+\.\d+\.\d+\.\d+/,
    // ...
};
```

### CSS Application
```css
/* cisco-theme.css */
.token.prompt-enable { color: #ffff00; }
.token.interface { color: #ff8800; }
.token.number { color: #00ff7f; }
```

### Result
```html
<!-- HTML output -->
<pre><code class="language-cisco">
    <span class="token prompt-enable">Router#</span>
    <span class="token interface">interface GigabitEthernet0/1</span>
    <span class="token keyword">ip</span>
    <span class="token keyword">address</span>
    <span class="token number">192.168.1.1</span>
    <span class="token number">255.255.255.0</span>
</code></pre>
```

---

## Performance Notes

### CSS Specificity
- **Long selectors** - `code[class*="language-python"] .token.keyword`
- **Performance**: Negligible (CSS parsing is fast)
- **Specificity score**: 0,2,1 (2 classes, 1 element)

### File Size
- **cisco-theme.css**: ~3KB uncompressed
- **cisco-light-theme.css**: ~3KB
- **quiet-light-theme.css**: ~5KB (most complex)
- **Total**: ~11KB (minuscule in modern web)

### @import in quiet-light-theme.css
```css
@import url('cisco-light-theme.css');
```
- **Blocks rendering** - Waits for import to load
- **Impact**: Minimal (file tiny, cached)
- **Alternative**: Could inline cisco-light-theme.css

---

## Browser Compatibility

### Attribute Selectors
```css
code[class*="language-"]
```
- **IE 7+**, **All modern browsers**
- **Universal support**

### Descendant Selectors
```css
.token.keyword
```
- **IE 3+** (ancient)
- **No issues**

### CSS Colors (Hex)
```css
color: #00ffff;
```
- **All browsers** - Since CSS1 (1996)

---

## Usage in Application

### Theme Activation (themes.js)
```javascript
function applyCiscoTheme() {
    // cisco-theme.css already loaded via main.css
    // Just ensure Prism uses correct language class
    document.querySelectorAll('code').forEach(block => {
        if (isCiscoConfig(block.textContent)) {
            block.className = 'language-cisco';
            Prism.highlightElement(block);
        }
    });
}
```

### Light Theme Switch
```javascript
function applyLightTheme(themeName) {
    if (themeName === 'light-quiet-theme') {
        // quiet-light-theme.css loaded via main.css
        // Overrides cisco-theme.css for non-Cisco code
    } else {
        // cisco-light-theme.css applies to all Cisco code
    }
}
```

---

## Maintenance Notes

### Adding New Token Type
1. **Update prism-cisco.js** - Define regex pattern
2. **Update cisco-theme.css** - Add color rule
3. **Update cisco-light-theme.css** - Add dark version
4. **Update quiet-light-theme.css** - If applicable to other languages

### Example: Adding VLAN Token
```javascript
// prism-cisco.js
Prism.languages.cisco['vlan'] = /\bvlan\s+\d+\b/;
```

```css
/* cisco-theme.css */
.token.vlan { color: #ff00ff; } /* Magenta */

/* cisco-light-theme.css */
code[class*="language-cisco"] .token.vlan { color: #990099; } /* Dark magenta */
```

---

## Konklusion

Prism theme files implementerer sofistikeret syntax highlighting:

### cisco-theme.css (88 linjer)
- **SecureCRT emulation** - Exact color matching
- **27 token types** - Comprehensive Cisco IOS coverage
- **Color psychology** - Green=good, red=bad, orange=important
- **Professional** - Terminal aesthetic for network engineers

### cisco-light-theme.css (97 linjer)
- **Light theme variant** - Dark colors for white background
- **Same semantic meaning** - Orange still means interface
- **Readable** - High contrast against light background
- **Cisco-specific** - Only applies to `language-cisco` class

### quiet-light-theme.css (171 linjer)
- **Hybrid approach** - VS Code Quiet Light + Cisco colors
- **Multi-language** - Python, HTML, JavaScript, CSS
- **@import strategy** - Reuses cisco-light-theme.css
- **Most complex** - Language-specific selectors throughout

**Total**: 356 linjer CSS til professionel syntax highlighting på tværs af dark/light themes og multiple programmeringssprog.

**Design excellence**: Semantiske farver (ikke tilfældige), terminal emulation (autentisk Cisco oplevelse), og performance optimization (små filer, hurtig parsing).
