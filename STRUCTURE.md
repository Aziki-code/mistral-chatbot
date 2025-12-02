# Modular Code Structure

## Overview
The chatbot code has been refactored from a single 1267-line monolithic file into modular components for better maintainability.

## File Structure

```
templates/
  index.html (main HTML structure)
  login.html (authentication page)

static/
  css/
    main.css (imports only - 24 lines)
    base.css (common styles - 476 lines)
    themes/
      cisco.css (Cisco SecureCRT theme with orange user styling)
      vscode.css (VS Code theme)
      monokai.css (Monokai theme)
      dracula.css (Dracula theme)
      nord.css (Nord theme)
      solarized.css (Solarized theme)
      github.css (GitHub theme)
      light-theme.css (Light theme with gray glow)
      light-quiet-theme.css (Light Quiet theme with purple glow)
  
  js/
    prism-cisco.js (Cisco IOS language definition)
    themes.js (theme management and switching - 9 themes)
    code-detector.js (language detection utilities)
    message-parser.js (message parsing logic)
    message-handler.js (message display, API calls, clickable code blocks)
    ui-handlers.js (event handlers and initialization)
    session-timeout.js (auto-logout timer)
  
  images/
    kali-layers.png (watermark for dark themes)
    kali-layers-light2.jpeg (watermark for light theme)
    kali-layers-quiet2.jpeg (watermark for light-quiet theme)
  
  uploads/
    .gitkeep (ensures directory exists in git)
```

## Module Responsibilities

### CSS Modules
- **main.css**: Import manager for all CSS files
- **base.css**: Common styles, layout, watermark system, animations
- **themes/*.css**: Individual theme files (9 total) with custom colors, glows, and styling
  - Dark themes: cyan glow effect with kali-layers.png watermark
  - Light themes: gray/purple glow with custom watermarks
  - Cisco theme: orange user styling with orange glow effect

### JavaScript Modules
- **prism-cisco.js**: Cisco IOS language definition for Prism.js
- **themes.js**: Theme definitions (9 themes), applyTheme(), initThemes()
- **code-detector.js**: Language detection (Cisco, HTML, CSS, Python, SQL, etc.)
- **message-parser.js**: Parse messages with code fences (```), escape HTML
- **message-handler.js**: appendMessage(), sendMessage(), uploadScreenshotFile(), addPastedCode(), clickable code block indicators with scroll and glow effects
- **ui-handlers.js**: Event listeners, DOM initialization, window resize handler
- **session-timeout.js**: Auto-logout after 30 minutes of inactivity

## Load Order (Important!)
Scripts must load in this order (dependencies):
1. Prism.js (external CDN)
2. prism-cisco.js (defines Prism.languages.cisco)
3. code-detector.js (uses normalizeNewlines, parseMessage)
4. message-parser.js (provides parseMessage)
5. themes.js (defines themes, applyTheme)
6. message-handler.js (uses all above)
7. ui-handlers.js (initializes everything)

## Benefits of Modular Structure

### Maintainability
- Each file has one clear responsibility (Single Responsibility Principle)
- Easy to find and fix bugs - you know exactly which file to edit
- Smaller files are easier to understand and review

### Browser Performance
- CSS and JS are cached separately
- Only reload changed modules during development
- Faster page loads on subsequent visits

### Collaboration
- Multiple developers can work on different modules without conflicts
- Clear module boundaries make code review easier
- Easier to add new features without breaking existing code

### AI-Friendly
- Each module fits completely within AI context windows
- No truncation when analyzing code
- Can paste entire modules for review/optimization

### Reusability
- Themes module can be reused in other projects
- Cisco syntax highlighting can be extracted
- Code detector works standalone

## Restoring Original Version

If you need to restore the monolithic version:
```bash
cd /home/kasperadm/mistral-bot/templates
cp index_monolith.html.backup index.html
sudo systemctl restart mistral-chatbot
```

## File Sizes
- Original monolithic: 47KB (1267 lines)
- New modular index.html: 3KB (75 lines) - **93% reduction**
- Total size (all modules): ~35KB - smaller due to less duplication

## Testing
After modular refactor, test:
- ✅ All 8 themes work correctly
- ✅ Cisco syntax highlighting
- ✅ Three-panel layout (pasted code, chat, code output)
- ✅ Language detection (Cisco, HTML, CSS, Python, SQL)
- ✅ Message sending and receiving
- ✅ Screenshot upload
- ✅ Copy buttons on code blocks
- ✅ Theme persistence (localStorage)
- ✅ Window resize handling
