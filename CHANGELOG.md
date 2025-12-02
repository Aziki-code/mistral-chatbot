# Changelog

All notable changes to the AzikiAI Chatbot project.

## [2.1.0] - 2025-12-02

### 🎨 UI/UX Enhancements
- **CSS Architecture Reorganization**
  - Restructured CSS into modular system with `main.css` (imports), `base.css` (common), and `themes/` folder
  - Created individual CSS files for each theme (9 total themes)
  - Improved maintainability and theme customization

- **Enhanced Code Block Interactions**
  - Implemented clickable code indicators that scroll to specific code blocks
  - Added smooth scroll animation with ripple glow effects
  - Fixed closure issue preventing proper code block targeting
  - Persistent pasted code (accumulates instead of clearing)

- **Theme-Specific Customizations**
  - Cisco theme: Orange user message styling (#ffaa33) with orange glow effect
  - Light theme: Gray glow effect (#5a6268) with custom watermark
  - Light-quiet theme: Purple glow effect (#8b7b9b) with custom watermark
  - Dark themes: Cyan glow effect with grayscale watermark

- **Watermark System**
  - Implemented transparent background watermarks across all themes
  - Dark themes: kali-layers.png with grayscale filter
  - Light themes: Custom kali-layers-light2.jpeg and kali-layers-quiet2.jpeg
  - Proper z-index layering for visibility

- **Chat Layout Improvements**
  - Fixed chat window centering (800px fixed width)
  - User messages aligned right (80% max-width)
  - Bot messages aligned left (80% max-width)
  - Copy buttons right-aligned in code headers
  - "Copied!" feedback centered in each code block

### 🧹 Code Cleanup
- **Removed obsolete files**
  - Deleted `templates/index_monolith.html.backup`
  - Deleted `templates/.style_changes.css`
  - Deleted `templates/debug.html`
  - Deleted old uploads from `static/uploads/`

### 📝 Documentation Updates
- **Updated STRUCTURE.md**
  - Reflected new CSS architecture with themes folder
  - Added session-timeout.js documentation
  - Updated file structure to match current state

## [2.0.0] - 2025-12-02

### 🔒 Security Improvements
- **Moved hardcoded LDAP credentials to environment variables**
  - `LDAP_HOST`, `LDAP_PORT`, `LDAP_BASE_DN` now configured via `.env`
  - Added `LDAP_VALIDATE_SSL` toggle for certificate validation (defaults to false for internal AD)
  
- **Improved error handling with specific exceptions**
  - Replaced broad `except Exception` with specific LDAP exceptions
  - Better error messages for debugging
  
- **Added rate limiting**
  - Flask-Limiter integration: 30 requests/minute on `/chat` endpoint
  - Global limits: 200/day, 50/hour per IP
  - Protection against spam and abuse

### 🚀 Performance & Scalability
- **Refactored database connection handling**
  - Removed global connection (thread-safety issue)
  - Implemented context manager pattern with `get_db_connection()`
  - Proper connection pooling and cleanup
  - Added timestamp column to messages table

- **Production WSGI server with Gunicorn**
  - Created `gunicorn_config.py` with optimal settings
  - Multi-worker configuration based on CPU cores
  - SSL/TLS support
  - Proper logging and process management
  - Updated systemd service to use Gunicorn

### 📝 Code Quality
- **Structured logging**
  - Python `logging` module with file and console handlers
  - Logs saved to `logs/azikiai.log`
  - Request tracking, authentication events, and error logging
  - Separate Gunicorn access and error logs

- **Refactored language detection**
  - Created reusable `detect_language()` helper function
  - Eliminated 50+ lines of duplicate code
  - Support for Python, JavaScript, HTML, Java, CSS, SQL

### 🧹 Code Cleanup
- **Removed obsolete files**
  - Deleted `old_chatbot_sql.py`
  - Deleted `chatbot_sql.py`
  
- **Updated documentation**
  - Fixed theme count (7 themes, not 8)
  - Removed Quiet Light references
  - Added production deployment instructions
  - Updated structure documentation with new files

### 📦 Configuration
- **Enhanced `.env.example`**
  - Added `LDAP_PORT` (default: 636)
  - Added `LDAP_VALIDATE_SSL` (default: false)
  - Added `SESSION_TIMEOUT_MINUTES` (default: 10)

- **Updated requirements.txt**
  - Added `flask-limiter==3.5.0`
  - Organized dependencies by category

- **Improved `.gitignore`**
  - Added `logs/` directory exclusion
  - Better organization

### 🔧 Systemd Service
- **Enhanced service configuration**
  - Changed from `Type=simple` to `Type=notify`
  - Added `WatchdogSec=30` for health monitoring
  - Changed from `Restart=always` to `Restart=on-failure`
  - Security hardening: `NoNewPrivileges=true`, `PrivateTmp=true`
  - Increased `TimeoutStartSec` to 120s for Gunicorn startup

### 🎨 UI/UX
- **No breaking changes to frontend**
  - All 7 themes still functional
  - Kali Layers background preserved
  - Transparent windows maintained

## [1.x.x] - Previous versions
See git history for earlier changes.
