# Loads + assembles .md files (boilerplate)
# prompts.py
# Loads and assembles system prompts from .md files

from pathlib import Path

PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"


def load_prompt(filename: str) -> str:
    """Load a single .md prompt file by filename."""
    path = PROMPTS_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def get_system_prompt() -> str:
    """Assembles the full system prompt for Fish."""
    return "\n\n".join([
        load_prompt("system.md"),
        load_prompt("dcf_methodology.md"),
        load_prompt("industry_knowledge.md"),
        load_prompt("factset_excel.md"),
    ])
