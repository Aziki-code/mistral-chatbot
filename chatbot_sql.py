#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_ldap3_login import LDAP3LoginManager
from flask_ldap3_login.forms import LDAPLoginForm
from dotenv import load_dotenv
from mistralai import Mistral
import os
import sqlite3

# --- Load .env ---
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    raise ValueError("MISTRAL_API_KEY not found in .env")

# --- Mistral client ---
client = Mistral(api_key=api_key)

# --- Flask app ---
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'change-this-secret-key-in-production')

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
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL
)
""")
conn.commit()

# --- Upload folder ---
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Manual LDAP authentication using ldap3 directly
        try:
            from ldap3 import Server, Connection, ALL, Tls
            import ssl
            
            # LDAP server configuration
            ldap_host = "192.168.0.82"
            ldap_port = 636
            base_dn = "DC=Area51,DC=local"
            
            # Create TLS configuration
            tls = Tls(validate=ssl.CERT_NONE, version=ssl.PROTOCOL_TLSv1_2)
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
                return redirect(url_for('index'))
                
            except Exception as bind_error:
                # Authentication failed
                error_msg = f"Invalid username or password"
                return render_template("login.html", error=error_msg)
                
        except Exception as e:
            print(f"LDAP Exception: {e}")
            import traceback
            traceback.print_exc()
            return render_template("login.html", error=f"LDAP Error: {str(e)}")
    
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    
    if not user_msg:
        return jsonify({"response": "No message sent."})
    
    # Warn if message is very long but allow up to 100k chars (Mistral can handle ~32k tokens)
    truncated = False
    if len(user_msg) > 100000:
        user_msg = user_msg[:100000]
        truncated = True
    
    # Save user message WITHOUT HTML-escaping
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
    conn.commit()
    
    # Only keep last 20 messages to prevent token overflow
    cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 20")
    history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
    
    # Add system prompt to ensure proper code formatting
    if not history or history[0].get("role") != "system":
        history.insert(0, {
            "role": "system",
            "content": "You are a helpful assistant. When showing code, you MUST ALWAYS use fenced code blocks with triple backticks (```) and the language name. Example:\n```python\nprint('hello')\n```"
        })
    
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=history
    )
    
    bot_msg = response.choices[0].message.content
    
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
                    # Detect language from first line
                    first_code = '\n'.join(code_buffer)
                    if '<html' in first_code.lower() or '<!doctype' in first_code.lower() or '<div' in first_code.lower() or '<script>' in first_code.lower():
                        lang = 'html'
                    elif 'def ' in first_code or 'import ' in first_code or 'print(' in first_code:
                        lang = 'python'
                    elif 'function' in first_code or 'const ' in first_code or 'let ' in first_code:
                        lang = 'javascript'
                    elif 'public class' in first_code or 'private ' in first_code:
                        lang = 'java'
                    else:
                        lang = 'plaintext'
                    
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
            first_code = '\n'.join(code_buffer)
            if '<html' in first_code.lower() or '<!doctype' in first_code.lower() or '<div' in first_code.lower() or '<script>' in first_code.lower():
                lang = 'html'
            elif 'def ' in first_code or 'import ' in first_code or 'print(' in first_code:
                lang = 'python'
            elif 'function' in first_code or 'const ' in first_code:
                lang = 'javascript'
            else:
                lang = 'plaintext'
            result_lines.append(f'```{lang}')
            result_lines.extend(code_buffer)
            result_lines.append('```')
        elif code_buffer:
            result_lines.extend(code_buffer)
        
        bot_msg = '\n'.join(result_lines)
    
    # Gem bot-besked
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", bot_msg))
    conn.commit()
    
    return jsonify({"response": bot_msg})

@app.route("/upload", methods=["POST"])
@login_required
def upload():
    if "screendump" not in request.files:
        return jsonify({"response": "No file uploaded."})
    
    file = request.files["screendump"]
    if file.filename == "":
        return jsonify({"response": "No file selected."})
    
    # Save file
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # Add analysis here if needed (OCR, Mistral AI, etc.)
    response_text = f"Screenshot '{file.filename}' received and saved."
    
    # Save message to database
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", f"[Uploaded screenshot: {file.filename}]"))
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", response_text))
    conn.commit()
    
    return jsonify({"response": response_text})

@app.route("/history", methods=["GET"])
@login_required
def history():
    cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 50")
    history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
    return jsonify({"history": history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, ssl_context=('cert.pem','key.pem'))
