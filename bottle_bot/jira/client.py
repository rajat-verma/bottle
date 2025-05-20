"""Simple Jira API wrapper (stub)."""
from typing import Dict


def create_ticket(project_key: str, title: str, summary: str, pr_url: str) -> Dict[str, str]:
    """Create a Jira ticket. This is a stub returning a fake ticket."""
    key = f"{project_key}-123"
    url = f"https://jira.example.com/browse/{key}"
    return {"key": key, "url": url}
