from typing import Callable, Dict, Any, Tuple, Optional

from .commands import cmr, help

CommandFunc = Callable[[Dict[str, Any], list], Any]

COMMANDS: Dict[str, CommandFunc] = {
    "CMR": cmr.run,
    "help": help.run,
}

def parse_command(text: str) -> Optional[Tuple[str, list]]:
    """Parse a command from a comment body."""
    if not text.startswith("@bottle"):
        return None
    parts = text.strip().split()
    if len(parts) < 2:
        return None
    name = parts[1]
    args = parts[2:]
    return name, args

def handle_comment(body: str, pr_info: Dict[str, Any]) -> Any:
    """Handle a PR comment, dispatching commands if found."""
    parsed = parse_command(body)
    if not parsed:
        return None
    name, args = parsed
    cmd = COMMANDS.get(name)
    if not cmd:
        raise ValueError(f"Unknown command: {name}")
    return cmd(pr_info, args)
