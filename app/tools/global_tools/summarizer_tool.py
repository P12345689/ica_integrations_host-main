# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Summarization tool for use with LangChain agents.

This module provides a tool that uses the summarization functionality from the main router.
It can be used within LangChain agents to summarize text with configurable settings.

Example:
    >>> from langchain.agents import Tool
    >>> from langchain.agents import initialize_agent
    >>> from langchain.llms import OpenAI
    >>>
    >>> llm = OpenAI(temperature=0)
    >>> tools = [Tool(
    ...     name="Summarizer",
    ...     func=summarize_text_tool,
    ...     description="A tool that summarizes text. Accepts text and optional parameters for customization."
    ... )]
    >>> agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    >>> agent.run("Summarize this text: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit...' Use a casual style and bullet points.")
"""

import asyncio
from typing import Optional

from fastapi import FastAPI, Request
from langchain.agents import tool

from app.routes.summarizer.summarizer_router import SummarizeInputModel, add_custom_routes

# Create a global variable to store the summarize_text function
global_summarize_text = None


def initialize_summarize_text() -> None:
    """Initialize the global summarize_text function."""
    global global_summarize_text
    if global_summarize_text is None:
        app = FastAPI()
        add_custom_routes(app)
        for route in app.routes:
            if route.path == "/experience/summarize/summarize_text/invoke":
                global_summarize_text = route.endpoint
                break
        if global_summarize_text is None:
            raise ValueError("Could not find summarize_text function in routes")


# Initialize the global function
initialize_summarize_text()


@tool
def summarize_text_tool(
    text: str,
    style: Optional[str] = "business",
    output_format: Optional[str] = "plain",
    summary_type: Optional[str] = "bullets",
    summary_length: Optional[str] = "medium",
    additional_instruction: Optional[str] = "",
) -> str:
    """
    Tool for summarizing text using configurable LangChain methods.

    Args:
        text (str): The long text to be summarized.
        style (str, optional): Style of the summary ("business" or "casual"). Defaults to "business".
        output_format (str, optional): Output format of the summary ("plain" or "markdown"). Defaults to "plain".
        summary_type (str, optional): Type of summary output ("bullets" or "paragraphs"). Defaults to "bullets".
        summary_length (str, optional): Length of the summary ("short", "medium", or "long"). Defaults to "medium".
        additional_instruction (str, optional): Additional instruction for the summarizer. Defaults to "".

    Returns:
        str: The summarized text.

    Raises:
        ValueError: If the input text is empty or invalid.

    Example:
        >>> text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit..."
        >>> summary = summarize_text_tool(text, style="casual", summary_type="paragraphs", summary_length="short")
        >>> print(summary)
        A concise summary of the given text...
    """
    if not text or not isinstance(text, str):
        return "Error: Invalid input. Please provide a non-empty string to summarize."

    try:
        # Ensure the global function is initialized
        if global_summarize_text is None:
            initialize_summarize_text()

        # Create a SummarizeInputModel instance with the input data and default values
        input_model = SummarizeInputModel(
            text=text,
            max_tokens=1024,
            summary_type=summary_type,
            summary_length=summary_length,
            output_format=output_format,
            style=style,
            additional_instruction=additional_instruction,
            chain_type="map_reduce",
            context_length=8192,
            temperature=0.7,
            chunk_size=6000,
            chunk_overlap=200,
        )

        # Create a mock Request object
        mock_request = Request(scope={"type": "http"})
        mock_request._json = input_model.dict()

        # Call the summarize_text function from the router
        result = asyncio.run(global_summarize_text(mock_request))

        # Extract the summary from the result
        if result.response and result.response[0].message:
            return result.response[0].message
        else:
            return "Failed to generate summary."

    except Exception as e:
        return f"An error occurred while summarizing the text: {str(e)}"
