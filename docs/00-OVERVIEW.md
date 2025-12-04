# AzikiAI Coding Chatbot - Project Overview

## Project Description
AzikiAI Coding Chatbot is a web-based AI assistant application that provides an interactive chat interface for coding assistance. The application integrates with Mistral AI's API to provide intelligent responses with support for code snippets, syntax highlighting, and multiple visual themes.

## Technology Stack

### Backend
- **Python 3.x** - Core programming language
- **Flask** - Web framework for HTTP server and routing
- **SQLite** - Database for storing chat history and user sessions
- **Mistral AI API** - Large Language Model for generating responses
- **LDAP** - User authentication (optional)

### Frontend
- **HTML5** - Page structure
- **CSS3** - Styling with modular theme system
- **JavaScript (Vanilla)** - Client-side interactivity
- **Prism.js** - Syntax highlighting for code blocks

## Architecture Overview

```
AzikiAI-codingbot/
├── bot.py                 # Main Flask application and server
├── chatbot_sql.py         # Database operations and session management
├── static/                # Frontend assets
│   ├── css/              # Stylesheets (modular theme system)
│   ├── js/               # Client-side JavaScript modules
│   ├── images/           # Image assets (logos, backgrounds)
│   └── uploads/          # User uploaded files
├── templates/            # HTML templates (Jinja2)
└── docs/                 # Documentation (this folder)
```

## Key Features

### 1. Multi-Model AI Support
- Mistral Large (default)
- Mistral Small
- Mistral Vision (image analysis)
- Pixtral (vision model)

### 2. Theme System
Nine professionally designed themes:
- Cisco Theme (default) - Teal/cyan corporate design
- VS Code Dark - Microsoft VS Code inspired
- Monokai - Popular code editor theme
- Dracula - Purple-based dark theme
- Nord - Arctic blue palette
- Solarized - Low-contrast scientific design
- GitHub Light - Clean white theme
- Light Theme - Bright with dragon watermark
- Light Quiet - Minimalist light design

### 3. Code Handling
- Automatic code detection and syntax highlighting
- Clickable code block indicators with smooth scroll
- Copy-to-clipboard functionality
- Visual feedback (ripple glow effect)
- Pasted code preservation across multiple sends

### 4. User Experience
- Session-based chat history
- Persistent conversations (saved in SQLite)
- Automatic session timeout (15 minutes)
- Message alignment (user right, bot left)
- Real-time typing indicators
- Responsive design

### 5. Security Features
- Optional LDAP authentication
- Session management
- Secure file uploads
- SQL injection protection via parameterized queries

## Data Flow

### Request Flow (User Message → AI Response)
```
1. User types message in browser
   ↓
2. JavaScript captures input (ui-handlers.js)
   ↓
3. POST request to /chat endpoint (bot.py)
   ↓
4. Session validation (chatbot_sql.py)
   ↓
5. Message saved to database
   ↓
6. Request sent to Mistral AI API
   ↓
7. Response received and processed
   ↓
8. Response saved to database
   ↓
9. JSON response sent to browser
   ↓
10. JavaScript renders message (message-handler.js)
    ↓
11. Code detection and highlighting (code-detector.js)
    ↓
12. Theme styling applied
```

### Database Schema
```
users table:
- username (TEXT PRIMARY KEY)
- password (TEXT)

sessions table:
- session_id (TEXT PRIMARY KEY)
- username (TEXT)
- created_at (TIMESTAMP)
- last_activity (TIMESTAMP)

chat_history table:
- id (INTEGER PRIMARY KEY AUTOINCREMENT)
- session_id (TEXT)
- username (TEXT)
- message (TEXT)
- response (TEXT)
- timestamp (TIMESTAMP)
- model (TEXT)
```

## Network Configuration
- **Host**: 0.0.0.0 (all interfaces)
- **Port**: 5000
- **Static IP**: 192.168.0.80/24 (Raspberry Pi 5)
- **Access**: http://192.168.0.80:5000

## Document Structure

This documentation is organized as follows:

### Backend Documentation
1. **01-BACKEND-OVERVIEW.md** - Backend architecture overview
2. **bot.py-DETAILED.md** - Line-by-line documentation of main application
3. **chatbot_sql.py-DETAILED.md** - Line-by-line database module documentation

### Frontend Documentation
1. **01-FRONTEND-OVERVIEW.md** - Frontend architecture overview
2. **CSS-ARCHITECTURE.md** - CSS structure and theme system
3. **JAVASCRIPT-MODULES.md** - JavaScript module documentation
4. **HTML-TEMPLATES.md** - Template structure documentation

Each detailed file includes:
- Purpose and responsibilities
- Line-by-line code explanation
- Data flow diagrams
- Integration points
- Error handling
- Security considerations

## Getting Started

### Prerequisites
```bash
# Python packages
pip install flask mistralai python-ldap

# System packages (for LDAP)
sudo apt-get install libldap2-dev libsasl2-dev
```

### Running the Application
```bash
# Start the server
python bot.py

# Access in browser
http://192.168.0.80:5000
```

### Environment Variables
```bash
export MISTRAL_API_KEY="your-api-key-here"
```

## Future Enhancements
- File upload and analysis
- Multi-user concurrent sessions
- Chat export functionality
- Voice input/output
- Mobile app version
- Docker containerization

---

**Documentation Status**: In Progress  
**Last Updated**: December 3, 2025  
**Version**: 1.0  
**Author**: Aziki-code
