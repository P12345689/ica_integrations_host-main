# -*- coding: utf-8 -*-
"""
WebEx integration tool for retrieving and summarizing call transcripts.

This module provides tools that wrap the functionality from the main webex_router.
"""

from typing import Dict

from langchain.agents import tool

# Import the webex_operation function from the main router
from app.routes.webex.webex_router import webex_operation


@tool
def webex_action(action: str, params: Dict, webex_token: str) -> str:
    """
    Tool for performing various WebEx operations.

    Args:
        action (str): Action to perform (e.g., 'list_transcripts', 'get_transcript').
        params (Dict): Additional parameters for the action.
        webex_token (str): WebEx access token.

    Returns:
        str: Result of the WebEx operation.

    Example:
        >>> result = webex_action("list_transcripts", {}, "your_webex_token_here")
        >>> assert "transcripts" in result.lower()
    """
    return webex_operation(webex_token, action, params)


@tool
def get_webex_info() -> str:
    """
    Tool for getting information about the WebEx integration.

    Returns:
        str: Information about the WebEx integration.

    Example:
        >>> info = get_webex_info()
        >>> assert "WebEx" in info
        >>> assert "transcripts" in info
    """
    return (
        "The WebEx integration provides functionality to interact with WebEx transcripts, "
        "including listing available transcripts, retrieving specific transcripts, "
        "and summarizing transcript content using an LLM."
    )


@tool
def webex_action_helper(action: str) -> str:
    """
    Tool for providing information about different WebEx actions and their required parameters.

    Args:
        action (str): The WebEx action (e.g., "list_transcripts", "get_transcript").

    Returns:
        str: Information about the specified WebEx action and its required parameters.

    Example:
        >>> result = webex_action_helper("get_transcript")
        >>> assert "transcript_id" in result
    """
    actions = {
        "list_transcripts": "Lists all available transcripts. No additional parameters required.",
        "get_transcript": "Retrieves a specific transcript. Required params: transcript_id (str).",
    }
    return actions.get(action, f"Unknown action: {action}")


@tool
def summarize_transcript(transcript: str) -> str:
    """
    Tool for summarizing a WebEx transcript using an LLM.

    Args:
        transcript (str): The full transcript content.

    Returns:
        str: A summary of the transcript.

    Example:
        >>> summary = summarize_transcript("This is a sample transcript of a meeting about project deadlines.")
        >>> assert "summary" in summary.lower()
    """
    # This is a placeholder. In a real implementation, you would call your LLM here.
    return f"This is a summary of the transcript: {transcript[:100]}..."
