# AzikiAI Chatbot - Dokumentation

Komplet teknisk dokumentation af AzikiAI chatbot projektet med line-by-line forklaring af hele kodebasen.

---

## 📋 Quick Start

**Ny i projektet?** Start her:
1. Læs [PROJECT-OVERVIEW.md](PROJECT-OVERVIEW.md) for high-level arkitektur
2. Læs [DOCUMENTATION-STATUS.md](DOCUMENTATION-STATUS.md) for dokumentations status
3. Find relevant fil nedenfor baseret på hvad du arbejder på

---

## 📁 Dokumentations Index

### 🎯 Start Her
- **[PROJECT-OVERVIEW.md](PROJECT-OVERVIEW.md)** - Komplet projekt oversigt
  - Arkitektur diagrammer
  - Deployment guide
  - Konfiguration reference
  - Troubleshooting
  - Performance metrics
  - Security analysis

- **[DOCUMENTATION-STATUS.md](DOCUMENTATION-STATUS.md)** - Dokumentations status
  - ✅ 21/21 filer dokumenteret
  - ~20,000 linjer dokumentation
  - Kvalitets checklist
  - Statistik og metrics

---

## 🐍 Backend Documentation (Python)

### bot.py - Main Flask Application (3 parts)
1. **[bot.py-PART1-DETAILED.md](backend/bot.py-PART1-DETAILED.md)**
   - Imports og dependencies
   - Flask app initialization
   - Session configuration
   - Upload folder setup
   - Mistral AI client setup

2. **[bot.py-PART2-DETAILED.md](backend/bot.py-PART2-DETAILED.md)**
   - Login routes (GET/POST)
   - LDAP authentication
   - SQLite fallback
   - Session management
   - Logout route

3. **[bot.py-PART3-DETAILED.md](backend/bot.py-PART3-DETAILED.md)**
   - Chat routes (/api/chat, /api/upload)
   - AI model selection (text vs Vision)
   - Mistral Vision API integration
   - Image processing (base64 encoding)
   - Stream responses
   - Helper functions

### Database Module
4. **[chatbot_sql.py-DETAILED.md](backend/chatbot_sql.py-DETAILED.md)**
   - SQLite database wrapper
   - Schema (users, messages tables)
   - CRUD operations
   - Message logging
   - User management
   - Connection handling

---

## 🌐 Frontend Documentation (HTML)

5. **[index.html-DETAILED.md](frontend/index.html-DETAILED.md)**
   - 3-panel layout structure
   - Left panel (chat messages)
   - Input panel (textarea, buttons)
   - Right panel (code output)
   - Message bubbles
   - Code blocks with copy buttons
   - Theme selector
   - AI model dropdown
   - Screenshot upload area
   - ~500 linjer HTML forklaret

6. **[login.html-DETAILED.md](frontend/login.html-DETAILED.md)**
   - Login form structure
   - Embedded CSS animations
   - Input field styling
   - Error message display
   - Submit button
   - Glassmorphism effects
   - ~313 linjer HTML+CSS forklaret

---

## 💻 Frontend Documentation (JavaScript)

### Core Functionality
7. **[message-handler.js-DETAILED.md](frontend/message-handler.js-DETAILED.md)**
   - sendMessage() - POST til /api/chat
   - handleUpload() - Screenshot upload
   - displayMessage() - Render chat bubbles
   - streamResponse() - AI streaming
   - detectCode() - Language detection integration
   - Copy to clipboard
   - ~344 linjer forklaret

8. **[message-parser.js-DETAILED.md](frontend/message-parser.js-DETAILED.md)**
   - parseMessage() - Markdown til HTML
   - State machine implementation
   - Code block detection
   - escapedHtml() - XSS prevention
   - Supports: **bold**, *italic*, `code`, ```blocks```
   - ~200 linjer forklaret

