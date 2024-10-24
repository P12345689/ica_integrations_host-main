# -*- coding: utf-8 -*-
"""
Jira tool for creating issues and retrieving information.

This module provides tools that use the Jira functionality from the main router.
"""

from typing import Dict

from langchain.agents import tool

# Import the functions from the main router
from ..jira_router import create_jira_issue, get_jira_issue


@tool
def create_jira_issue_tool(project_key: str, summary: str, description: str, issue_type: str = "Task") -> str:
    """
    Tool for creating a new Jira issue.

    Args:
        project_key (str): The project key where the issue will be created.
        summary (str): The summary of the issue.
        description (str): The description of the issue.
        issue_type (str, optional): The type of the issue. Defaults to "Task".

    Returns:
        str: The key of the created issue.

    >>> create_jira_issue_tool("PROJ", "Test Issue", "This is a test issue", "Bug")
    'PROJ-123'
    """
    issue_data = {
        "project_key": project_key,
        "summary": summary,
        "description": description,
        "issue_type": issue_type,
    }
    return create_jira_issue(issue_data)


@tool
def get_jira_issue_tool(issue_key: str) -> Dict[str, str]:
    """
    Tool for retrieving information about a Jira issue.

    Args:
        issue_key (str): The key of the issue to retrieve.

    Returns:
        Dict[str, str]: A dictionary containing issue information.

    >>> get_jira_issue_tool("PROJ-123")
    {'key': 'PROJ-123', 'summary': 'Test Issue', 'description': 'This is a test issue', 'status': 'Open'}
    """
    return get_jira_issue(issue_key)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
