# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Document Builder Tool - Generates PPTX and DOCX documents from input text.

This module provides a tool that can be used with LangChain agents to generate
PowerPoint presentations (PPTX) and Word documents (DOCX) from plain text input.
It directly calls the docbuilder function from the router.

Example:
    >>> from langchain.agents import Tool
    >>> from langchain.agents import initialize_agent
    >>> from langchain.llms import OpenAI
    >>>
    >>> llm = OpenAI(temperature=0)
    >>> tools = [Tool(
    ...     name="DocBuilder",
    ...     func=docbuilder_tool_markdown_to_pptx_docx,
    ...     description="A tool that generates PPTX and DOCX documents from plain text input."
    ... )]
    >>> agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    >>> agent.run("Create a presentation about OpenShift with the following content: 'OpenShift is a Kubernetes platform...'")
"""

import asyncio
from typing import Optional

from fastapi import FastAPI, Request
from langchain.agents import tool

from app.routes.docbuilder.docbuilder_router import InputModel, add_custom_routes

# Create a global variable to store the docbuilder function
global_docbuilder = None


def initialize_docbuilder() -> None:
    """Initialize the global docbuilder function."""
    global global_docbuilder
    if global_docbuilder is None:
        app = FastAPI()
        add_custom_routes(app)
        for route in app.routes:
            if route.path == "/experience/docbuilder/generate_docs/invoke":
                global_docbuilder = route.endpoint
                break
        if global_docbuilder is None:
            raise ValueError("Could not find docbuilder function in routes")


# Initialize the global function
initialize_docbuilder()


@tool
def docbuilder_tool_markdown_to_pptx_docx(input_text: str, template_type: Optional[str] = "IBM Consulting Green") -> str:
    """
    Tool for generating PPTX and DOCX documents from input text.

    Args:
        input_text (str): The text content to be converted into documents.
        template_type (str, optional): The type of template to use. Defaults to "IBM Consulting Green".

    Returns:
        str: A message containing URLs to the generated PPTX and DOCX documents.

    Raises:
        ValueError: If the input text is empty or invalid.

    Example:
        >>> text = "OpenShift is a Kubernetes platform..."
        >>> result = docbuilder_tool_markdown_to_pptx_docx(text)
        >>> print(result)
        URLs to the generated documents: PPTX: http://..., DOCX: http://...
    """
    if not input_text or not isinstance(input_text, str):
        return "Error: Invalid input. Please provide a non-empty string to convert into documents."

    try:
        # Ensure the global function is initialized
        if global_docbuilder is None:
            initialize_docbuilder()

        # Create an InputModel instance with the input data
        input_model = InputModel(input_text=input_text, template_type=template_type)

        # Create a mock Request object
        mock_request = Request(scope={"type": "http"})
        mock_request._json = input_model.dict()

        # Call the docbuilder function from the router
        result = asyncio.run(global_docbuilder(mock_request))

        # Extract the document URLs from the result
        if result.response and result.response[0].message:
            return result.response[0].message
        else:
            return "Failed to generate documents."

    except Exception as e:
        return f"An error occurred while generating the documents: {str(e)}"