9. **[code-detector.js-DETAILED.md](frontend/code-detector.js-DETAILED.md)**
   - detectLanguage() - Auto-detect syntax
   - isPythonCode(), isCiscoConfig(), etc.
   - Confidence scoring
   - Returns: { language: 'cisco', confidence: 0.95 }
   - ~108 linjer forklaret

### UI Components
10. **[ui-handlers.js-DETAILED.md](frontend/ui-handlers.js-DETAILED.md)**
    - Event listeners setup
    - copyCode() - Copy to clipboard
    - showCodeOutput() - Display i right panel
    - scrollToBottom() - Auto-scroll chat
    - Paste detection
    - ~150 linjer forklaret

11. **[themes.js-DETAILED.md](frontend/themes.js-DETAILED.md)**
    - applyTheme() - Set data-theme attribute
    - 9 themes: cisco, vscode, monokai, dracula, nord, solarized, github, light, light-quiet
    - CSS variable switching
    - LocalStorage persistence
    - Watermark filter toggle
    - Prism theme switching
    - ~260 linjer forklaret

12. **[ai-selector.js-DETAILED.md](frontend/ai-selector.js-DETAILED.md)**
    - AI model dropdown
    - LocalStorage persistence
    - Model change notifications
    - Icon updates
    - ~80 linjer forklaret

### Security & Utilities
13. **[session-timeout.js-DETAILED.md](frontend/session-timeout.js-DETAILED.md)**
    - 24-hour session timeout
    - Warning modal at 23h 50m
    - Auto-logout at 24h
    - Heartbeat to /api/heartbeat
    - Inactivity detection
    - ~100 linjer forklaret

14. **[prism-cisco.js-DETAILED.md](frontend/prism-cisco.js-DETAILED.md)**
    - Custom Prism.js language definition
    - 21 Cisco IOS token types
    - Patterns: prompts, interfaces, IPs, keywords
    - Regex tokenization
    - ~100 linjer forklaret

---

## 🎨 Frontend Documentation (CSS)

### Foundation
15. **[main.css-DETAILED.md](frontend/main.css-DETAILED.md)**
    - Import hub (23 linjer)
    - @import cascade
    - Load order: base → cisco → themes
    - Performance analysis
    - Cache strategy

16. **[base.css-DETAILED.md](frontend/base.css-DETAILED.md)**
    - Foundation CSS (476 linjer)
    - CSS reset
    - 15 CSS variables (:root)
    - 3-panel layout (flexbox + calc())
    - Watermark (body::before)
    - Message bubbles
    - Code blocks
    - Animations (fadeIn, ripple)
    - Custom scrollbar
    - Input styling

