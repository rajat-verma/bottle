"""Lightweight GitHub API client."""

from typing import Dict, Any
import os

import requests


API_URL = os.getenv("GITHUB_API_URL", "https://api.github.com")
REPO = os.getenv("GITHUB_REPO")
TOKEN = os.getenv("GITHUB_TOKEN")

session = requests.Session()
session.headers["Accept"] = "application/vnd.github+json"
if TOKEN:
    session.headers["Authorization"] = f"token {TOKEN}"


def _require_repo() -> str:
    if not REPO:
        raise ValueError("GITHUB_REPO environment variable not set")
    return REPO


def get_pr(pr_number: int) -> Dict[str, Any]:
    """Return information for a pull request."""
    repo = _require_repo()
    url = f"{API_URL}/repos/{repo}/pulls/{pr_number}"
    response = session.get(url)
    response.raise_for_status()
    return response.json()


def post_comment(pr_number: int, text: str) -> None:
    """Post a comment to a pull request."""
    repo = _require_repo()
    url = f"{API_URL}/repos/{repo}/issues/{pr_number}/comments"
    response = session.post(url, json={"body": text})
    response.raise_for_status()
