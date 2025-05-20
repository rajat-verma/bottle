"""CMR command for creating change request tickets in Jira."""
from typing import Dict, Any

from ..jira import client as jira_client
from ..llm import compressor


def run(pr_info: Dict[str, Any], args: list) -> Dict[str, Any]:
    if not args:
        raise ValueError("Project key required")
    project_key = args[0]

    title = pr_info.get("title", "")
    description = pr_info.get("body", "")
    pr_url = pr_info.get("html_url", "")

    summary = compressor.compress(description)
    return jira_client.create_ticket(project_key, title, summary, pr_url)
