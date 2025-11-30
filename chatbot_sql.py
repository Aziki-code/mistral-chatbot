#!/usr/bin/env python3
from flask import Flask, request, jsonify, render_template
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
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    
    if not user_msg:
        return jsonify({"response": "No message sent."})
    
    # Save user message WITHOUT HTML-escaping
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
    conn.commit()
    
    cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 50")
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
def history():
    cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 50")
    history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
    return jsonify({"history": history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, ssl_context=('cert.pem','key.pem'))
