# Mistral Chatbot

Flask-based chatbot with Mistral AI, advanced code highlighting, and three-panel layout for optimal code review.

**Platform:** Developed and tested on Raspberry Pi 5 running Kali Linux 2025.4 (kali-rolling). Compatible with Ubuntu and other Linux distributions.

## Features
- Chat with Mistral AI (mistral-small-latest)
- **Custom Cisco IOS syntax highlighting** with SecureCRT-matching colors
- **Three-panel layout:**
  - Left: Pasted code preview with real-time syntax detection
  - Center: Chat conversation
  - Right: AI code output with syntax highlighting
- **Six dark themes:** VS Code Dark, Monokai, Dracula, Nord, Solarized Dark, Cisco
- Auto-detection for multiple languages (Cisco, HTML, Python, CSS, SQL, JavaScript)
- Upload and paste images
- Chat history in SQLite
- SSL support
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
pip install flask python-dotenv mistralai
```

4. Create `.env` file with your Mistral API key:
```
MISTRAL_API_KEY=your_api_key_here
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

## Structure
- `chatbot_sql.py` - Flask server with Mistral AI integration and message truncation
- `templates/index.html` - Frontend with three-panel layout and custom Cisco language definition
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
- `.env` file contains API key and is NOT uploaded to GitHub
- SSL certificates are NOT uploaded to GitHub
- Chat history is NOT uploaded to GitHub
