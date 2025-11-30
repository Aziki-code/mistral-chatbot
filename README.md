# Mistral Chatbot

Flask-based chatbot with Mistral AI, code highlighting and upload functionality.

**Platform:** Developed and tested on Raspberry Pi 5 running Kali Linux 2025.4 (kali-rolling). Compatible with Ubuntu and other Linux distributions.

## Features
- Chat with Mistral AI (mistral-small-latest)
- Syntax highlighting via Prism.js
- Upload and paste images
- Chat history in SQLite
- SSL support

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
- `chatbot_sql.py` - Flask server and Mistral integration
- `templates/index.html` - Frontend with robust code parsing
- `static/uploads/` - Uploaded images
- `chat_history.db` - SQLite database (auto-generated)

## Security
- `.env` file contains API key and is NOT uploaded to GitHub
- SSL certificates are NOT uploaded to GitHub
- Chat history is NOT uploaded to GitHub
