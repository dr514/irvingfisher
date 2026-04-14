# server.py
# Web frontend and API for IrvingFisher
# Run this on your always-on Windows machine alongside ngrok

import os
from flask import Flask, request, jsonify, render_template_string, session
from dotenv import load_dotenv

import agent

load_dotenv()

app = Flask(__name__)
# Secret key for session/cookies
app.secret_key = os.getenv("FLASK_SECRET_KEY", "super-secret-fish-key")

API_TOKEN = os.getenv("JIMMY_API_TOKEN")


def authorize_cli(req) -> bool:
    """Check request carries the correct API token from CLI."""
    token = req.headers.get("X-API-Token")
    return token == API_TOKEN


# -----------------------------------------------------
# HTML Web Interface (Mobile View)
# -----------------------------------------------------

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
    <title>IrvingFisher AI</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial; background: #0f172a; color: #f8fafc; margin: 0; padding: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: #1e293b; padding: 15px; text-align: center; border-bottom: 1px solid #334155; font-weight: bold; }
        .chat-container { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .msg { max-width: 85%; padding: 10px 15px; border-radius: 15px; line-height: 1.4; word-wrap: break-word; white-space: pre-wrap; }
        .user { align-self: flex-end; background: #3b82f6; color: white; border-bottom-right-radius: 2px; }
        .assistant { align-self: flex-start; background: #334155; color: white; border-bottom-left-radius: 2px; }
        .input-area { padding: 10px; background: #1e293b; display: flex; gap: 10px; }
        input[type="text"] { flex: 1; padding: 12px; border-radius: 20px; border: 1px solid #475569; background: #0f172a; color: white; outline: none; }
        button { padding: 10px 20px; border-radius: 20px; border: none; background: #3b82f6; color: white; font-weight: bold; cursor: pointer; }
        .login-box { margin: auto; padding: 20px; background: #1e293b; border-radius: 10px; text-align: center; width: 80%; max-width: 300px;}
        .login-box input { width: 100%; box-sizing: border-box; margin: 10px 0; }
    </style>
</head>
<body>
    <div class="header">IrvingFisher Agent</div>

    {% if not logged_in %}
    <!-- Login Screen -->
    <div class="login-box">
        <h3>Enter Passcode</h3>
        <p>Ask Fish via Powershell for the dynamic mobile passcode.</p>
        <form method="POST" action="/mobile_login">
            <input type="text" name="passcode" placeholder="Passcode" required autocomplete="off">
            <button type="submit">Unlock</button>
        </form>
    </div>
    {% else %}
    <!-- Chat Screen -->
    <div class="chat-container" id="chat">
        {% for msg in history %}
            <div class="msg {{ msg.role }}">{{ msg.text }}</div>
        {% endfor %}
    </div>
    <form class="input-area" onsubmit="sendMessage(event)">
        <input type="text" id="userInput" placeholder="Message Fish..." autocomplete="off">
        <button type="submit">Send</button>
    </form>
    <script>
        const chat = document.getElementById('chat');
        chat.scrollTop = chat.scrollHeight;

        async function sendMessage(e) {
            e.preventDefault();
            const input = document.getElementById('userInput');
            const term = input.value.trim();
            if(!term) return;

            // Add user message to UI immediately
            const userDiv = document.createElement('div');
            userDiv.className = 'msg user';
            userDiv.innerText = term;
            chat.appendChild(userDiv);
            input.value = '';
            chat.scrollTop = chat.scrollHeight;

            // Call API
            const res = await fetch('/mobile_chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: term})
            });
            const data = await res.json();

            // Add assistant response to UI
            const botDiv = document.createElement('div');
            botDiv.className = 'msg assistant';
            botDiv.innerText = data.response;
            chat.appendChild(botDiv);
            chat.scrollTop = chat.scrollHeight;
        }
    </script>
    {% endif %}
</body>
</html>
"""

def get_clean_history():
    """Extracts plain text from the Anthropic message format for the UI."""
    history_clean = []
    for msg in agent.global_state.get_history():
        text = ""
        if isinstance(msg["content"], str):
            text = msg["content"]
        elif isinstance(msg["content"], list):
            for block in msg["content"]:
                if isinstance(block, dict) and block.get("type") == "text":
                    text += block["text"] + "\n"
        
        # Don't show system tool requests to user UI directly unless they contain text
        if text.strip():
            history_clean.append({"role": msg["role"], "text": text.strip()})
    return history_clean


@app.route("/", methods=["GET"])
def index():
    logged_in = session.get("authenticated", False)
    history = get_clean_history() if logged_in else []
    return render_template_string(HTML_TEMPLATE, logged_in=logged_in, history=history)


@app.route("/mobile_login", methods=["POST"])
def mobile_login():
    passcode = request.form.get("passcode", "").strip().lower()
    true_passcode = agent.global_state.mobile_passcode
    
    if true_passcode and passcode == true_passcode.lower():
        session["authenticated"] = True
        # Clear it so it can't be used again by someone else?
        # agent.global_state.mobile_passcode = None # Optional: one-time use
        return render_template_string("<script>window.location.href='/';</script>")
    else:
        return "<script>alert('Invalid passcode'); window.location.href='/';</script>"


@app.route("/mobile_chat", methods=["POST"])
def mobile_chat():
    if not session.get("authenticated", False):
        return jsonify({"error": "Not authenticated"}), 401
    
    msg = request.json.get("message", "")
    reply = agent.send_message(msg)
    return jsonify({"response": reply})


# -----------------------------------------------------
# API Interface (For Powershell CLI main.py)
# -----------------------------------------------------

@app.route("/chat", methods=["POST"])
def cli_chat():
    if not authorize_cli(request):
        return jsonify({"error": "Unauthorized"}), 401
        
    msg = request.json.get("message")
    if not msg:
        return jsonify({"error": "Message required"}), 400
        
    reply = agent.send_message(msg)
    return jsonify({"response": reply})


if __name__ == "__main__":
    print("[SYSTEM] Starting IrvingFisher Server...")
    # debug=False since standard debugger breaks Anthropic loops occasionally with threads
    app.run(host="0.0.0.0", port=5000, debug=False)