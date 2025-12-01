# AzikiAI-codingbot

Enterprise-grade AI coding assistant powered by Mistral AI with LDAP authentication, advanced code highlighting, and three-panel layout for optimal code review.

**Platform:** Developed and tested on Raspberry Pi 5 running Kali Linux 2025.4 (kali-rolling). Compatible with Ubuntu and other Linux distributions.

## Features
- **Mistral AI Integration:** Chat with mistral-small-latest for intelligent code assistance
- **LDAP Authentication:** Secure Active Directory integration with session management
- **Session Security:** Automatic logout after 10 minutes of inactivity
- **Custom Cisco IOS syntax highlighting** with SecureCRT-matching colors
- **Three-panel layout:**
  - Left: Pasted code preview with real-time syntax detection
  - Center: Chat conversation
  - Right: AI code output with syntax highlighting
- **Eight professional themes:** Cisco (default), VS Code Dark, Monokai, Dracula, Nord, Solarized Dark, Quiet Light, GitHub Dark
- Auto-detection for multiple languages (Cisco, HTML, Python, CSS, SQL, JavaScript)
- Upload and paste images
- Chat history in SQLite
- SSL/TLS support
- Copy-to-clipboard for all code blocks

## Installation

1. Clone the project
2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install flask python-dotenv mistralai flask-login flask-ldap3-login ldap3
```

4. Create `.env` file with your configuration:
```
MISTRAL_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
LDAP_HOST=your_ldap_server_ip
LDAP_BASE_DN=DC=YourDomain,DC=local
LDAP_USER_SEARCH_BASE=CN=Users,DC=YourDomain,DC=local
```

5. Generate SSL certificates (optional):
```bash
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

## Running

### Quick start (Linux):
```bash
./start.sh
```

### As systemd service:
```bash
sudo systemctl start mistral-chatbot
```

### Direct:
```bash
python chatbot_sql.py
```

Access at: `https://localhost:5000` or `https://[your-pi-ip]:5000`

**Login:** Use your Active Directory credentials (username and password from configured LDAP domain)

## Authentication
- **LDAP/Active Directory integration** for secure user authentication
- **Session management** with Flask-Login
- **Automatic session timeout** after 10 minutes of inactivity
- **Secure logout** functionality
- All routes require authentication except login page

## Structure
- `chatbot_sql.py` - Flask server with Mistral AI integration, LDAP authentication, and message truncation
- `templates/index.html` - Main chatbot interface with three-panel layout
- `templates/login.html` - LDAP login page
- `static/js/session-timeout.js` - Auto-logout after inactivity
- `static/uploads/` - Uploaded images
- `chat_history.db` - SQLite database (auto-generated)

## Cisco Syntax Highlighting
Custom Prism.js language definition for Cisco IOS with 85+ keyword patterns:
- **Interfaces:** GigabitEthernet, FastEthernet, Vlan (orange)
- **IP addresses:** Highlighted in green
- **Good keywords:** permit, up, running (green)
- **Bad keywords:** no, shutdown, deny, down (red)
- **Important keywords:** erase, delete, reload (red bold)
- **Comments:** Lines starting with ! (green)
- **Auto-detection:** Automatically detects Cisco configs without language tags

Based on SecureCRT color scheme for accurate network engineer experience.

## Security
- LDAP/Active Directory authentication required for all access
- Session management with automatic timeout (10 minutes)
- `.env` file contains API key and secrets - NOT uploaded to GitHub
- SSL/TLS certificates are NOT uploaded to GitHub
- Chat history is NOT uploaded to GitHub
- Certificate validation disabled for internal AD (configure for production)
