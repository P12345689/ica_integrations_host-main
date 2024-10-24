# -*- coding: utf-8 -*-
"""
GitHub integration tool for performing various GitHub operations.

This module provides tools that wrap the functionality from the main github_router.
"""

import json
from typing import Dict, Optional
from langchain.agents import tool
# Import the github_operation function from the main router
from app.routes.github.github_router import github_operation


def clean_json_string(json_string):
    # Remove the starting ```json and ending ```
    cleaned_string = json_string.replace("```json", "").replace("```", "")

    # Find the index of the last closing brace
    last_brace_index = cleaned_string.rfind('}')
    
    # Remove any text after it
    if last_brace_index != -1:
        cleaned_string = cleaned_string[:last_brace_index + 1]

    # Remove the first character if it's a single quote
    if cleaned_string.startswith("'"):
        cleaned_string = cleaned_string[1:]

    # Strip any leading/trailing whitespace or newlines
    return cleaned_string.strip()

@tool
# def github_action(repo: str, action: str, params: Dict, token: Optional[str] = None) -> str:
def github_action(input_json: str) -> str:
    """
    Tool for performing various GitHub operations.

    Args:
        repo (str): Repository name (e.g., 'owner/repo').
        action (str): Action to perform (e.g., 'list_issues', 'create_pr').
        params (Dict): Additional parameters for the action.
        token (Optional[str]): GitHub access token (optional).

    Returns:
        str: Result of the GitHub operation.

    Example:
        >>> result = github_action("octocat/Hello-World", "list_issues", {})
        >>> assert "issues" in result.lower()
    """
    input_json = input_json.strip()

    try:
        params = json.loads(clean_json_string(input_json))
        print(f"Santana: Params: {params}")
    except json.JSONDecodeError:
        return "Error: Invalid JSON input. Please provide a valid JSON string."

    token = params.get("token")
    repo = params.get("repo")
    action = params.get("action")
    params = params.get("params")

    return github_operation(token, repo, action, params)


@tool
def get_github_info() -> str:
    """
    Tool for getting information about the GitHub integration.

    Returns:
        str: Information about the GitHub integration.

    Example:
        >>> info = get_github_info()
        >>> assert "GitHub" in info
        >>> assert "repositories" in info
    """
    return (
        "The GitHub integration provides functionality to interact with GitHub repositories, "
        "including both public and Enterprise private repos. It can perform various operations "
        "such as listing and creating issues, pull requests, releases, and retrieving file contents."
    )


@tool
def github_action_helper(action: str) -> str:
    """
    Tool for providing information about different GitHub actions and their required parameters.

    Args:
        action (str): The GitHub action (e.g., "create_issue", "list_prs").

    Returns:
        str: Information about the specified GitHub action and its required parameters.

    Example:
        >>> result = github_action_helper("create_issue")
        >>> assert "title" in result and "body" in result
    """
    actions = {
        "list_issues": "Lists all issues in the repository. No additional parameters required.",
        "create_issue": "Creates a new issue. Required params: title (str), body (str).",
        "list_prs": "Lists all pull requests in the repository. No additional parameters required.",
        "create_pr": "Creates a new pull request. Required params: title (str), body (str), head (str), base (str, default='main').",
        "list_releases": "Lists all releases in the repository. No additional parameters required.",
        "create_release": "Creates a new release. Required params: tag (str), title (str), body (str).",
        "get_file": "Retrieves the contents of a file. Required params: path (str).",
    }
    return actions.get(action, f"Unknown action: {action}")
