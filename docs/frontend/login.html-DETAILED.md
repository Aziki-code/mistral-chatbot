# login.html - Detaljeret Dokumentation

## Overordnet Formål
`login.html` er login-siden med "Demon Hunter" tema inspireret af Illidan fra World of Warcraft. Den håndterer bruger authentication via LDAP og indeholder avancerede CSS animationer (particles, scanline, gradient effects).

---

## Filstruktur

### 1. DOCTYPE og HEAD (Linje 1-7)
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AzikiAI - Demon Hunter Protocol</title>
```
- Standard HTML5 struktur
- **Title**: "Demon Hunter Protocol" - tematisk navn (reference til Illidan Stormrage)
- Viewport meta tag for mobile responsiveness

---

### 2. STYLE Sektion (Linje 7-256)

#### Font Import (Linje 8)
```css
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');
```
- **Orbitron**: Futuristisk sci-fi font til headings (firkantet, teknisk udseende)
- **Share Tech Mono**: Monospace font til labels og tekst (terminal/kode stil)
- `display=swap`: Viser fallback font først, switcher når custom fonts loader (forbedrer performance)

#### Reset Styles (Linje 10-14)
```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
```
- **Linje 11-12**: Fjerner browser default margins og padding på ALLE elementer
- **Linje 13**: `box-sizing: border-box` - padding og border inkluderes i width/height (lettere at regne med)

#### Body Base Styling (Linje 16-24)
```css
body {
    font-family: 'Share Tech Mono', monospace;
    background: #1a1d2e;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    position: relative;
}
```
- **Linje 17**: Default font til hele siden (monospace cyber-tema)
- **Linje 18**: Mørk blå-grå baggrund (#1a1d2e)
- **Linje 19**: `100vh` = 100% af viewport height (fylder hele skærmen)
- **Linje 20-22**: Flexbox centrerer login box både horisontalt og vertikalt
- **Linje 23**: `overflow: hidden` skjuler scrollbars (forhindrer particles i at skabe overflow)
- **Linje 24**: `position: relative` gør body til positioning context for absolute children

#### Kali Dragon Background (Linje 27-42)
```css
body::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: url('/static/images/kali-layers.png');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    opacity: 0.4;
    z-index: 0;
    filter: grayscale(100%) brightness(0.8) contrast(1.2);
}
```
- **Linje 27**: `::after` pseudo-element - ekstra layer OVEN PÅ body
- **Linje 28**: `content: ''` - tom content (kræves for at vise pseudo-element)
- **Linje 29-33**: Position absolute fylder hele viewport (0,0 til 100%,100%)
- **Linje 34**: Kali dragon baggrundsbillede
- **Linje 35**: `cover` - skalerer billede til at fylde hele skærmen (crop hvis nødvendigt)
- **Linje 36**: Centrerer billede
- **Linje 37**: Ingen tiling
- **Linje 38**: `opacity: 0.4` - 40% synlighed (subtil watermark)
- **Linje 39**: `z-index: 0` - bag andre elementer
- **Linje 40**: **Filters**:
  - `grayscale(100%)` - sort/hvid billede
  - `brightness(0.8)` - 20% mørkere
  - `contrast(1.2)` - 20% mere kontrast (skarpere kanter)

#### Dark Overlay for Readability (Linje 45-54)
```css
body::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(ellipse at center, rgba(30, 30, 35, 0.5) 0%, rgba(15, 15, 18, 0.85) 100%);
    z-index: 1;
}
```
- **Linje 45**: `::before` pseudo-element - ekstra layer UNDER body
- **Linje 52**: **Radial gradient**:
  - `ellipse at center` - oval gradient fra centrum
  - Start: `rgba(30, 30, 35, 0.5)` - 50% transparent grå i centrum (lysere)
  - Slut: `rgba(15, 15, 18, 0.85)` - 85% opaque sort i kanterne (mørkere)
  - Skaber spotlight effect - centrum er lysere, kanter mørkere
- **Linje 53**: `z-index: 1` - oven på `::after` (dragen), under login container

**Z-index layers:**
0. body::after (dragon image) - z-index: 0
1. body::before (dark overlay) - z-index: 1
2. .particles - z-index: 1
3. .login-container - z-index: 3
4. .scanline - z-index: 10

#### Pulse Animation (Linje 56-59)
```css
@keyframes pulse {
    0%, 100% { opacity: 0.3; }
    50% { opacity: 0.6; }
}
```
- Animation definition (bruges ikke i denne fil, men defineret for fremtidig brug)
- 0% og 100%: 30% opacity (fade out)
- 50%: 60% opacity (fade in)
- Skaber pulserende glow effect

#### Login Container Base (Linje 62-77)
```css
.login-container {
    position: relative;
    z-index: 3;
    background: rgba(25, 28, 32, 0.9);
    backdrop-filter: blur(15px);
    padding: 45px;
    border-radius: 20px;
    border: 2px solid rgba(100, 105, 110, 0.4);
    box-shadow: 0 0 40px rgba(80, 85, 90, 0.5),
                inset 0 0 30px rgba(150, 155, 160, 0.08);
    width: 450px;
    max-width: 90%;
    margin-left: auto;
    margin-right: 8%;
}
```
- **Linje 63-64**: Relative positioning, z-index 3 (oven på overlays)
- **Linje 65**: **Background**: `rgba(25, 28, 32, 0.9)` - 90% opaque mørk grå (næsten sort, lidt gennemsigtig)
- **Linje 66**: **backdrop-filter blur** - blurrer baggrunden BAG containeren (glassmorphism effect)
  - Kræver moderne browser (ikke IE)
  - Skaber frosted glass look
- **Linje 67**: 45px padding indeni
- **Linje 68**: 20px rounded corners
- **Linje 69**: 2px solid border, semi-transparent grå
- **Linje 70-71**: **Box shadows**:
  - `0 0 40px rgba(80, 85, 90, 0.5)` - Outer glow (grå halo omkring container)
  - `inset 0 0 30px rgba(150, 155, 160, 0.08)` - Inner glow (subtil lys inden i kanter)
- **Linje 72**: 450px bredde
- **Linje 73**: `max-width: 90%` - på små skærme, max 90% af viewport
- **Linje 74-75**: **Positioning**:
  - `margin-left: auto` - skubber til højre
  - `margin-right: 8%` - 8% margin fra højre kant
  - Resultat: Box er offset til højre (ikke helt centreret)

#### Login Header (Linje 79-109)
```css
.login-header {
    text-align: center;
    margin-bottom: 35px;
}

