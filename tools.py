# Tool definitions for API (project-specific)
# tools.py
# Tool definitions for the Anthropic API (function calling format)

TOOLS = [
    {
        "name": "run_script",
        "description": (
            "Runs a whitelisted Python script on the local desktop with the given arguments. "
            "Always confirm with the user before calling this tool. "
            "Returns the output file path on success, or an error message on failure."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "script_name": {
                    "type": "string",
                    "description": "The script filename to run, e.g. 'insider_buying.py'. Must be on the whitelist in server.py."
                },
                "args": {
                    "type": "object",
                    "description": (
                        "Key-value pairs of command line arguments to pass to the script. "
                        "e.g. {\"tickers\": \"AAPL-US MSFT-US\", \"days\": \"90\"}"
                    )
                }
            },
            "required": ["script_name", "args"]
        }
    },
    {
        "name": "send_email",
        "description": (
            "Sends an email with a file attachment via Gmail. "
            "Call this after run_script completes successfully."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {
                    "type": "string",
                    "description": "Recipient email address."
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line, e.g. 'Insider Buying Output — April 8 2026'"
                },
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to the output file to attach, returned by run_script."
                }
            },
            "required": ["to", "subject", "file_path"]
        }
    },
    {
        "name": "list_scripts",
        "description": (
            "Returns the list of available whitelisted scripts Jimmy can run. "
            "Use this when the user is unsure of a script name or wants to know what's available."
        ),
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "name": "set_mobile_passcode",
        "description": (
            "Generates and sets a new dynamic passcode for the mobile web interface. "
            "Call this when the user says they are switching to their phone or asks to set a passcode. "
            "Pass a single, simple, easy-to-type English word (like 'hello', 'park', 'chicago')."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "passcode": {
                    "type": "string",
                    "description": "A simple word to use as the temporary mobile passcode."
                }
            },
            "required": ["passcode"]
        }
    }
]