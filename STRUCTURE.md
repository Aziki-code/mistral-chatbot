# Modular Code Structure

## Overview
The chatbot code has been refactored from a single 1267-line monolithic file into modular components for better maintainability.

## File Structure

```
templates/
  index.html (75 lines - main HTML structure)
  index_monolith.html.backup (1267 lines - original version)

static/
  css/
    main.css (363 lines - main styles and layout)
    cisco-theme.css (110 lines - Cisco SecureCRT colors)
  
  js/
    prism-cisco.js (123 lines - Cisco IOS language definition)
    themes.js (246 lines - theme management and switching)
    code-detector.js (116 lines - language detection utilities)
    message-parser.js (63 lines - message parsing logic)
    message-handler.js (294 lines - message display and API calls)
    ui-handlers.js (98 lines - event handlers and initialization)
```

## Module Responsibilities

### CSS Modules
- **main.css**: All layout, colors, panels, buttons, scrollbars
- **cisco-theme.css**: SecureCRT exact color matching for Cisco syntax

### JavaScript Modules
- **prism-cisco.js**: Cisco IOS language definition for Prism.js
- **themes.js**: Theme definitions (8 themes), applyTheme(), initThemes()
- **code-detector.js**: Language detection (Cisco, HTML, CSS, Python, SQL)
- **message-parser.js**: Parse messages with code fences (```), escape HTML
- **message-handler.js**: appendMessage(), sendMessage(), uploadScreenshotFile(), addPastedCode()
- **ui-handlers.js**: Event listeners, DOM initialization, window resize handler

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
