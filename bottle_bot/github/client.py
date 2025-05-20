"""Placeholder GitHub API client."""

from typing import Dict, Any


def get_pr(pr_number: int) -> Dict[str, Any]:
    """Stub returning PR info."""
    # In a real implementation, this would call GitHub.
    return {
        "number": pr_number,
        "title": "Example PR",
        "body": "This is an example pull request body.",
        "html_url": f"https://github.com/example/repo/pull/{pr_number}",
    }


def post_comment(pr_number: int, text: str) -> None:
    """Stub posting a comment to a PR."""
    print(f"Would post comment to PR {pr_number}: {text}")