### Dark Themes (Combined Documentation)
17. **[DARK-THEMES-DETAILED.md](frontend/DARK-THEMES-DETAILED.md)**
    - **6 dark themes** dokumenteret sammen:
      1. cisco.css - Default, cyan accent (#00d7ff)
      2. vscode.css - VS Code Dark+, teal (#4ec9b0)
      3. monokai.css - Sublime Text, lime green (#a6e22e)
      4. dracula.css - Gothic purple (#bd93f9)
      5. nord.css - Arctic frost (#88c0d0)
      6. solarized.css - Lab-tested, yellow (#b58900)
      7. github.css - GitHub official dark (#58a6ff)
    - Color psychology analysis
    - Comparison table
    - ~17 linjer per theme (simple variable overrides)

### Light Themes (Combined Documentation)
18. **[LIGHT-THEMES-DETAILED.md](frontend/LIGHT-THEMES-DETAILED.md)**
    - **2 light themes** dokumenteret sammen:
      1. light-theme.css - Standard light (185 linjer)
         - Gray buttons (#5a6268)
         - Light backgrounds (#f8f9fa)
         - Custom watermark (kali-layers-light2.jpeg)
      2. light-quiet-theme.css - Purple/pink soft (182 linjer)
         - Purple color scheme (#4a3a4a text)
         - Soft pastel backgrounds (#f5f0f5)
         - Custom watermark (kali-layers-quiet2.jpeg)
    - Override strategies
    - !important usage analysis

### Prism Syntax Themes (Combined Documentation)
19. **[PRISM-THEMES-DETAILED.md](frontend/PRISM-THEMES-DETAILED.md)**
    - **3 Prism themes** dokumenteret sammen:
      1. cisco-theme.css - SecureCRT colors (88 linjer)
         - Exact color matching fra SecureCRT
         - 27 token types (prompts, IPs, keywords)
         - Color psychology (green=good, red=bad)
      2. cisco-light-theme.css - Dark for light bg (97 linjer)
         - Darkened colors for readability
         - Same semantic meaning maintained
      3. quiet-light-theme.css - VS Code Quiet Light (171 linjer)
         - Python/HTML/JS colors
         - @import cisco-light-theme.css
         - Language-specific selectors
    - Token type mapping
    - Prism.js integration

---

## ⚙️ Support Files

20. **[SUPPORT-FILES-DETAILED.md](SUPPORT-FILES-DETAILED.md)**
    - **start.sh** - Startup script analysis
      - Line-by-line breakdown
      - 🐛 Bug: Runs `main.py` (should be `bot.py`)
      - 🐛 Bug: Shows `https://` (should be `http://`)
      - Improved version included
    - **test_ldap.py** - Missing (reconstructed logic)
    - **test_user_auth.py** - Missing (reconstructed logic)
    - **requirements.txt** - Should exist (recommended content)

---

## 📊 Dokumentations Statistik

### Omfang
- **Total filer dokumenteret**: 21
- **Total linjer dokumentation**: ~20,000
- **Faktisk kodebase**: ~4,400 linjer
- **Ratio**: 4.5:1 (dokumentation til kode)

### Per Kategori
| Kategori | Filer | Kode Linjer | Docs Linjer | Ratio |
|----------|-------|-------------|-------------|-------|
| Backend (Python) | 4 | ~900 | ~3,000 | 3.3:1 |
| Frontend (HTML) | 2 | ~600 | ~2,500 | 4.2:1 |
| Frontend (JavaScript) | 8 | ~1,080 | ~5,000 | 4.6:1 |
| Frontend (CSS) | 6 docs (14 files) | ~1,850 | ~6,000 | 3.2:1 |
| Support | 1 | N/A | ~1,500 | N/A |
| Overview | 2 | N/A | ~2,000 | N/A |
| **TOTAL** | **23** | **~4,430** | **~20,000** | **4.5:1** |

---

## 🎯 Hvordan Bruger Man Dokumentationen

### Som Ny Udvikler
```
1. Start: PROJECT-OVERVIEW.md (arkitektur, deployment)
2. Backend: Læs bot.py parts 1-3 (Flask routes, AI integration)
3. Frontend: Læs index.html + message-handler.js (UI + core logic)
4. Styling: Læs base.css + relevant theme (layout + colors)
5. Deep dive: Læs specifik fil du skal ændre
```

### Til Debugging
```
1. Identificer problem område (backend/frontend?)
2. Find relevant fil i dokumentationen
3. Søg efter funktion/selector i docs
4. Læs line-by-line forklaring
5. Check "Known Issues" section
```

### Til Feature Development
```
1. Læs PROJECT-OVERVIEW.md → Architecture
2. Find lignende eksisterende feature
3. Læs dens implementation i docs
4. Copy pattern, tilpas til nyt feature
5. Check best practices i docs
```

### Til System Administration
```
1. PROJECT-OVERVIEW.md → Deployment section
2. SUPPORT-FILES-DETAILED.md → start.sh, .env setup
3. PROJECT-OVERVIEW.md → Troubleshooting
4. Check performance metrics
```

---

## 🔍 Søg i Dokumentation

### Find Specifik Feature
```bash
# Søg i alle docs
grep -r "LDAP" docs/

# Find hvor en funktion er forklaret
grep -r "sendMessage" docs/frontend/

# Find CSS selector forklaring
grep -r ".message.user" docs/frontend/
```

### Common Searches
- **Authentication**: `bot.py-PART2-DETAILED.md` → LDAP/SQLite
- **AI Integration**: `bot.py-PART3-DETAILED.md` → Mistral Vision
- **Code Highlighting**: `prism-cisco.js-DETAILED.md` + `PRISM-THEMES-DETAILED.md`
- **Theme Switching**: `themes.js-DETAILED.md` + theme CSS docs
- **Layout**: `base.css-DETAILED.md` → 3-panel structure
- **Message Flow**: `message-handler.js-DETAILED.md` → sendMessage()

---

## 🐛 Kendte Problemer Dokumenteret

### Critical Bugs
1. **start.sh** - Kører `main.py` i stedet for `bot.py` (SUPPORT-FILES)
2. **start.sh** - Viser `https://` i stedet for `http://` (SUPPORT-FILES)

### Security Issues
1. **No HTTPS** - All traffic unencrypted (PROJECT-OVERVIEW)
2. **No rate limiting** - API misbrugsbar (PROJECT-OVERVIEW)
3. **No CSRF protection** - Forms vulnerable (PROJECT-OVERVIEW)
4. **Debug mode** - Stack traces exposed (bot.py-PART1)

### Performance Concerns
1. **No caching** - Repeated API calls (PROJECT-OVERVIEW)
2. **No pagination** - Loads all messages (chatbot_sql.py)
3. **No image compression** - 5MB uploads (bot.py-PART3)

---

## 📖 Dokumentations Kvalitet

### Hver Fil Indeholder
- ✅ File information (størrelse, formål, kompleksitet)
- ✅ Structure overview (high-level flow)
- ✅ Line-by-line walkthrough (hver linje forklaret)
- ✅ Code examples (konkrete use cases)
- ✅ Data flow diagrams (visualiseringer)
- ✅ Error handling (exception håndtering)
- ✅ Performance notes (optimering)
- ✅ Browser/platform compatibility
- ✅ Best practices (anbefalinger)
- ✅ Troubleshooting (common issues + fixes)

### Specielle Features
- **CSS**: RGB/hex color analysis, contrast ratios
- **JavaScript**: Closure patterns, event flow
- **Python**: LDAP flow, AI integration
- **Security**: Vulnerabilities identified
- **Performance**: Metrics og optimization tips

---

## 🚀 Next Steps (Valgfrit)

### Potential Udvidelser
- [ ] Merge alt til ét MASTER-DOCUMENTATION.md
- [ ] Generer PDF version (pandoc)
- [ ] Interactive HTML dokumentation
- [ ] Flowcharts med Mermaid.js
- [ ] Oversæt til engelsk
- [ ] Video tutorials
- [ ] GitHub wiki integration

### Maintenance
- [ ] Opdater når kode ændres
- [ ] Version tracking (git tags)
- [ ] Changelog for docs
- [ ] Review process

---

## 📞 Kontakt & Support

For spørgsmål om dokumentationen:
1. Check [DOCUMENTATION-STATUS.md](DOCUMENTATION-STATUS.md) først
2. Søg i relevant fil (se index ovenfor)
3. Check PROJECT-OVERVIEW.md → Troubleshooting

---

## 📜 License & Credits

**Projekt**: AzikiAI Chatbot
**Version**: 2.0 (Mistral Vision integration)
**Dokumentation Oprettet**: 2024
**Teknologi**: Python Flask, Mistral AI, SQLite, LDAP

---

**🎉 Komplet projekt dokumentation klar til brug! 🎉**

Alle 21 filer dokumenteret med ~20,000 linjer teknisk dokumentation.
Line-by-line forklaring af hele kodebasen (~4,400 linjer).
Ratio: 4.5:1 (dokumentation til kode).

**Start her**: [PROJECT-OVERVIEW.md](PROJECT-OVERVIEW.md)
