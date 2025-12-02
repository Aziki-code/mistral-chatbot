#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_ldap3_login import LDAP3LoginManager
from flask_ldap3_login.forms import LDAPLoginForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv
import os
import sqlite3
import logging

# --- Load .env FIRST before any other imports that need environment variables ---
load_dotenv()

# Import Bot Manager AFTER loading .env
from bot_manager import get_bot_manager

# --- Configure Logging ---
log_dir = os.path.join(os.path.dirname(__file__), 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_dir, 'azikiai.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Initialize Bot Manager (handles all AI bots) ---
try:
    bot_manager = get_bot_manager()
    logger.info("Bot manager initialized successfully")
except Exception as e:
    logger.critical(f"Failed to initialize bot manager: {e}")
    raise

# --- Flask app ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-secret-key-in-production')

# --- Rate Limiting ---
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

# --- LDAP Configuration ---
app.config['LDAP_HOST'] = os.getenv('LDAP_HOST')
app.config['LDAP_BASE_DN'] = os.getenv('LDAP_BASE_DN')
app.config['LDAP_USER_DN'] = os.getenv('LDAP_USER_SEARCH_BASE', 'CN=Users,DC=Area51,DC=local')
app.config['LDAP_GROUP_DN'] = ''
app.config['LDAP_USER_RDN_ATTR'] = 'cn'  # Changed from sAMAccountName to cn
app.config['LDAP_USER_LOGIN_ATTR'] = 'sAMAccountName'
app.config['LDAP_BIND_USER_DN'] = None  # Use direct bind instead of service account
app.config['LDAP_BIND_USER_PASSWORD'] = None
app.config['LDAP_USE_SSL'] = True
app.config['LDAP_BIND_DIRECT_CREDENTIALS'] = True  # Enable direct credential binding
app.config['LDAP_BIND_DIRECT_SUFFIX'] = ''  # Will use full DN
app.config['LDAP_BIND_DIRECT_GET_USER_INFO'] = True

# SSL/TLS Configuration - Don't validate certificate for internal AD
import ssl
from ldap3 import Tls
tls_configuration = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
app.config['LDAP_TLS_CONFIG'] = tls_configuration

# --- Flask-Login Setup ---
login_manager = LoginManager(app)
login_manager.login_view = 'login'
ldap_manager = LDAP3LoginManager(app)

# User class for Flask-Login
class User(UserMixin):
    def __init__(self, dn, username, data):
        self.dn = dn
        self.username = username
        self.data = data

    def __repr__(self):
        return self.dn

    def get_id(self):
        return self.dn

@login_manager.user_loader
def load_user(user_id):
    # Return a user object based on the user_id (DN)
    return User(user_id, user_id.split(',')[0].split('=')[1], {})

@ldap_manager.save_user
def save_user(dn, username, data, memberships):
    # Create and return user object after successful LDAP authentication
    return User(dn, username, data)

# --- SQLite setup ---
db_path = os.path.join(os.path.dirname(__file__), "chat_history.db")

def get_db_connection():
    """Create a new database connection"""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database schema"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
    finally:
        conn.close()

# Initialize database on startup
init_db()

# --- Helper Functions ---
def detect_language(code: str) -> str:
    """
    Detect programming language from code content
    
    Args:
        code: Code string to analyze
        
    Returns:
        str: Language identifier (e.g., 'python', 'html', 'javascript')
    """
    code_lower = code.lower()
    
    language_patterns = {
        'html': ['<html', '<!doctype', '<div', '<script>'],
        'python': ['def ', 'import ', 'print(', 'class ', '__init__'],
        'javascript': ['function', 'const ', 'let ', 'var ', '=>'],
        'java': ['public class', 'private ', 'void main'],
        'css': ['{', '}', 'color:', 'background:'],
        'sql': ['select ', 'from ', 'where ', 'insert into'],
    }
    
    for lang, patterns in language_patterns.items():
        if any(pattern in code_lower for pattern in patterns):
            return lang
    
    return 'plaintext'

# --- Upload folder ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
@login_required
def index():
    # Pass available AI bots info to template
    return render_template("index.html", 
                         mistral_available=bot_manager.is_bot_available("mistral"),
                         github_available=bot_manager.is_bot_available("github-copilot"),
                         default_provider=bot_manager.get_default_bot().name)

@app.route("/debug")
@login_required
def debug():
    return render_template("debug.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Manual LDAP authentication using ldap3 directly
        try:
            from ldap3 import Server, Connection, ALL, Tls
            from ldap3.core.exceptions import LDAPException, LDAPBindError
            import ssl
            
            # LDAP server configuration from environment
            ldap_host = os.getenv('LDAP_HOST')
            ldap_port = int(os.getenv('LDAP_PORT', 636))
            base_dn = os.getenv('LDAP_BASE_DN')
            validate_ssl = os.getenv('LDAP_VALIDATE_SSL', 'false').lower() == 'true'
            
            # Create TLS configuration
            ssl_validation = ssl.CERT_REQUIRED if validate_ssl else ssl.CERT_NONE
            tls = Tls(validate=ssl_validation, version=ssl.PROTOCOL_TLSv1_2)
            server = Server(ldap_host, port=ldap_port, use_ssl=True, tls=tls, get_info=ALL)
            
            # Try to authenticate user with full DN
            user_dn = f"CN={username},CN=Users,{base_dn}"
            
            try:
                # Attempt to bind with user credentials
                conn = Connection(server, user=user_dn, password=password, auto_bind=True)
                
                # If we got here, authentication succeeded
                conn.unbind()
                
                # Create user object and log them in
                user = User(user_dn, username, {})
                login_user(user)
                logger.info(f"User {username} logged in successfully")
                return redirect(url_for('index'))
                
            except LDAPBindError:
                # Authentication failed
                logger.warning(f"Failed login attempt for user {username}")
                error_msg = "Invalid username or password"
                return render_template("login.html", error=error_msg)
                
        except LDAPException as e:
            logger.error(f"LDAP connection error: {e}")
            return render_template("login.html", error=f"LDAP Connection Error: {str(e)}")
        except ValueError as e:
            logger.error(f"Configuration error in login: {e}")
            return render_template("login.html", error=f"Configuration Error: {str(e)}")
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logger.info(f"User {current_user.username if hasattr(current_user, 'username') else 'unknown'} logged out")
    logout_user()
    return redirect(url_for('login'))

@app.route("/chat", methods=["POST"])
@login_required
@limiter.limit("30 per minute")
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    ai_model = data.get("ai_model", "mistral")  # Get selected AI model
    
    if not user_msg:
        return jsonify({"response": "No message sent."})
    
    # Check if selected bot is available
    if not bot_manager.is_bot_available(ai_model):
        bot_names = {"mistral": "Mistral AI", "github-copilot": "GitHub Copilot"}
        bot_name = bot_names.get(ai_model, ai_model)
        logger.warning(f"User attempted to use unavailable bot: {ai_model}")
        return jsonify({
            "response": f"⚠️ {bot_name} is not configured. Please check your .env file."
        })
    
    # Get the selected bot
    selected_bot = bot_manager.get_bot(ai_model)
    ai_provider = selected_bot.name
    
    if not user_msg:
        return jsonify({"response": "No message sent."})
    
    # Warn if message is very long but allow up to 100k chars (Mistral can handle ~32k tokens)
    truncated = False
    if len(user_msg) > 100000:
        user_msg = user_msg[:100000]
        truncated = True
    
    # Save user message WITHOUT HTML-escaping
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
        conn.commit()
    
        # Limit history based on AI model
        # GitHub Models has smaller context window
        if ai_model == "github-copilot":
            history_limit = 6  # Only last 3 exchanges (6 messages)
        else:
            history_limit = 20  # Mistral can handle more
    
        cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT ?", (history_limit,))
        history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
    finally:
        conn.close()
    
    # Add system prompt to ensure proper code formatting
    if not history or history[0].get("role") != "system":
        history.insert(0, {
            "role": "system",
            "content": f"You are {ai_provider}, a helpful coding assistant. When showing code, you MUST ALWAYS use fenced code blocks with triple backticks (```) and the language name. Example:\n```python\nprint('hello')\n```"
        })
    
    # Use bot manager to get response
    try:
        logger.info(f"Chat request using {ai_model} - message length: {len(user_msg)}")
        bot_msg = bot_manager.chat(
            bot_id=ai_model,
            messages=history,
            model="mistral-small-latest"
        )
    except Exception as e:
        logger.error(f"Error in chat with {ai_model}: {e}")
        bot_msg = f"❌ Error: {str(e)}"
    
    # Add truncation warning if message was cut
    if truncated:
        bot_msg = "⚠️ Your message was truncated to 100,000 characters due to length limits.\n\n" + bot_msg
    
    # Auto-detect and wrap code blocks if not already wrapped
    # Look for common code patterns (indented blocks, function definitions, etc.)
    import re
    
    # If response doesn't contain triple-backticks but has code-like content
    if '```' not in bot_msg:
        # Pattern: Multiple lines starting with common code keywords or significant indentation
        lines = bot_msg.split('\n')
        in_code_block = False
        result_lines = []
        code_buffer = []
        
        for i, line in enumerate(lines):
            # Detect code: starts with 4+ spaces, HTML tags, regex patterns, or has code keywords at start
            stripped = line.strip()
            is_code_line = (
                line.startswith('    ') or 
                line.startswith('\t') or
                re.match(r'^\s*<[^>]+>', line) or  # HTML tags
                (stripped and ('regex' in stripped.lower() or '=/.*/' in stripped or r'\n' in stripped or r'\s' in stripped)) or  # Regex patterns
                re.match(r'^\s*(def|class|function|const|let|var|if|for|while|import|from|#include|public|private)\s', line) or
                (stripped and re.match(r'^[a-zA-Z_]\w*\s*[=\(]', stripped))  # assignment or function call
            )
            
            if is_code_line and not in_code_block:
                # Start code block
                in_code_block = True
                code_buffer = [line]
            elif is_code_line and in_code_block:
                # Continue code block
                code_buffer.append(line)
            elif not is_code_line and in_code_block:
                # End code block if we have 3+ lines of code
                if len(code_buffer) >= 3:
                    # Detect language using helper function
                    lang = detect_language('\n'.join(code_buffer))
                    result_lines.append(f'```{lang}')
                    result_lines.extend(code_buffer)
                    result_lines.append('```')
                else:
                    # Too short, keep as regular text
                    result_lines.extend(code_buffer)
                
                code_buffer = []
                in_code_block = False
                result_lines.append(line)
            else:
                # Regular text line
                result_lines.append(line)
        
        # Handle any remaining code at end
        if in_code_block and len(code_buffer) >= 3:
            lang = detect_language('\n'.join(code_buffer))
            result_lines.append(f'```{lang}')
            result_lines.extend(code_buffer)
            result_lines.append('```')
        elif code_buffer:
            result_lines.extend(code_buffer)
        
        bot_msg = '\n'.join(result_lines)
    
    # Save bot response
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", bot_msg))
        conn.commit()
    finally:
        conn.close()
    
    return jsonify({"response": bot_msg})

@app.route("/upload", methods=["POST"])
@login_required
@limiter.limit("10 per minute")  # Add rate limiting for uploads
def upload():
    if "screendump" not in request.files:
        return jsonify({"response": "No file uploaded."})
    
    file = request.files["screendump"]
    if file.filename == "":
        return jsonify({"response": "No file selected."})
    
    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Analyze image with Mistral Vision
    try:
        bot = bot_manager.get_bot('mistral')
        if bot and bot.is_available:
            response_text = bot.analyze_image(
                file_path, 
                prompt="Analyze this screenshot. Describe what you see, identify any text, UI elements, code, or other relevant content."
            )
        else:
            response_text = f"Screenshot '{file.filename}' received and saved (vision analysis not available)."
    except Exception as e:
        logger.error(f"Error analyzing image: {str(e)}")
        response_text = f"Screenshot '{file.filename}' received and saved, but analysis failed: {str(e)}"
    
    # Save message to database
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", f"[Uploaded screenshot: {file.filename}]"))
        cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", response_text))
        conn.commit()
    finally:
        conn.close()
    
    return jsonify({"response": response_text})

@app.route("/history", methods=["GET"])
@login_required
def history():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 50")
        history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
        return jsonify({"history": history})
    finally:
        conn.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, ssl_context=('cert.pem','key.pem'))
