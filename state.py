# Conversation history + task context (boilerplate
# state.py
# Manages conversation history and task context

class State:
    def __init__(self):
        self.conversation_history = []
        self.last_script_run = None
        self.last_output_path = None
        self.mobile_passcode = None

    def add_message(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def update_last_run(self, script_name: str, output_path: str):
        """Track the last script that was run and its output."""
        self.last_script_run = script_name
        self.last_output_path = output_path

    def get_history(self) -> list:
        """Return full conversation history for API calls."""
        return self.conversation_history

    def clear(self):
        """Reset state — useful for starting a fresh task."""
        self.conversation_history = []
        self.last_script_run = None
        self.last_output_path = None