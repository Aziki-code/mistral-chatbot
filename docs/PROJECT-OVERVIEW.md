# AzikiAI Chatbot - Complete Project Overview

Komplet teknisk oversigt over AzikiAI chatbot projektet med Mistral Vision integration.

---

## Project Metadata

- **Project Name**: AzikiAI Chatbot
- **Version**: 2.0 (Mistral Vision integration)
- **Technology Stack**: Python Flask, Mistral AI, SQLite, LDAP
- **Deployment**: Raspberry Pi 5 (192.168.0.80:5000)
- **Documentation Created**: 2024
- **Total Lines Documented**: ~20,000+ lines of technical documentation

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Backend (Python)](#backend-python)
3. [Frontend (HTML/CSS/JavaScript)](#frontend-htmlcssjavascript)
4. [Database Schema](#database-schema)
5. [Authentication Flow](#authentication-flow)
6. [AI Integration](#ai-integration)
7. [File Structure](#file-structure)
8. [Deployment](#deployment)
9. [Configuration](#configuration)
10. [Documentation Index](#documentation-index)

---

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Browser                          │
│  (http://192.168.0.80:5000)                                 │
└────────────┬────────────────────────────────────────────────┘
             │
             │ HTTP/HTTPS
             │
             v
┌─────────────────────────────────────────────────────────────┐
│                     Flask Application                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐         │
│  │   bot.py    │  │chatbot_sql  │  │  Templates  │         │
│  │ (Routes &   │  │(Database)   │  │ (HTML/CSS)  │         │
│  │  AI Logic)  │  │             │  │             │         │
│  └─────────────┘  └─────────────┘  └─────────────┘         │
└────────────┬───────────────┬────────────────────────────────┘
             │               │
             │               │ SQLite queries
             v               v
┌──────────────────┐  ┌────────────────┐
│   Mistral AI     │  │ azikiai_users  │
│   Vision API     │  │    .db         │
│                  │  │                │
│ - pixtral-large  │  │ - users table  │
│ - Image analysis │  │ - sessions     │
└──────────────────┘  └────────────────┘
             │
             │ LDAP (optional)
             v
┌──────────────────────────────┐
│   Active Directory Server    │
│   (LDAP authentication)      │
└──────────────────────────────┘
```

### Component Interaction

```
User Input (text/image)
        │
        v
JavaScript (message-handler.js)
        │
        │ POST /api/chat or /api/upload
        v
Flask Route (@app.route)
        │
        v
AI Model Selection (bot.py)
        │
        ├─> Text-only: mistral-large-latest
        │
        └─> With image: pixtral-large-latest (Vision)
                │
                v
        Mistral API Request
                │
                v
        AI Response
                │
                v
        Database Logging (chatbot_sql.py)
                │
                v
        JSON Response to Browser
                │
                v
        JavaScript Rendering (message-parser.js)
                │
                v
        Display in Chat (with Prism.js highlighting)
```

---

## Backend (Python)

### bot.py - Main Application (3 parts documentation)

#### Purpose
Flask application med routes, session handling, AI integration

#### Key Components
1. **Flask Setup**
   - App initialization with secret key
   - Session configuration (permanent, 24h timeout)
   - Upload folder configuration

2. **Authentication Routes**
   - `/login` (GET/POST) - User login with LDAP or SQLite fallback
   - `/logout` - Session cleanup
   - Login decorator for protected routes

3. **Chat Routes**
   - `/` - Main chat interface (requires login)
   - `/api/chat` (POST) - Text message processing
   - `/api/upload` (POST) - Image upload for Vision API

4. **AI Integration**
   - Mistral AI client initialization
   - Model selection logic:
     * `mistral-large-latest` - Text-only chat
     * `pixtral-large-latest` - Vision API (with images)
   - Image encoding (base64 for API)
   - Stream processing for real-time responses

5. **Database Integration**
   - Message logging via chatbot_sql.py
   - User conversation history
   - Session tracking

#### Critical Functions
- `handle_chat()` - Main chat endpoint, routes to Vision or text-only
- `handle_vision()` - Process images with Mistral Vision
- `login_required()` - Decorator protecting routes
- `validate_login()` - LDAP/SQLite authentication

### chatbot_sql.py - Database Module

#### Purpose
SQLite database wrapper for message storage and retrieval

#### Schema
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    username TEXT NOT NULL,
    role TEXT NOT NULL,  -- 'user' or 'assistant'
    content TEXT NOT NULL,
    image_path TEXT,     -- NULL for text-only messages
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### Key Functions
- `create_tables()` - Initialize database schema
- `save_message()` - Store chat messages
- `get_conversation_history()` - Retrieve user's past messages
- `save_user()` - Create new user
- `get_user()` - Fetch user credentials

---

## Frontend (HTML/CSS/JavaScript)

### HTML Templates

#### index.html - Main Chat Interface
- **3-panel layout**:
  1. **Left panel** (#left-panel) - Chat messages (800px centered)
  2. **Input panel** (#input-panel) - Textarea, buttons, file upload
  3. **Right panel** (#right-panel) - Code output from clicked blocks

- **Components**:
  - Message bubbles (.message.user, .message.assistant)
  - Code blocks (.codeblock) with copy buttons
  - AI model selector dropdown
  - Theme selector (dark/light themes)
  - Screenshot upload area
  - Logout button

#### login.html - Authentication Page
- **Simple login form**:
  - Username input
  - Password input (type="password")
  - Submit button
  - Error message display

### CSS Architecture

#### main.css - Import Hub (23 lines)
```css
@import url('base.css');              /* Foundation */
@import url('themes/cisco.css');      /* Cisco dark theme */
@import url('themes/vscode.css');     /* VS Code dark */
@import url('themes/monokai.css');    /* Sublime Text */
/* ... 9 more theme imports ... */
@import url('cisco-theme.css');       /* Prism Cisco syntax */
@import url('cisco-light-theme.css'); /* Prism light mode */
```

#### base.css - Foundation (476 lines)
- **CSS Reset**: Universal selector, box-sizing
- **CSS Variables** (15 variables in :root):
  - `--bg-darkest`, `--bg-darker`, `--bg-dark`
  - `--text-primary`, `--text-muted`
  - `--accent-primary`, `--accent-secondary`
  - `--border-color`, `--hover-bg`, etc.
  
- **3-Panel Layout**:
  ```css
  #input-panel {
      position: fixed;
      left: calc(50% - 400px);  /* Centered, left side */
      width: 800px;
      bottom: 0;
  }
  
  #left-panel {
      position: fixed;
      left: calc(50% - 400px);  /* Same, above input */
      width: 800px;
      top: 0;
      bottom: 200px;  /* Space for input panel */
  }
  
  #right-panel {
      position: fixed;
      right: 0;
      width: 400px;  /* Side panel for code output */
  }
  ```

- **Watermark**: `body::before` with Kali dragon image
- **Message Bubbles**: Flexbox layout, user (right), assistant (left)
- **Code Blocks**: `.codeblock` with header, copy button, Prism.js integration
- **Animations**: `fadeIn`, `ripple`, `fadeInOut` keyframes
- **Custom Scrollbar**: `::-webkit-scrollbar` styling

#### Theme System (11 themes total)

**Dark Themes** (6):
1. **cisco.css** - Default, cyan accent (#00d7ff)
2. **vscode.css** - VS Code Dark+, teal accent (#4ec9b0)
3. **monokai.css** - Sublime Text, lime green (#a6e22e)
4. **dracula.css** - Gothic purple (#bd93f9)
5. **nord.css** - Arctic frost (#88c0d0)
6. **solarized.css** - Lab-tested, yellow accent (#b58900)
7. **github.css** - GitHub official dark (#58a6ff)

**Light Themes** (2):
1. **light-theme.css** - Standard light, gray buttons
2. **light-quiet-theme.css** - Purple/pink soft colors

**Prism Syntax Themes** (3):
1. **cisco-theme.css** - SecureCRT colors (dark)
2. **cisco-light-theme.css** - Dark colors for light bg
3. **quiet-light-theme.css** - VS Code Quiet Light

#### Theme Activation
```javascript
// themes.js
function applyTheme(themeName) {
    document.body.setAttribute('data-theme', themeName);
    // CSS: body[data-theme="vscode"] { --accent-primary: #4ec9b0; }
}
```

### JavaScript Modules

#### Core Functionality

1. **message-handler.js** (Main controller)
   - `sendMessage()` - POST to /api/chat
   - `handleUpload()` - POST to /api/upload with screenshot
   - `displayMessage()` - Render chat bubbles
   - `streamResponse()` - Handle AI streaming
   - `detectCode()` - Call code-detector.js

2. **code-detector.js** (Syntax detection)
   - `detectLanguage()` - Identify code language
   - `isPythonCode()`, `isCiscoConfig()`, etc.
   - Returns: `{ language: 'cisco', confidence: 0.95 }`

3. **message-parser.js** (Markdown + code rendering)
   - `parseMessage()` - Convert Markdown to HTML
   - `createCodeBlock()` - Wrap code in Prism.js structure
   - `escapedHtml()` - Prevent XSS
   - Supports: **bold**, *italic*, `code`, ```blocks```

4. **prism-cisco.js** (Custom Prism language)
   - Defines Cisco IOS syntax tokens
   - Patterns: prompts, interfaces, IPs, keywords
   - Integrates with Prism.js tokenizer

5. **themes.js** (Theme switcher)
   - `applyTheme()` - Set data-theme attribute
   - `loadTheme()` - Load from localStorage
   - `saveTheme()` - Persist selection
   - Watermark filter toggle for light themes

6. **session-timeout.js** (Inactivity detection)
   - 24-hour timeout
   - Modal warning at 23h 50m
   - Auto-logout at 24h
   - Heartbeat to /api/heartbeat

7. **ui-handlers.js** (UI interactions)
   - `copyCode()` - Copy code block to clipboard
   - `showCodeOutput()` - Display in right panel
   - `togglePanel()` - Show/hide panels
   - `scrollToBottom()` - Auto-scroll chat

---

## Database Schema

### azikiai_users.db

#### users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,  -- Werkzeug pbkdf2:sha256
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_login DATETIME
);

-- Example row:
-- id: 1
-- username: 'admin'
-- password_hash: 'pbkdf2:sha256:260000$...'
-- created_at: '2024-01-15 10:30:00'
```

#### messages Table
```sql
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,         -- Flask session['session_id']
    username TEXT NOT NULL,            -- session['username']
    role TEXT NOT NULL,                -- 'user' or 'assistant'
    content TEXT NOT NULL,             -- Message text
    image_path TEXT,                   -- /static/uploads/filename.png (NULL if text-only)
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    ai_model TEXT DEFAULT 'mistral-large-latest'
);

-- Example row (text message):
-- id: 42
-- session_id: 'a3f8d9e2-...'
-- username: 'kasperadm'
-- role: 'user'
-- content: 'Explain Python decorators'
-- image_path: NULL
-- timestamp: '2024-01-15 14:23:45'
-- ai_model: 'mistral-large-latest'

-- Example row (vision message):
-- id: 43
-- session_id: 'a3f8d9e2-...'
-- username: 'kasperadm'
-- role: 'assistant'
-- content: 'This network diagram shows...'
-- image_path: '/static/uploads/network_diagram_20240115_142350.png'
-- timestamp: '2024-01-15 14:23:50'
-- ai_model: 'pixtral-large-latest'
```

#### Indexes (Recommended, Not Implemented)
```sql
CREATE INDEX idx_session_id ON messages(session_id);
CREATE INDEX idx_username ON messages(username);
CREATE INDEX idx_timestamp ON messages(timestamp);
```

---

## Authentication Flow

### Login Process

```
┌─────────────────────────────────────────────────────────────┐
│ User visits http://192.168.0.80:5000                        │
└────────────┬────────────────────────────────────────────────┘
             │
             v
┌─────────────────────────────────────────────────────────────┐
│ Flask: Check if session['logged_in'] == True?              │
│  NO -> Redirect to /login                                   │
└────────────┬────────────────────────────────────────────────┘
             │
             v
┌─────────────────────────────────────────────────────────────┐
│ User enters username + password in login.html               │
│ POST to /login                                              │
└────────────┬────────────────────────────────────────────────┘
             │
             v
┌─────────────────────────────────────────────────────────────┐
│ bot.py: Try LDAP authentication first                       │
│  1. Connect to ldap://192.168.0.153                         │
│  2. Bind with user credentials                              │
│  3. Search for user in AD                                   │
└────────────┬────────────────────────────────────────────────┘
             │
             ├─> LDAP Success ──┐
             │                  │
             └─> LDAP Fail      │
                      │         │
                      v         │
         ┌────────────────────┐│
         │ Try SQLite fallback││
         │ 1. Query users tbl ││
         │ 2. check_password  ││
         │    _hash()         ││
         └────────┬───────────┘│
                  │            │
                  ├─> Success ─┤
                  │            │
                  └─> Fail     v
                       │  ┌─────────────────┐
                       │  │ Set session:    │
                       │  │ - logged_in:True│
                       │  │ - username      │
                       │  │ - session_id    │
                       │  └────────┬────────┘
                       │           │
                       v           v
              ┌─────────────┐  ┌───────────┐
              │ Redirect to │  │ Redirect  │
              │ /login with │  │ to /      │
              │ error       │  │ (chat UI) │
              └─────────────┘  └───────────┘
```

### Session Management

#### Session Variables
```python
session['logged_in'] = True
session['username'] = 'kasperadm'
session['session_id'] = 'uuid4-generated-id'
session.permanent = True  # 24-hour timeout
```

#### Session Timeout
- **Server-side**: Flask session expires after 24h (permanent_session_lifetime)
- **Client-side**: session-timeout.js monitors inactivity
  - Warning modal at 23h 50m
  - Auto-logout at 24h
  - Heartbeat every 5 minutes to keep session alive

---

## AI Integration

### Mistral AI Models

#### mistral-large-latest (Text-only)
- **Use case**: Regular chat messages without images
- **API endpoint**: `client.chat.complete()`
- **Max tokens**: 8192 context
- **Response time**: ~2-5 seconds
- **Cost**: $0.002 per 1K tokens (input)

#### pixtral-large-latest (Vision)
- **Use case**: Messages with screenshots/images
- **API endpoint**: Same, but with image_url in content
- **Image format**: base64 encoded PNG/JPEG
- **Max image size**: 5MB (enforced by Flask)
- **Response time**: ~5-10 seconds (image processing)
- **Cost**: $0.004 per 1K tokens (higher due to vision)

### API Request Flow

#### Text-only Message
```python
# bot.py
response = mistral_client.chat.complete(
    model="mistral-large-latest",
    messages=[
        {"role": "system", "content": "You are a helpful AI assistant..."},
        {"role": "user", "content": "Explain Python decorators"}
    ],
    stream=True  # Server-Sent Events for real-time response
)

for chunk in response:
    if chunk.data.choices[0].delta.content:
        yield chunk.data.choices[0].delta.content
```

#### Vision Message
```python
# bot.py
with open(image_path, 'rb') as img_file:
    image_base64 = base64.b64encode(img_file.read()).decode('utf-8')

response = mistral_client.chat.complete(
    model="pixtral-large-latest",
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user_message},
                {"type": "image_url", "image_url": f"data:image/png;base64,{image_base64}"}
            ]
        }
    ]
)
```

### Error Handling

#### API Failures
```python
try:
    response = mistral_client.chat.complete(...)
except Exception as e:
    return jsonify({
        'error': 'AI service unavailable',
        'details': str(e)
    }), 503
```

#### Rate Limiting
- No explicit rate limiting in code
- Relies on Mistral API tier limits
- Should implement: Token bucket algorithm

#### Timeout Handling
- No timeout set (default requests timeout)
- Should implement: 30-second timeout

---

## File Structure

```
AzikiAI-codingbot/
│
├── bot.py                          # Main Flask app (700+ lines)
├── chatbot_sql.py                  # Database module (200 lines)
├── old_chatbot_sql.py              # Legacy backup
├── start.sh                        # Startup script (31 lines, has bugs)
├── README.md                       # Project readme
├── STRUCTURE.md                    # File structure doc
│
├── azikiai_users.db                # SQLite database
│
├── static/                         # Static assets
│   ├── css/
│   │   ├── main.css                # Import hub (23 lines)
│   │   ├── base.css                # Foundation (476 lines)
│   │   ├── cisco-theme.css         # Prism Cisco dark (88 lines)
│   │   ├── cisco-light-theme.css   # Prism Cisco light (97 lines)
│   │   └── themes/
│   │       ├── cisco.css           # Default dark theme (17 lines)
│   │       ├── vscode.css          # VS Code dark (17 lines)
│   │       ├── monokai.css         # Sublime Text (17 lines)
│   │       ├── dracula.css         # Gothic purple (17 lines)
│   │       ├── nord.css            # Arctic frost (17 lines)
│   │       ├── solarized.css       # Lab-tested colors (17 lines)
│   │       ├── github.css          # GitHub dark (17 lines)
│   │       ├── light-theme.css     # Standard light (185 lines)
│   │       ├── light-quiet-theme.css # Purple light (182 lines)
│   │       └── quiet-light-theme.css # Prism light (171 lines)
│   │
│   ├── js/
│   │   ├── message-handler.js      # Main controller (300+ lines)
│   │   ├── code-detector.js        # Syntax detection (150 lines)
│   │   ├── message-parser.js       # Markdown parser (200 lines)
│   │   ├── prism-cisco.js          # Cisco syntax (100 lines)
│   │   ├── themes.js               # Theme switcher (80 lines)
│   │   ├── session-timeout.js      # Timeout handler (100 lines)
│   │   └── ui-handlers.js          # UI interactions (150 lines)
│   │
│   ├── images/
│   │   ├── kali-layers.png         # Dark theme watermark
│   │   ├── kali-layers-light2.jpeg # Light theme watermark
│   │   └── kali-layers-quiet2.jpeg # Quiet theme watermark
│   │
│   └── uploads/                    # User-uploaded screenshots
│       └── (dynamic content)
│
├── templates/
│   ├── index.html                  # Main chat UI (500+ lines)
│   ├── login.html                  # Login page (100 lines)
│   └── index_monolith.html.backup  # Old version backup
│
├── venv/                           # Python virtual environment
│   ├── bin/
│   ├── lib/
│   └── pyvenv.cfg
│
└── docs/                           # Documentation (NEW)
    ├── backend/
    │   ├── bot.py-PART1-DETAILED.md
    │   ├── bot.py-PART2-DETAILED.md
    │   ├── bot.py-PART3-DETAILED.md
    │   └── chatbot_sql.py-DETAILED.md
    │
    ├── frontend/
    │   ├── index.html-DETAILED.md
    │   ├── login.html-DETAILED.md
    │   ├── message-handler.js-DETAILED.md
    │   ├── code-detector.js-DETAILED.md
    │   ├── message-parser.js-DETAILED.md
    │   ├── prism-cisco.js-DETAILED.md
    │   ├── themes.js-DETAILED.md
    │   ├── session-timeout.js-DETAILED.md
    │   ├── ui-handlers.js-DETAILED.md
    │   ├── main.css-DETAILED.md
    │   ├── base.css-DETAILED.md
    │   ├── DARK-THEMES-DETAILED.md
    │   ├── LIGHT-THEMES-DETAILED.md
    │   └── PRISM-THEMES-DETAILED.md
    │
    ├── SUPPORT-FILES-DETAILED.md
    ├── DOCUMENTATION-STATUS.md
    └── PROJECT-OVERVIEW.md (this file)
```

### File Size Statistics

#### Python Backend
- **bot.py**: ~700 lines (main app)
- **chatbot_sql.py**: ~200 lines (database)
- **Total backend**: ~900 lines Python

#### HTML Templates
- **index.html**: ~500 lines (chat UI)
- **login.html**: ~100 lines (login form)
- **Total HTML**: ~600 lines

#### JavaScript Frontend
- **message-handler.js**: ~300 lines
- **message-parser.js**: ~200 lines
- **code-detector.js**: ~150 lines
- **ui-handlers.js**: ~150 lines
- **prism-cisco.js**: ~100 lines
- **session-timeout.js**: ~100 lines
- **themes.js**: ~80 lines
- **Total JavaScript**: ~1,080 lines

#### CSS Styling
- **base.css**: 476 lines (foundation)
- **main.css**: 23 lines (imports)
- **Theme CSS**: ~1,000 lines total (11 themes)
- **Prism CSS**: ~350 lines (3 syntax themes)
- **Total CSS**: ~1,850 lines

#### Grand Total Codebase
**~4,400 lines of code** (excluding documentation)

---

## Deployment

### Current Setup

#### Hardware
- **Device**: Raspberry Pi 5 (4GB RAM)
- **OS**: Raspberry Pi OS (Debian-based Linux)
- **IP Address**: 192.168.0.80 (static)
- **Network**: Local network (192.168.0.0/24)

#### Software Stack
```bash
# OS
$ uname -a
Linux pi 6.1.0-rpi4-rpi-v8 #1 SMP PREEMPT Debian ... aarch64 GNU/Linux

# Python
$ python3 --version
Python 3.11.2

# Flask
$ flask --version
Flask 3.0.0
Werkzeug 3.0.1
```

#### Running Process
```bash
# Check if running
$ ps aux | grep bot.py
kasperadm  1234  5.2  8.3 245672 167344 ?  Ssl  10:30  0:15 python bot.py

# Port listening
$ netstat -tuln | grep 5000
tcp        0      0 0.0.0.0:5000            0.0.0.0:*               LISTEN
```

### Startup Methods

#### Method 1: Using start.sh (Has Bugs)
```bash
cd /home/kasperadm/projects/AzikiAI-codingbot
./start.sh
```
**Issues**:
- Runs `python main.py` (should be `bot.py`)
- Says `https://` (should be `http://`)

#### Method 2: Manual (Recommended)
```bash
cd /home/kasperadm/projects/AzikiAI-codingbot
source venv/bin/activate
python bot.py
```

#### Method 3: Systemd Service (Production)
```bash
# Create service file
sudo nano /etc/systemd/system/azikiai.service

# Content:
[Unit]
Description=AzikiAI Chatbot
After=network.target

[Service]
Type=simple
User=kasperadm
WorkingDirectory=/home/kasperadm/projects/AzikiAI-codingbot
Environment="PATH=/home/kasperadm/projects/AzikiAI-codingbot/venv/bin"
ExecStart=/home/kasperadm/projects/AzikiAI-codingbot/venv/bin/python bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable azikiai.service
sudo systemctl start azikiai.service

# Check status
sudo systemctl status azikiai.service
```

### Access URLs

#### Local Network
- **Main URL**: http://192.168.0.80:5000
- **Login**: http://192.168.0.80:5000/login
- **API**: http://192.168.0.80:5000/api/chat

#### From Pi Itself
- **Localhost**: http://localhost:5000
- **127.0.0.1**: http://127.0.0.1:5000

#### External Access (If Port Forwarding Enabled)
- Would need: Router port forward 5000 → 192.168.0.80:5000
- **Security risk**: Flask debug mode, no HTTPS
- **Not recommended** without: HTTPS, firewall, rate limiting

---

## Configuration

### .env File (Required)

```env
# Mistral AI API (REQUIRED)
MISTRAL_API_KEY=your_mistral_api_key_here

# Flask Secret Key (REQUIRED)
SECRET_KEY=your_random_secret_key_here_32_characters_minimum

# LDAP Configuration (OPTIONAL - falls back to SQLite)
LDAP_SERVER=ldap://192.168.0.153
LDAP_USER_DN=CN=ldapuser,CN=Users,DC=domain,DC=local
LDAP_PASSWORD=ldap_password_here
LDAP_SEARCH_BASE=DC=domain,DC=local

# Admin Credentials (OPTIONAL - for SQLite fallback)
ADMIN_USERNAME=admin
ADMIN_PASSWORD=pbkdf2:sha256:260000$...hashed_password...

# Flask Configuration (OPTIONAL)
FLASK_ENV=production
FLASK_DEBUG=False
MAX_CONTENT_LENGTH=5242880  # 5MB max upload
```

### Environment Variables Used

#### bot.py
```python
mistral_api_key = os.getenv('MISTRAL_API_KEY')
app.secret_key = os.getenv('SECRET_KEY')
ldap_server = os.getenv('LDAP_SERVER')
ldap_user_dn = os.getenv('LDAP_USER_DN')
ldap_password = os.getenv('LDAP_PASSWORD')
ldap_search_base = os.getenv('LDAP_SEARCH_BASE')
```

#### Default Values (If .env Missing)
```python
# In bot.py (NOT RECOMMENDED - hardcoded fallbacks)
mistral_api_key = os.getenv('MISTRAL_API_KEY', 'default_key_placeholder')
app.secret_key = os.getenv('SECRET_KEY', 'default_insecure_key')
```

### Requirements (Python Packages)

#### Current Installation (via start.sh)
```bash
pip install flask python-dotenv mistralai
```

#### Full Requirements (Recommended requirements.txt)
```txt
Flask==3.0.0
python-dotenv==1.0.0
mistralai==0.1.8
ldap3==2.9.1
requests==2.31.0
Pillow==10.1.0
Werkzeug==3.0.1
```

#### Install All
```bash
pip install -r requirements.txt
```

---

## Documentation Index

### Backend Documentation
1. **bot.py-PART1-DETAILED.md**
   - Imports and Flask setup
   - Session configuration
   - Upload folder setup
   - Database initialization

2. **bot.py-PART2-DETAILED.md**
   - Login routes (/login GET/POST)
   - LDAP authentication
   - SQLite fallback
   - Session management

3. **bot.py-PART3-DETAILED.md**
   - Chat routes (/api/chat, /api/upload)
   - AI integration (text-only vs Vision)
   - Image processing
   - Stream responses

4. **chatbot_sql.py-DETAILED.md**
   - Database schema (users, messages)
   - CRUD operations
   - Connection pooling
   - Error handling

### Frontend Documentation

#### HTML
5. **index.html-DETAILED.md**
   - 3-panel layout structure
   - Message rendering
   - File upload UI
   - Theme/model selectors

6. **login.html-DETAILED.md**
   - Login form
   - Error handling
   - Redirect logic

#### JavaScript
7. **message-handler.js-DETAILED.md**
   - Main chat controller
   - API requests
   - Message display
   - Upload handling

8. **code-detector.js-DETAILED.md**
   - Language detection
   - Pattern matching
   - Confidence scoring

9. **message-parser.js-DETAILED.md**
   - Markdown to HTML
   - Code block creation
   - XSS prevention

10. **prism-cisco.js-DETAILED.md**
    - Cisco IOS grammar
    - Token definitions
    - Regex patterns

11. **themes.js-DETAILED.md**
    - Theme switcher
    - LocalStorage persistence
    - Watermark filters

12. **session-timeout.js-DETAILED.md**
    - Inactivity detection
    - Warning modal
    - Auto-logout

13. **ui-handlers.js-DETAILED.md**
    - Copy to clipboard
    - Panel toggling
    - Scroll management

#### CSS
14. **main.css-DETAILED.md**
    - Import structure
    - Load order
    - Performance analysis

15. **base.css-DETAILED.md**
    - CSS variables
    - 3-panel layout
    - Watermark
    - Message bubbles
    - Code blocks
    - Animations

16. **DARK-THEMES-DETAILED.md**
    - cisco, vscode, monokai
    - dracula, nord, solarized, github
    - Color psychology
    - Comparison table

17. **LIGHT-THEMES-DETAILED.md**
    - light-theme.css (gray buttons)
    - light-quiet-theme.css (purple/pink)
    - Override strategies

18. **PRISM-THEMES-DETAILED.md**
    - cisco-theme.css (SecureCRT colors)
    - cisco-light-theme.css (dark colors for light bg)
    - quiet-light-theme.css (VS Code Quiet Light)

### Support Files
19. **SUPPORT-FILES-DETAILED.md**
    - start.sh analysis
    - Missing test files
    - requirements.txt recommendations
    - Bugs and fixes

### Overview
20. **PROJECT-OVERVIEW.md** (this file)
    - Complete architecture
    - Component interaction
    - Deployment guide
    - Configuration reference

---

## Key Features

### 1. Mistral Vision Integration
- Upload screenshots directly in chat
- AI analyzes network diagrams, code screenshots, error messages
- Automatic model selection (Vision vs text-only)

### 2. Multi-Language Code Highlighting
- Python, JavaScript, HTML, CSS syntax
- Custom Cisco IOS configuration highlighting
- 27 Cisco token types (prompts, interfaces, IPs, keywords)
- SecureCRT color matching

### 3. Theme System
- 11 themes total (7 dark, 2 light, 2 Prism variants)
- Instant switching (no page reload)
- CSS variables for consistency
- LocalStorage persistence

### 4. LDAP Integration
- Active Directory authentication
- SQLite fallback if LDAP unavailable
- Secure password hashing (pbkdf2:sha256)

### 5. Session Management
- 24-hour sessions
- Inactivity warnings
- Auto-logout
- Heartbeat keep-alive

### 6. Code Block Features
- One-click copy to clipboard
- Click to expand in side panel
- Language auto-detection
- Syntax highlighting with Prism.js

### 7. Message History
- All conversations logged to database
- Per-user message retrieval
- Includes images and timestamps

---

## Known Issues & Future Improvements

### Critical Bugs
1. **start.sh**: Runs `main.py` instead of `bot.py`
2. **start.sh**: Shows `https://` URL (should be `http://`)
3. **No requirements.txt**: Dependencies hardcoded in start.sh

### Security Concerns
1. **No HTTPS**: All traffic unencrypted
2. **No rate limiting**: Vulnerable to API abuse
3. **No CSRF protection**: Forms lack tokens
4. **Debug mode**: May expose stack traces
5. **Hardcoded secrets**: Fallback keys in code

### Performance Improvements
1. **No caching**: Repeated API calls
2. **No pagination**: Loads all messages
3. **No image compression**: 5MB uploads allowed
4. **No CDN**: All assets served locally

### Feature Requests
1. **Conversation branching**: Multiple threads per user
2. **Message editing**: Edit/delete past messages
3. **File attachments**: PDF, text files
4. **Voice input**: Speech-to-text
5. **Export chat**: Download as PDF/HTML
6. **Multi-user chat**: Group conversations
7. **Code execution**: Run Python in sandbox
8. **Prompt templates**: Saved prompts
9. **Search history**: Full-text search
10. **Mobile responsive**: Better mobile UI

---

## Development Workflow

### Adding New Features

#### Backend Changes
```bash
# 1. Edit bot.py or chatbot_sql.py
nano bot.py

# 2. Test locally
source venv/bin/activate
python bot.py

# 3. Access http://localhost:5000
# 4. Test functionality
# 5. Check logs for errors
```

#### Frontend Changes
```bash
# 1. Edit HTML/CSS/JS files
nano templates/index.html
nano static/css/base.css
nano static/js/message-handler.js

# 2. Hard refresh browser (Ctrl+Shift+R)
# 3. Check browser console (F12)
# 4. Test UI interactions
```

#### Database Changes
```bash
# 1. Update schema in chatbot_sql.py
nano chatbot_sql.py

# 2. Delete database (for testing only)
rm azikiai_users.db

# 3. Restart app (recreates DB)
python bot.py
```

### Testing

#### Unit Tests (Not Implemented)
```python
# tests/test_bot.py (should create)
import unittest
from bot import app

class TestBot(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        
    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
```

#### Manual Testing Checklist
- [ ] Login with LDAP credentials
- [ ] Login with SQLite credentials
- [ ] Send text message
- [ ] Upload screenshot
- [ ] Switch themes
- [ ] Copy code block
- [ ] Check session timeout
- [ ] Test logout
- [ ] Verify message history

---

## Troubleshooting

### Common Issues

#### "MISTRAL_API_KEY not found"
```bash
# Solution: Create .env file
echo "MISTRAL_API_KEY=your_key_here" > .env
```

#### "Address already in use"
```bash
# Solution: Kill existing process
ps aux | grep bot.py
kill -9 <PID>

# Or use different port
# In bot.py: app.run(port=5001)
```

#### "Permission denied: venv/bin/activate"
```bash
# Solution: Make executable
chmod +x venv/bin/activate
```

#### "LDAP connection failed"
```bash
# Solution: Check LDAP server
ping 192.168.0.153

# Check LDAP settings in .env
grep LDAP .env

# Test with ldapsearch
ldapsearch -x -H ldap://192.168.0.153 -D "CN=ldapuser,..." -W
```

#### "Database is locked"
```bash
# Solution: Close other connections
fuser azikiai_users.db
kill -9 <PID>

# Or delete lock file
rm azikiai_users.db-journal
```

---

## Performance Metrics

### Response Times (Approximate)

| Operation | Time | Notes |
|-----------|------|-------|
| Page load | ~500ms | Including all CSS/JS |
| Login (LDAP) | ~200ms | Active Directory lookup |
| Login (SQLite) | ~50ms | Local database |
| Text message | ~2-5s | Mistral API latency |
| Vision message | ~5-10s | Image processing + AI |
| Theme switch | <100ms | CSS change only |
| Copy code | <50ms | Clipboard API |

### Resource Usage

#### Raspberry Pi 5 (During Active Use)
```bash
# CPU
$ top -n 1 | grep python
kasperadm  1234  5.2  8.3 245672 167344 S  10:30  0:15 python bot.py
# ~5% CPU idle, ~50% during AI response

# Memory
$ free -h
              total        used        free
Mem:          3.8Gi       1.2Gi       2.1Gi
# ~300MB for Flask app
# ~800MB peak during Vision API

# Disk
$ du -sh azikiai_users.db
4.5M    azikiai_users.db
# ~100KB per 1000 messages
```

---

## Security Best Practices

### Implemented
✅ Password hashing (pbkdf2:sha256)
✅ Session management (Flask sessions)
✅ File upload restrictions (5MB, image only)
✅ XSS prevention (HTML escaping)

### Missing (Should Implement)
❌ HTTPS/TLS encryption
❌ CSRF protection
❌ Rate limiting
❌ SQL injection prevention (using SQLite safely, but not parameterized everywhere)
❌ Input validation (size, format)
❌ Security headers (CSP, X-Frame-Options)
❌ API key rotation
❌ Audit logging

### Recommendations
```python
# 1. Add Flask-Talisman for HTTPS
from flask_talisman import Talisman
Talisman(app, force_https=True)

# 2. Add Flask-Limiter for rate limiting
from flask_limiter import Limiter
limiter = Limiter(app, default_limits=["100 per hour"])

# 3. Add CSRF protection
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# 4. Validate all inputs
from wtforms import StringField, validators
username = StringField('Username', [validators.Length(min=3, max=25)])
```

---

## Conclusion

AzikiAI Chatbot er et komplet Flask-baseret AI chat system med:
- **Mistral Vision integration** - Billede analyse
- **Multi-theme UI** - 11 temaer med Cisco SecureCRT farver
- **LDAP + SQLite auth** - Fleksibel autentifikation
- **Custom syntax highlighting** - Specialiseret til Cisco IOS
- **Session management** - 24-timers sessions med timeout
- **Database logging** - Komplet beskedhistorik

**Total kodebase**: ~4,400 linjer kode + ~20,000 linjer dokumentation

**Deployment**: Raspberry Pi 5 @ 192.168.0.80:5000

**Dokumentation**: Komplet line-by-line forklaring af alle filer i docs/ mappen.
