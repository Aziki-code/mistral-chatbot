# AzikiAI-codingbot

Enterprise-grade AI coding assistant powered by **GitHub Copilot** or Mistral AI with LDAP authentication, advanced code highlighting, and three-panel layout for optimal code review.

**Platform:** Developed and tested on Raspberry Pi 5 running Kali Linux 2025.4 (kali-rolling). Compatible with Ubuntu and other Linux distributions.

## Features
- **🤖 Dual AI Support:** GitHub Copilot (primary) with Mistral AI fallback
- **🔄 Dynamic AI Switching:** Choose between AI models in real-time via dropdown menu
- **GitHub Copilot Integration:** Use your GitHub credentials for enterprise-grade AI assistance
- **Mistral AI Integration:** Alternative AI backend with mistral-small-latest
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
pip install flask python-dotenv requests mistralai flask-login flask-ldap3-login ldap3
```

4. Create `.env` file with your configuration:
```bash
# Option 1: Using GitHub Copilot (Recommended)
GITHUB_TOKEN=your_github_personal_access_token
SECRET_KEY=your_secret_key_here
LDAP_HOST=your_ldap_server_ip
LDAP_BASE_DN=DC=YourDomain,DC=local
LDAP_USER_SEARCH_BASE=CN=Users,DC=YourDomain,DC=local

# Option 2: Using Mistral AI (Fallback)
# If GITHUB_TOKEN is not set, the bot will use Mistral AI
MISTRAL_API_KEY=your_mistral_api_key_here
SECRET_KEY=your_secret_key_here
LDAP_HOST=your_ldap_server_ip
LDAP_BASE_DN=DC=YourDomain,DC=local
LDAP_USER_SEARCH_BASE=CN=Users,DC=YourDomain,DC=local
```

**Getting GitHub Token:**
1. Go to https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Select scopes: `read:user` and if available `copilot`
4. Copy the token to your `.env` file

**Note:** You can use both tokens - the bot will prefer GitHub Copilot if available.

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
python main.py
```

Access at: `https://localhost:5000` or `https://[your-pi-ip]:5000`

**Login:** Use your Active Directory credentials (username and password from configured LDAP domain)

## Using the AI Model Selector

After logging in, you'll see an **AI Model** dropdown in the top-left corner:

- **🤖 Mistral AI** - Fast and efficient French AI model, great for general coding tasks
- **💻 GitHub Copilot** - Powered by GPT-4, excellent for complex coding and debugging

**Features:**
- Switch between models anytime during your session
- Your choice is remembered (saved in browser localStorage)
- Only configured models appear in the dropdown
- If only one model is configured, the dropdown is disabled
- Visual notification when switching models

**Tips:**
- Use Mistral AI for quick responses and general questions
- Use GitHub Copilot for advanced code generation and complex debugging
- Both models support all features (code highlighting, Cisco syntax, etc.)

## Authentication
- **LDAP/Active Directory integration** for secure user authentication
- **Session management** with Flask-Login
- **Automatic session timeout** after 10 minutes of inactivity
- **Secure logout** functionality
- All routes require authentication except login page

## Structure
- `main.py` - Flask server with GitHub Copilot/Mistral AI integration, LDAP authentication, and message truncation
- `bot_manager.py` - Central bot manager that orchestrates all AI bots
- `mistral_bot.py` - Mistral AI bot implementation
- `github_copilot_bot.py` - GitHub Copilot bot implementation
- `base_bot.py` - Abstract base class for all bots
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
