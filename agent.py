# agent.py
# Core Anthropic Engine and State Manager

import os
import json
import anthropic
from dotenv import load_dotenv

from state import State
from prompts import get_system_prompt
from tools import TOOLS
from actions import run_script, list_scripts, send_email

load_dotenv()

# Global State Instance - shared memory!
global_state = State()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
# Ensure we have a client even if key is missing (it'll error on call, which is fine)
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None


def set_mobile_passcode(passcode: str) -> dict:
    global_state.mobile_passcode = passcode
    return {"success": True, "message": f"Mobile passcode set to: {passcode}"}


def execute_tool(tool_name: str, tool_args: dict) -> dict:
    if tool_name == "run_script":
        return run_script(tool_args["script_name"], tool_args["args"])
    elif tool_name == "list_scripts":
        return list_scripts()
    elif tool_name == "send_email":
        return send_email(tool_args["to"], tool_args["subject"], tool_args["file_path"])
    elif tool_name == "set_mobile_passcode":
        return set_mobile_passcode(tool_args["passcode"])
    
    return {"error": f"Unknown tool: {tool_name}"}


def send_message(user_msg: str) -> str:
    """Sends a message to Claude, handles any tool calls recursively, returns text response."""
    if not client:
        return "Error: ANTHROPIC_API_KEY is not set in .env"

    global_state.add_message("user", user_msg)
    
    while True:
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=4096,
                system=get_system_prompt(),
                messages=global_state.get_history(),
                tools=TOOLS
            )
        except Exception as e:
            # Handle API errors gracefully
            error_msg = f"API Error: {str(e)}"
            global_state.add_message("assistant", error_msg)
            return error_msg
        
        # Add assistant's raw message format directly to state for proper tool flow
        # Anthropic SDK requires blocks as dicts for following appeals
        # We manually append a formatted dict to bypass add_message's string assumption
        assistant_content = []
        text_reply = ""
        
        for block in response.content:
            if block.type == "text":
                assistant_content.append({"type": "text", "text": block.text})
                text_reply += block.text + "\n"
            elif block.type == "tool_use":
                assistant_content.append({
                    "type": "tool_use",
                    "id": block.id,
                    "name": block.name,
                    "input": block.input
                })
                
        global_state.conversation_history.append({
            "role": "assistant",
            "content": assistant_content
        })

        if response.stop_reason == "tool_use":
            # We have tools to execute!
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": json.dumps(result)
                    })
            
            # Feed tool results back
            global_state.conversation_history.append({
                "role": "user",
                "content": tool_results
            })
            continue # Loop back to Claude with the tool result
        
        else:
            # Normal completion
            return text_reply.strip()
