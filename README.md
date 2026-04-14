# JimmySims Agent

An AI agent system with dual interfaces: a PowerShell CLI client and a mobile-accessible Flask web UI.

## Features

- Anthropic Claude tool-calling agent loop
- Flask server with web interface (mobile-friendly)
- Dynamic passcode authentication for remote access
- Email sending via Gmail
- Script execution from agent context
- Conversation history management

## Structure

```
JimmySims/
├── agent.py          # Core agent loop (Anthropic tool-calling)
├── state.py          # Conversation history management
├── tools.py          # Tool definitions
├── prompts.py        # System prompt management
├── prompts/          # Markdown prompt files
├── main.py           # CLI entry point
├── server.py         # Flask web server entry point
├── actions/          # Action handlers (email, scripting)
├── tests/            # Unit tests
├── artifacts/        # Agent-generated artifacts
├── logs/             # Runtime logs
└── scripts/          # Executable scripts
```

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# Fill in your keys in .env
```

## Usage

**CLI mode:**
```bash
python main.py
```

**Web server mode:**
```bash
python server.py
```
