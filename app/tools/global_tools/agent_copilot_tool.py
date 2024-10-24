# -*- coding: utf-8 -*-
"""
Agent Copilot tool for use with LangChain.

This module provides a tool that can be used to interact with the Agent Copilot integration.
"""

from typing import Optional

import requests
from langchain.agents import tool


@tool
def agent_copilot_tool(assistant: str, message: str, api_key: Optional[str] = None) -> str:
    """
    Tool for interacting with the Agent Copilot integration.

    Args:
        assistant (str): The name of the assistant to invoke (e.g., "appmod" or "migration")
        message (str): The message to send to the assistant
        api_key (str, optional): The API key for the integration. If not provided, it should be set in the environment.

    Returns:
        str: The response from the assistant

    Raises:
        Exception: If there's an error in the API call
    """
    url = f"http://localhost:8080/agent_copilot/{assistant}/invoke"
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": api_key or "dev-only-token",
    }
    payload = {"message": message}

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result["response"][0]["message"]
    except requests.RequestException as e:
        raise Exception(f"Error calling Agent Copilot API: {str(e)}")


# Example usage
if __name__ == "__main__":
    response = agent_copilot_tool("appmod", "Explain the benefits of containerization")
    print(response)
