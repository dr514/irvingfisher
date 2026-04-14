
# actions/__init__.py
# Registers all actions for easy import

from .scripting import run_script, list_scripts
from .email import send_email

__all__ = ["run_script", "list_scripts", "send_email"]