.login-header h1 {
    font-family: 'Orbitron', sans-serif;
    font-size: 32px;
    font-weight: 900;
    background: linear-gradient(135deg, #b8bcc2 0%, #70757a 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
    text-shadow: 0 0 20px rgba(120, 125, 130, 0.5);
    letter-spacing: 2px;
}
```
- **H1 Styling**:
  - **Linje 84**: Orbitron font (futuristisk)
  - **Linje 86**: `font-weight: 900` - ekstra bold (Black weight)
  - **Linje 87**: **Linear gradient** - lys grå til mørk grå, 135° diagonal
  - **Linje 88-89**: **Gradient text trick**:
    - `background-clip: text` - clipper gradient til kun tekst
    - `text-fill-color: transparent` - gør tekst transparent, viser gradient
    - Resultat: Tekst har gradient fill i stedet for solid farve
  - **Linje 91**: `text-shadow` - grå glow omkring tekst
  - **Linje 92**: `letter-spacing: 2px` - ekstra spacing mellem bogstaver (epic titel look)

```css
.login-header .subtitle {
    color: #a0a5aa;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 3px;
    opacity: 0.8;
}
```
- **Subtitle**: "◈ Demon Hunter Access ◈"
  - Lys grå farve
  - Små versaler (uppercase)
  - 3px letter spacing (spredt ud)
  - 80% opacity (semi-transparent)

```css
.login-header .tagline {
    color: rgba(140, 145, 150, 0.8);
    font-size: 11px;
    margin-top: 5px;
    font-style: italic;
}
```
- **Tagline**: "You are not prepared... to login"
  - Reference til Illidan quote "You are not prepared!"
  - Italic, lille font, semi-transparent

#### Form Group Base (Linje 111-123)
```css
.form-group {
    margin-bottom: 25px;
    position: relative;
}

.form-group label {
    display: block;
    margin-bottom: 10px;
    color: #c0c5ca;
    font-weight: 600;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
```
- **form-group**: Container for label + input
  - 25px spacing mellem groups
  - `position: relative` for absolute positioned children (hvis nødvendigt)
- **Label styling**:
  - `display: block` - fylder hele bredde (input starter på ny linje)
  - Lys grå farve
  - Semi-bold (600 weight)
  - Små uppercase bogstaver
  - Letter spacing for cyber-look

#### Input Fields (Linje 125-148)
```css
.form-group input {
    width: 100%;
    padding: 14px 16px;
    background: rgba(20, 22, 25, 0.6);
    border: 2px solid rgba(100, 105, 110, 0.4);
    border-radius: 8px;
    color: #d0d5da;
    font-size: 15px;
    font-family: 'Share Tech Mono', monospace;
    transition: all 0.3s ease;
}

.form-group input::placeholder {
    color: rgba(120, 125, 130, 0.5);
}

.form-group input:focus {
    outline: none;
    border-color: #8090a0;
    box-shadow: 0 0 15px rgba(120, 130, 140, 0.5),
                inset 0 0 10px rgba(160, 165, 170, 0.1);
}
```
- **Input base**:
  - **Linje 126**: 100% bredde
  - **Linje 127**: 14px vertikal, 16px horisontal padding
  - **Linje 128**: Næsten sort baggrund, 60% opacity (gennemsigtig)
  - **Linje 129**: 2px border, semi-transparent grå
  - **Linje 130**: 8px rounded corners
  - **Linje 131**: Lys grå text color
  - **Linje 133**: Monospace font (terminal-stil)
  - **Linje 134**: `transition: all 0.3s ease` - animerer ALLE property changes over 0.3 sekunder

- **Placeholder text**:
  - 50% transparent grå
  - Vises når input er tom

- **Focus state** (når bruger klikker i input):
  - **Linje 143**: `outline: none` - fjerner browser default blå outline
  - **Linje 144**: Border bliver lysere grå (#8090a0)
  - **Linje 145-146**: **Box shadows**:
    - `0 0 15px rgba(120, 130, 140, 0.5)` - Outer glow (grå halo)
    - `inset 0 0 10px rgba(160, 165, 170, 0.1)` - Inner glow (subtil lys inden i)
  - Resultat: Input "lyser op" når aktiv

#### Error Message (Linje 150-158)
```css
.error-message {
    background: rgba(255, 0, 100, 0.1);
    border: 1px solid rgba(255, 0, 100, 0.4);
    color: #ff0066;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 20px;
    font-size: 13px;
    text-align: center;
}
```
- **Pink/rød error styling**:
  - **Linje 151**: Baggrund: pink med 10% opacity
  - **Linje 152**: Border: pink med 40% opacity
  - **Linje 153**: Tekst: bright pink (#ff0066)
  - Centreret tekst, lille font
- Vises kun hvis Jinja2 `{% if error %}` er true

#### Login Button (Linje 160-186)
```css
.login-button {
    width: 100%;
    padding: 16px;
    background: linear-gradient(135deg, #606570 0%, #4a4f58 100%);
    color: #f0f2f5;
    border: 2px solid rgba(120, 125, 130, 0.5);
    border-radius: 8px;
    font-size: 16px;
    font-weight: 700;
    font-family: 'Orbitron', sans-serif;
    text-transform: uppercase;
    letter-spacing: 2px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 0 20px rgba(100, 105, 110, 0.4);
}

.login-button:hover {
    background: linear-gradient(135deg, #707580 0%, #5a5f68 100%);
    transform: translateY(-2px);
    box-shadow: 0 0 30px rgba(120, 125, 130, 0.6),
                0 5px 20px rgba(100, 105, 110, 0.3);
}

.login-button:active {
    transform: translateY(0);
}
```
- **Base button**:
  - **Linje 163**: Gradient baggrund - lys grå til mørk grå diagonal
  - **Linje 164**: Næsten hvid text
  - **Linje 165**: Semi-transparent border
  - **Linje 169**: Orbitron font (matcher h1)
  - **Linje 170**: Uppercase (versaler)
  - **Linje 171**: Letter spacing (epic button look)
  - **Linje 172**: `cursor: pointer` - hånd cursor ved hover
  - **Linje 174**: Box shadow glow

- **Hover state**:
  - **Linje 177**: Lysere gradient
  - **Linje 178**: `translateY(-2px)` - flytter button 2px op (lift effect)
  - **Linje 179-180**: Stærkere glow + shadow under button
  - Resultat: Button "hæver sig" ved hover

- **Active state** (klikket):
  - **Linje 184**: `translateY(0)` - tilbage til normal position
  - Resultat: Button "trykkes ned" ved klik

#### Domain Info Box (Linje 188-198)
```css
.domain-info {
    text-align: center;
    margin-top: 20px;
    padding: 12px;
    background: rgba(150, 155, 160, 0.08);
    border: 1px solid rgba(120, 125, 130, 0.3);
    border-radius: 8px;
    font-size: 12px;
    color: #b0b5ba;
    font-weight: 600;
}
```
- Lille info box der viser "🛡 SECURED REALM: Area51.local"
- Semi-transparent baggrund
- Border og rounded corners
- Centreret tekst

#### Login Footer (Linje 200-205)
```css
.login-footer {
    text-align: center;
    margin-top: 20px;
    color: rgba(140, 145, 150, 0.6);
    font-size: 11px;
    letter-spacing: 1px;
}
```
- "Powered by Kali Dragon AI • Mistral Core • GitHub Sentinel"
- Meget lille, transparent tekst
- Subtil branding

#### Scanline Animation (Linje 208-227)
```css
.scanline {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(to bottom, 
        transparent 0%, 
        rgba(0, 255, 136, 0.03) 50%, 
        transparent 100%);
    animation: scan 8s linear infinite;
    pointer-events: none;
    z-index: 10;
}

@keyframes scan {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
}
```
- **Scanline div**:
  - Fylder hele viewport (absolute positioning)
  - **Linje 214-217**: **Vertical gradient**:
    - Top: Transparent
    - Midt: Svag grøn (#00ff88) med 3% opacity
    - Bund: Transparent
  - **Linje 218**: Animation "scan" 8 sekunder, linear timing, infinite loop
  - **Linje 219**: `pointer-events: none` - klik går igennem (ikke interactive)
  - **Linje 220**: `z-index: 10` - oven på ALT (scanline overlay effect)

- **Scan animation**:
  - **Linje 224**: Start position: `translateY(-100%)` - helt over skærmen (usynlig)
  - **Linje 225**: Slut position: `translateY(100%)` - helt under skærmen (usynlig)
  - Resultat: Grøn linje glider langsomt ned over skærmen (CRT monitor/hacker terminal effect)

#### Particle System (Linje 230-256)
```css
.particles {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    z-index: 1;
    pointer-events: none;
}

.particle {
    position: absolute;
    width: 2px;
    height: 2px;
    background: #a0a5aa;
    border-radius: 50%;
    opacity: 0.3;
    animation: float 20s infinite;
}

@keyframes float {
    0% { transform: translateY(100vh) translateX(0); opacity: 0; }
    10% { opacity: 0.3; }
    90% { opacity: 0.3; }
    100% { transform: translateY(-100vh) translateX(100px); opacity: 0; }
}
```
- **Particles container**:
  - Fylder hele viewport
  - `overflow: hidden` - particles går ikke uden for skærmen
  - `pointer-events: none` - ikke clickable
  - `z-index: 1` - samme layer som dark overlay

- **Individual particle**:
  - **Linje 244-245**: 2x2 pixel kvadrat
  - **Linje 246**: Lys grå farve
  - **Linje 247**: `border-radius: 50%` - gør kvadrat til cirkel
  - **Linje 248**: 30% opacity (subtil)
  - **Linje 249**: Float animation 20 sekunder, infinite

- **Float animation**:
  - **Linje 252**: Start: Bund af skærm (100vh), X=0, invisible
  - **Linje 253**: 10% inde i animation: fade in til 30% opacity
  - **Linje 254**: 90% inde: stadig 30% opacity
  - **Linje 255**: Slut: Top af skærm (-100vh), X=100px til højre, fade out
  - Resultat: Particles floater langsomt opad med slight horizontal drift, fade in/out

---

### 3. BODY Sektion (Linje 258-313)

#### Particles (Linje 260-271)
```html
<div class="particles">
    <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
    <div class="particle" style="left: 20%; animation-delay: 3s;"></div>
    <div class="particle" style="left: 30%; animation-delay: 6s;"></div>
    ...
</div>
```
- **9 particles** placeret på forskellige X-positions (10%, 20%, ..., 90%)
- **animation-delay**: Hver particle starter på forskellige tidspunkter (0s, 3s, 6s, ...)
  - Skaber staggered effect - ikke alle particles starter samtidig
  - Giver mere naturlig, random look

#### Login Container (Linje 274-310)
```html
<div class="login-container">
    <div class="login-header">
        <h1>AZIKI-AI PROTOCOL</h1>
        <div class="subtitle">◈ Demon Hunter Access ◈</div>
        <div class="tagline">"You are not prepared... to login"</div>
    </div>
```
- **H1**: "AZIKI-AI PROTOCOL" - main title
- **Subtitle**: ◈ symboler (diamond shapes) omkring "Demon Hunter Access"
- **Tagline**: Illidan quote parody

#### Error Handling (Linje 282-286)
```html
{% if error %}
<div class="error-message">
    ⚠ ACCESS DENIED: {{ error }}
</div>
{% endif %}
```
- **Jinja2 conditional** - vises kun hvis Flask sender `error` variable
- `{{ error }}` - indsætter error besked fra backend (f.eks. "Invalid credentials")
- ⚠ warning emoji for visuelt alert

#### Login Form (Linje 288-302)
```html
<form method="POST" action="/login">
    <div class="form-group">
        <label for="username">⟨ HUNTER ID ⟩</label>
        <input type="text" id="username" name="username" placeholder="Enter demon hunter credentials" required autofocus>
    </div>

    <div class="form-group">
        <label for="password">⟨ CIPHER KEY ⟩</label>
        <input type="password" id="password" name="password" placeholder="Enter encryption key" required>
    </div>

    <button type="submit" class="login-button">⟨ INITIATE PROTOCOL ⟩</button>
</form>
```
- **Form attributes**:
  - `method="POST"` - sender data via HTTP POST (sikker for passwords)
  - `action="/login"` - sender til Flask route `/login`

- **Username field**:
  - **Label**: "⟨ HUNTER ID ⟩" - tematisk navn for username (⟨ ⟩ er angle brackets)
  - **Input**:
    - `type="text"` - normal text input
    - `name="username"` - Flask modtager som `request.form['username']`
    - `required` - HTML5 validation (skal udfyldes)
    - `autofocus` - cursor starter her når siden loader

- **Password field**:
  - **Label**: "⟨ CIPHER KEY ⟩" - tematisk navn for password
  - **Input**:
    - `type="password"` - skjuler indtastet tekst (vises som bullets)
    - `name="password"` - Flask modtager som `request.form['password']`
    - `required` - skal udfyldes

- **Submit button**:
  - `type="submit"` - trigger form submission
  - Text: "⟨ INITIATE PROTOCOL ⟩" - tematisk action

#### Domain Info og Footer (Linje 304-310)
```html
<div class="domain-info">
    🛡 SECURED REALM: Area51.local
</div>

<div class="login-footer">
    Powered by Kali Dragon AI • Mistral Core • GitHub Sentinel
</div>
```
- **Domain info**: Viser LDAP domain navn (Area51.local)
- **Footer**: Credits til AI providers
  - Kali Dragon (projekt navn)
  - Mistral (AI model)
  - GitHub Sentinel (Copilot reference)

#### Scanline Effect (Linje 313)
```html
<div class="scanline"></div>
```
- Aktiverer CRT scanline animation over hele siden

---

## Dataflow og Backend Integration

### 1. Initial Load (`GET /login`):
```
Browser → Flask route /login (GET) → render_template('login.html') → Viser form
```
- Flask's `render_template()` loader login.html
- Ingen error variable sendes → error box vises ikke

### 2. Form Submission (`POST /login`):
```
User fylder form → Trykker "INITIATE PROTOCOL" → POST til /login
→ bot.py håndterer form data
→ LDAP authentication check
→ Success: redirect til / (index.html)
→ Failure: render login.html med error message
```

**I bot.py (login route):**
```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']  # Fra input name="username"
        password = request.form['password']  # Fra input name="password"
        
        # LDAP authentication logic
        if authenticate_ldap(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect('/')
        else:
            error = "Invalid credentials"
            return render_template('login.html', error=error)  # Sender error til template
    
    return render_template('login.html')
```

### 3. Error Display:
```
Flask sender error="Invalid credentials" → Jinja2 {% if error %} → Viser pink error box
```

---

## Security Features

1. **Password masking**: `type="password"` skjuler indtastet tekst
2. **POST method**: Sensitive data ikke i URL (ikke logged i server access logs)
3. **Required fields**: HTML5 validation forhindrer tom submission
4. **LDAP authentication**: Centraliseret user management (bot.py håndterer)
5. **Session management**: Flask session tracker login state
6. **No client-side validation**: Alt validering sker på backend (ikke trustable client-side)

---

## Animation Performance

### Optimeringsteknikker:
1. **CSS animations** (ikke JavaScript) - hardware accelerated, smooth 60fps
2. **transform property** - GPU accelerated (translateY brugt i stedet for top/bottom)
3. **pointer-events: none** - particles og scanline ikke clickable (browser ignorer dem i event handling)
4. **will-change** kunne tilføjes for yderligere optimization (ikke implementeret endnu)

### Animation load:
- **Scanline**: 1 element, simpel vertical transform - neglible performance impact
- **Particles**: 9 elements, hver med float animation - minimal impact (moderne browsers håndterer dette let)
- **Backdrop-filter**: Kan være performance-heavy på ældre hardware - fallback: background color

---

## Responsive Design

### Mobile Considerations:
- **Viewport meta tag** - korrekt scaling på mobile
- **max-width: 90%** - container bliver mindre på små skærme
- **Flexbox centering** - automatisk justering
- **Relative font sizes** - tekst skalerer proportionalt

### Potential Improvements:
```css
@media (max-width: 768px) {
    .login-container {
        margin-right: auto;  /* Centrer i stedet for offset */
        padding: 30px;       /* Mindre padding */
    }
    
    .particles { display: none; }  /* Deaktiver particles på mobile (performance) */
}
```

---

## Browser Compatibility

### Modern Features:
1. **backdrop-filter** - Chrome 76+, Safari 9+, Firefox 103+ (fallback: solid background)
2. **background-clip: text** - Chrome 4+, Safari 4+, Firefox 49+ (fallback: solid text color)
3. **CSS animations** - All modern browsers
4. **Flexbox** - IE 11+, all modern browsers
5. **::before/::after** - All browsers

### Fallbacks:
- Browsers uden backdrop-filter: Viser solid background (stadig pænt)
- Browsers uden gradient text: Viser solid farve
- IE 11: Fungerer men uden avancerede effects

---

## Konklusion

`login.html` er en standalone fil (ingen eksterne CSS/JS) med:
- **Tematisk design** inspireret af Illidan/Demon Hunter
- **Avancerede animations** (scanline, particles, gradients)
- **Sikker authentication** via Flask + LDAP
- **Responsive layout** med flexbox
- **Glassmorphism effects** (backdrop-filter)
- **Performance-optimized** animations

Filen er visuelt imponerende men stadig funktionel - authentication fungerer uafhængigt af styling. Alle animationer er ikke-blocking og påvirker ikke form functionality.
