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
    raise ValueError("MISTRAL_API_KEY ikke fundet i .env")

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

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "")
    
    if not user_msg:
        return jsonify({"response": "Ingen besked sendt."})
    
    # Gem brugerbesked UDEN HTML-escaping
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_msg))
    conn.commit()
    
    cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 50")
    history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
    
    response = client.chat.complete(
        model="mistral-small-latest",
        messages=history
    )
    
    bot_msg = response.choices[0].message.content
    
    # Gem bot-besked UDEN HTML-escaping - frontend håndterer det
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", bot_msg))
    conn.commit()
    
    # Send rå besked til frontend
    return jsonify({"response": bot_msg})

@app.route("/history", methods=["GET"])
def history():
    cursor.execute("SELECT role, content FROM messages ORDER BY id DESC LIMIT 50")
    history = [{"role": role, "content": content} for role, content in reversed(cursor.fetchall())]
    return jsonify({"history": history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False, ssl_context=('cert.pem','key.pem'))
