# -*- coding: utf-8 -*-
""""
Author: Gytis Oziunas
Description: This module provides a tool for generating PlantUML diagrams from text input.

This module provides a tool that can be used with LangChain agents to generate PlantUML diagrams from text input.
It directly calls the plantuml_tool_generate_uml function from the router.

Example:
    >>> from langchain.agents import Tool
    >>> from langchain.agents import initialize_agent
    >>> from langchain.llms import OpenAI
    >>>
    >>> llm = OpenAI(temperature=0)
    >>> tools = [Tool(
    ...     name="PlantUML",
    ...     func=plantuml_tool_generate_uml,
    ...     description="A tool that generates PlantUML diagrams from text input."
    ... )]
    >>> agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    >>> agent.run("Create a UML diagram with the following content: 'Alice -> Bob: Hello'")
"""
import asyncio
import re
import logging
from typing import Optional
from fastapi import FastAPI, Request
from langchain.agents import tool
from app.routes.plantuml.plantuml_router import add_custom_routes, OutputModel, clean_description
from pydantic import BaseModel

# Set up logging
log = logging.getLogger(__name__)

# Create a global variable to store the plantuml function
global_plantuml = None

def initialize_plantuml() -> None:
    """Initialize the global plantuml function."""
    global global_plantuml
    if global_plantuml is None:
        app = FastAPI()
        add_custom_routes(app)
        for route in app.routes:
             if route.path in ["/plantuml/invoke", "/system/plantuml/transformers/syntax_to_image/invoke", "/experience/plantuml/transformers/syntax_to_image/invoke"]:
                global_plantuml = route.endpoint
                break
        if global_plantuml is None:
            raise ValueError("Could not find plantuml function in routes")

# Initialize the global function
initialize_plantuml()

class MockRequest(BaseModel):
    json_data: dict

    async def json(self):
        return self.json_data

@tool
def plantuml_tool_generate_uml(description: str) -> str:
    """
    Tool for generating PlantUML diagrams from text input.
    Args:
        description (str): The input text describing the PlantUML diagram in PlantUML syntax.
    Returns:
        str: A string containing the image URL and formatted text response.
    """
    if not description or not isinstance(description, str):
        return "Error: The description must be a non-empty string."
    try:
        if global_plantuml is None:
            initialize_plantuml()

        # Clean the description
        clean_desc = clean_description(description)

        # Create a mock Request object with the cleaned description
        mock_request = MockRequest(json_data={"description": clean_desc})
        
        # Call the global_plantuml function with the mock request
        response = asyncio.run(global_plantuml(mock_request))

        # Parse the response into our Pydantic model
        parsed_response = OutputModel(**response)

        # Extract the URL from the first ResponseMessageModel
        url = parsed_response.response[0].message
        
        # Extract the PlantUML code from the second ResponseMessageModel
        plantuml_code = parsed_response.response[1].message.split('\n\n', 1)[1]
        
        # Format the response
        formatted_response = f"UML Diagram URL: {url}\n\nFormatted PlantUML code:\n```\n{plantuml_code}\n```"
        
        log.info(f"Formatted response: {formatted_response}") 

        return formatted_response
    

    except Exception as e:
        error_message = f"An error occurred while generating the PlantUML diagram: {str(e)}"
        log.error(error_message)
        return error_message