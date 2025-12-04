# index.html - Detaljeret Dokumentation

## Overordnet Formål
`index.html` er hovedskabelonen for chatbot-applikationen. Den definerer hele brugergrænsefladen med tre-panel layout: venstre panel (chat), midterpanel (pasted code), og højre panel (bot code output).

---

## Filstruktur og Sektioner

### 1. DOCTYPE og HTML Tag (Linje 1-2)
```html
<!DOCTYPE html>
<html lang="en">
```
- **Linje 1**: `<!DOCTYPE html>` - Fortæller browseren at dette er et HTML5 dokument
- **Linje 2**: `<html lang="en">` - Root element, `lang="en"` specificerer engelsk sprog for accessibility og SEO

---

### 2. HEAD Sektion (Linje 3-22)

#### Meta Tags (Linje 4-10)
```html
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#1e1e1e" media="(prefers-color-scheme: dark)">
<meta name="theme-color" content="#f5f5f5" media="(prefers-color-scheme: light)">
<meta name="msapplication-navbutton-color" content="#1e1e1e">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
```
- **Linje 4**: `charset="UTF-8"` - Understøtter alle internationale tegn (emojis, danske æ/ø/å, etc.)
- **Linje 5**: `viewport` - Gør siden responsive på mobile enheder, `width=device-width` matcher skærmbredde, `initial-scale=1.0` starter ved 100% zoom
- **Linje 7**: `theme-color` for dark mode - Farver browser UI (adressebar, navigation) mørk grå (#1e1e1e) når bruger har dark mode
- **Linje 8**: `theme-color` for light mode - Farver browser UI lys grå (#f5f5f5) i light mode
- **Linje 9**: `msapplication-navbutton-color` - Specifik til Internet Explorer/Edge, farver navigation mørk
- **Linje 10**: `apple-mobile-web-app-status-bar-style` - På iOS Safari, gør status bar translucent sort

#### Title (Linje 11)
```html
<title>Chatbot with Upload v2.0</title>
```
- Vises i browser tab og bookmarks
- "v2.0" indikerer version med upload funktionalitet

#### CSS Links (Linje 13-22)
```html
<link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css" rel="stylesheet" />
<link rel="stylesheet" href="/static/css/main.css?v=7.2">
<style id="cisco-prism-theme" disabled>
    @import url('/static/css/themes/cisco-theme.css?v=7.2');
</style>
<style id="quiet-light-prism-theme" disabled>
    @import url('/static/css/themes/quiet-light-theme.css?v=7.2');
</style>
```
- **Linje 14**: Prism Tomorrow CSS fra CDN - Syntax highlighting for code blocks, dark theme som base
- **Linje 17**: main.css - Hoved stylesheet, `?v=7.2` er cache busting parameter (tvinger browser til at hente ny version)
- **Linje 18-20**: Cisco Prism theme - Inline `<style>` tag med `disabled` attribute, aktiveres kun når Cisco theme vælges
- **Linje 21-23**: Quiet Light Prism theme - Disabled som standard, aktiveres for Light Quiet theme

**Hvorfor disabled styles?**
JavaScript i themes.js aktiverer/deaktiverer disse dynamisk når bruger skifter theme. Dette undgår at loade unødvendige CSS filer.

---

### 3. BODY Sektion (Linje 24-67)

#### Chat Container (Linje 26)
```html
<div id="chat-container">
```
- Root container for hele applikationen
- Stylet i CSS med flexbox layout (3 kolonne grid)
- ID bruges af JavaScript til at manipulere layout

#### Theme Selector Panel (Linje 27-49)
```html
<div id="theme-selector">
    <label for="ai-model-dropdown" style="color: white; margin-right: 10px;">AI Model:</label>
    <select id="ai-model-dropdown" style="margin-right: 20px;">
        <option value="mistral">Mistral AI</option>
        <option value="github-copilot">GitHub Copilot</option>
    </select>
    <label for="theme-dropdown" style="color: white; margin-right: 10px;">Theme:</label>
    <select id="theme-dropdown">
        <option value="cisco">Cisco</option>
        <option value="vscode">VS Code Dark</option>
        <option value="monokai">Monokai</option>
        <option value="dracula">Dracula</option>
        <option value="nord">Nord</option>
        <option value="solarized">Solarized Dark</option>
        <option value="github">GitHub Dark</option>
        <option value="light">Light Theme</option>
        <option value="light-quiet">Light Quiet</option>
    </select>
    <a href="/logout" id="logout-btn">Logout</a>
</div>
```

**AI Model Dropdown (Linje 28-32):**
- **Linje 28**: Label med inline style `color: white` (synlig på dark baggrund), `margin-right: 10px` spacing
- **Linje 29**: `<select>` dropdown med ID for JavaScript targeting, `margin-right: 20px` afstand til næste element
- **Linje 30**: `value="mistral"` - Sender "mistral" til backend når valgt
- **Linje 31**: `value="github-copilot"` - Alternativ AI provider
- JavaScript i `ai-selector.js` håndterer skift mellem modeller

**Theme Dropdown (Linje 33-44):**
- **Linje 33**: Label for theme selector
- **Linje 34**: Select dropdown, ID `theme-dropdown` bruges af `themes.js`
- **Linje 35-43**: 9 theme options:
  - `cisco` - Default cyan/orange tema
  - `vscode` - VS Code dark colors
  - `monokai` - Populært editor tema
  - `dracula` - Lilla/pink tema
  - `nord` - Blå/frost farver
  - `solarized` - Beige/brun tema
  - `github` - GitHub dark mode
  - `light` - Standard light mode
  - `light-quiet` - Dæmpet light mode

**Logout Button (Linje 45):**
- `<a href="/logout">` - Link til Flask route der clearer session
- ID `logout-btn` bruges til styling i CSS

#### Input Panel - Pasted Code (Linje 50-52)
```html
<div id="input-panel">
    <div id="pasted-code-header">Pasted Code</div>
    <div id="pasted-code-output"></div>
</div>
```
- **Linje 50**: Midter-panel container, vises til venstre på skærmen (historisk naming)
- **Linje 51**: Header tekst "Pasted Code" - statisk label
- **Linje 52**: Tom div hvor pasted code blocks indsættes dynamisk af `message-handler.js`

**Hvordan fungerer det?**
Når bruger paster code i textarea og trykker Send:
1. `ui-handlers.js` fanger paste event
2. `message-handler.js` opretter code block med syntax highlighting
3. Indsættes i `#pasted-code-output` div
4. Vises med scroll, line numbers, og copy button

#### Left Panel - Chat (Linje 53-62)
```html
<div id="left-panel">
    <div id="chat"></div>
    <div id="input-container">
        <div id="input-row">
            <textarea id="input" placeholder="Type..." rows="3"></textarea>
            <button id="send">Send</button>
        </div>
        <input type="file" id="upload" accept="image/*">
        <button id="uploadBtn">Upload screenshot</button>
    </div>
</div>
```

**Chat Display (Linje 54):**
- Tom div hvor chat messages indsættes dynamisk
- Stylet med `overflow-y: auto` for scrolling
- Messages tilføjes af `message-handler.js` funktionen `addMessage()`

**Input Container (Linje 55-61):**
- **Linje 56**: `input-row` - Flexbox container for textarea og send button
- **Linje 57**: `<textarea>` - Multi-line text input
  - `id="input"` - Target for JavaScript event listeners
  - `placeholder="Type..."` - Grå hjælpetekst når tom
  - `rows="3"` - Standard højde 3 linjer
- **Linje 58**: Send button - Trigger `sendMessage()` i `ui-handlers.js`
- **Linje 60**: File input - Hidden (styled med `display: none`), `accept="image/*"` kun billeder
- **Linje 61**: Upload button - Trigger file input click

**Hvorfor skjult file input?**
HTML `<input type="file">` er grim og ikke-stylet. Vi bruger custom button der trigger den skjulte input for bedre UI.

#### Right Panel - Code Output (Linje 63-66)
```html
<div id="right-panel">
    <div id="code-output-header">Code Output</div>
    <div id="code-output"></div>
</div>
```
- **Linje 63**: Højre panel container
- **Linje 64**: Header "Code Output" - viser hvad panelet indeholder
- **Linje 65**: Tom div hvor bot's code responses indsættes
  - `message-parser.js` detecterer code blocks i bot response
  - `message-handler.js` opretter formateret code block med Prism highlighting
  - Vises med clickable indicator button i chat

---

### 4. SCRIPT Sektion (Linje 69-90)

#### Prism.js Setup (Linje 69-75)
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js" data-manual></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/plugins/autoloader/prism-autoloader.min.js"></script>
<script>
    Prism.plugins.autoloader.languages_path = 'https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/';
</script>
```
- **Linje 69**: Prism core library, `data-manual` disabler auto-highlighting (vi styrer det manuelt)
- **Linje 70**: Autoloader plugin - loader language definitions on-demand (python, javascript, etc.)
- **Linje 72-74**: Konfigurerer autoloader til at hente languages fra CDN

**Hvorfor autoloader?**
I stedet for at loade ALLE sprog (100+ filer), loader vi kun dem vi bruger. Sparer bandwidth.

#### Backend Configuration (Linje 77-82)
```html
<script>
    window.mistralAvailable = {{ mistral_available|lower }};
    window.githubAvailable = {{ github_available|lower }};
    window.defaultProvider = "{{ default_provider }}";
</script>
```
- **Jinja2 Template Variables** - Flask sender Python variabler til JavaScript:
  - `{{ mistral_available|lower }}` - Boolean (true/false) om Mistral API er konfigureret
  - `{{ github_available|lower }}` - Boolean om GitHub Copilot API er konfigureret
  - `{{ default_provider }}` - String ("mistral" eller "github-copilot")
  - `|lower` filter konverterer Python True/False til JavaScript true/false

**Hvordan bruges det?**
`ai-selector.js` læser disse variabler for at:
1. Disable dropdown options hvis API ikke er konfigureret
2. Sætte default valgt model
3. Vise fejl hvis ingen modeller er tilgængelige

#### Custom JavaScript Modules (Linje 83-89)
```html
<script src="/static/js/prism-cisco.js?v=7.2"></script>
<script src="/static/js/code-detector.js?v=7.2"></script>
<script src="/static/js/message-parser.js?v=7.2"></script>
<script src="/static/js/themes.js?v=7.2"></script>
<script src="/static/js/message-handler.js?v=7.2"></script>
<script src="/static/js/ui-handlers.js?v=7.2"></script>
<script src="/static/js/session-timeout.js?v=7.2"></script>
<script src="/static/js/ai-selector.js?v=7.2"></script>
```

**Load order er kritisk:**

1. **prism-cisco.js** - Custom Prism language definition for Cisco syntax
2. **code-detector.js** - Funktioner til at detecte code blocks i tekst, identificere sprog
3. **message-parser.js** - Parser bot responses, extracterer code blocks, formaterer markdown
4. **themes.js** - Håndterer theme switching, localStorage persistence, CSS manipulation
5. **message-handler.js** - Opretter message elements, code blocks, scroll handlers, highlight effects
6. **ui-handlers.js** - Event listeners for buttons, textarea, file upload, send message logic
7. **session-timeout.js** - Detecterer inaktivitet, auto-logout efter 30 min, viser warning
8. **ai-selector.js** - Håndterer AI model dropdown, sender provider til backend

**Cache Busting (`?v=7.2`)**
- Query parameter tvinger browser til at hente ny fil når version ændres
- Uden dette ville browser bruge cached gammel version efter updates
- Skal opdateres hver gang JavaScript/CSS ændres

---

## Dataflow og Interaktioner

### Bruger Sender Besked:
1. Bruger skriver i `<textarea id="input">`
2. Trykker `<button id="send">` eller Enter
3. `ui-handlers.js` → `sendMessage()` funktion
4. POST request til `/chat` endpoint i `bot.py`
5. Backend kalder AI model (Mistral/GitHub)
6. Response sendes tilbage som JSON
7. `message-parser.js` parser response
8. `message-handler.js` opdaterer `<div id="chat">`
9. Code blocks indsættes i `<div id="code-output">`

### Bruger Uploader Billede:
1. Bruger trykker `<button id="uploadBtn">`
2. `ui-handlers.js` trigger click på `<input type="file" id="upload">`
3. Bruger vælger fil fra file picker
4. JavaScript læser fil, encoder som base64
5. POST request til `/chat` med image data
6. Backend bruger Mistral Vision til at analysere billede
7. Response vises i chat

### Bruger Skifter Theme:
1. Bruger vælger theme i `<select id="theme-dropdown">`
2. `themes.js` → `applyTheme()` funktion
3. Ændrer `<body>` class attribute (f.eks. `<body class="cisco">`)
4. CSS regler i `themes/cisco.css` aktiveres
5. Prism theme styles opdateres
6. Theme navn gemmes i localStorage
7. Næste besøg loader samme theme

---

## Accessibility Features

1. **Semantic HTML** - Korrekt brug af `<label>`, `<button>`, `<textarea>`
2. **Lang attribute** - `<html lang="en">` for screen readers
3. **Placeholder text** - Hjælp til input field
4. **Focus states** - CSS hover/focus states på buttons
5. **Keyboard navigation** - Tab gennem form elements
6. **Responsive viewport** - Fungerer på mobile devices

---

## Security Considerations

1. **File upload validation** - `accept="image/*"` begr ænser til billeder (backend validerer også)
2. **Session management** - Flask session håndteret af backend
3. **Logout funktion** - Korrekt session cleanup
4. **XSS prevention** - Jinja2 auto-escaper HTML i responses
5. **CSRF protection** - Flask har indbygget CSRF på POST routes

---

## Performance Optimizations

1. **CDN for Prism** - Hurtigere load, cached globalt
2. **Cache busting** - Sikrer users får nye versioner
3. **Lazy loading** - Prism autoloader kun loader nødvendige sprog
4. **Manual Prism** - Vi styrer hvornår highlighting sker
5. **Disabled styles** - Kun aktiv theme loades

---

## Forbindelser til Andre Filer

### Backend (`bot.py`):
- Route `/` render denne template
- Sender `mistral_available`, `github_available`, `default_provider` variabler
- Route `/chat` modtager POST fra send button
- Route `/uploads/<filename>` server uploaded images

### CSS:
- `main.css` - Importer og base styles
- `themes/*.css` - Theme-specifikke farver og overrides
- Prism CSS - Syntax highlighting farver

### JavaScript:
- `ui-handlers.js` - Lytter på alle button clicks
- `message-handler.js` - Manipulerer chat og code output divs
- `themes.js` - Opdaterer body class ved theme skift
- `session-timeout.js` - Redirect til `/logout` efter inaktivitet

---

## Konklusion

`index.html` er simpel men kraftfuld. Den definerer struktur, loader alle dependencies i korrekt rækkefølge, og fungerer som bro mellem backend (Flask/Python) og frontend (JavaScript/CSS). Layout er responsive, accessibility-aware, og optimeret for performance.
