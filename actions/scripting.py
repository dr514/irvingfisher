# Generate + execute scripts (project-specific)
# actions/scripting.py
# Handles script execution on the local desktop

import subprocess
import os
from pathlib import Path

# Base path to scripts folder
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"

# Whitelist of allowed scripts and their expected arguments
WHITELIST = {
    "insider_buying.py": ["tickers", "days"],
    # add more scripts here as you build them
    # "another_script.py": ["arg1", "arg2"],
}


def run_script(script_name: str, args: dict) -> dict:
    """
    Runs a whitelisted script with the given arguments.
    Returns a dict with success status, output file path or error message.
    """

    # Check whitelist
    if script_name not in WHITELIST:
        return {
            "success": False,
            "error": f"{script_name} is not on the approved whitelist."
        }

    # Check all required args are present
    expected_args = WHITELIST[script_name]
    missing = [arg for arg in expected_args if arg not in args]
    if missing:
        return {
            "success": False,
            "error": f"Missing required arguments: {', '.join(missing)}"
        }

    # Build the command
    script_path = SCRIPTS_DIR / script_name
    command = ["python", str(script_path)]
    for key, value in args.items():
        command += [f"--{key}", str(value)]

    # Execute
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=300  # 5 min timeout — adjust for long FactSet refreshes
        )

        if result.returncode != 0:
            return {
                "success": False,
                "error": result.stderr.strip() or "Script exited with a non-zero return code."
            }

        # Expect the script to print the output file path on the last line of stdout
        lines = [line.strip() for line in result.stdout.splitlines() if line.strip()]
        output_path = lines[-1] if lines else ""
        if not os.path.exists(output_path):
            return {
                "success": False,
                "error": f"Script ran but output file not found at: {output_path}"
            }

        return {
            "success": True,
            "output_path": output_path
        }

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Script timed out after 5 minutes."
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def list_scripts() -> dict:
    """
    Returns the list of available whitelisted scripts.
    """
    return {
        "success": True,
        "scripts": list(WHITELIST.keys())
    }