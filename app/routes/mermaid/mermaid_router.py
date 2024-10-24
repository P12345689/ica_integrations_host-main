# -*- coding: utf-8 -*-
"""
Author: Chris Hay, Mihai Criveti
Description: Mermaid Integration for text-to-image conversion and syntax generation.

The main functionality includes:
- Converting Mermaid text to syntax using LangChain and ChatConsultingAssistants.
- Generating Mermaid images from syntax using the Mermaid server.
- Downloading the generated image and serving it locally.
- Handling errors and providing informative responses to the user.
- Using Jinja2 templates for formatting the response.

The module uses FastAPI for handling HTTP requests, Pydantic for input validation and output structuring,
and Jinja2 for templating the responses.

Example usage:
    # Make a POST request to the /experience/mermaid/transformers/text_to_image/invoke endpoint with the following JSON payload:
    {
        "query": "A simple mindmap",
        "chart_type": "mindmap",
        "style": "default",
        "direction": "TB"
    }
"""

import logging
import os
from uuid import uuid4

import httpx
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_consultingassistants import ChatConsultingAssistants
from pydantic import BaseModel

from app.tools.global_tools.mermaid_tool import syntax_to_image

log = logging.getLogger(__name__)

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/mermaid/templates"))


class MermaidRequest(BaseModel):
    query: str
    chart_type: str
    style: str
    direction: str


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str
    response: list[ResponseMessageModel]
    invocationId: str  # noqa: N815


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/experience/mermaid/transformers/text_to_image/invoke")
    async def mermaid_text_to_image(request: Request):
        # Get the request data
        data = await request.json()

        # Validate input data using Pydantic model
        mermaid_request = MermaidRequest(**data)

        try:
            # Convert the text to syntax
            mermaid_syntax = await convert_mermaid_text_to_syntax(mermaid_request)

            # Generate the Mermaid image URL from the syntax
            image_url = await generate_mermaid_image(mermaid_syntax)

            # Create an invocation ID
            invocation_id = str(uuid4())

            # Format the response using a Jinja2 template
            template = template_env.get_template("mermaid_response.jinja")
            formatted_response = template.render(url=image_url, syntax=mermaid_syntax)

            # Create the response
            response = [
                ResponseMessageModel(message=image_url, type="image"),
                ResponseMessageModel(message=formatted_response, type="text"),
            ]
            log.info(f"Formatted response: {formatted_response}")
            log.info(f"Final response: {response}")

            return {
                "status": "success",
                "response": response,
                "invocationId": invocation_id,
            }
        except ValueError as e:
            log.error(f"Error generating image: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except HTTPException as e:
            log.error(f"Error generating Mermaid image: {str(e.detail)}")
            raise e

    @app.post("/experience/mermaid_service/transformers/text_to_syntax/invoke")
    async def mermaid_text_to_syntax(request: Request):
        # Get the request data
        data = await request.json()

        # Validate input data using Pydantic model
        mermaid_request = MermaidRequest(**data)

        try:
            # Convert the text to syntax
            mermaid_syntax = await convert_mermaid_text_to_syntax(mermaid_request)

            # Create an invocation ID
            invocation_id = str(uuid4())

            # Create the response
            response = [ResponseMessageModel(message=mermaid_syntax, type="text")]
            log.info(f"Mermaid syntax: {mermaid_syntax}")
            log.info(f"Final response: {response}")

            return {
                "status": "success",
                "response": response,
                "invocationId": invocation_id,
            }
        except HTTPException as e:
            log.error(f"Error converting text to Mermaid syntax: {str(e.detail)}")
            raise e

    @app.post("/mermaid/invoke")
    @app.post("/system/mermaid_service/transformers/syntax_to_image/invoke")
    async def mermaid_syntax_to_image(request: Request):
        # Get the request data
        data = await request.json()

        # Get the Mermaid syntax from the request data
        mermaid_syntax = data["query"]

        try:
            # Generate the Mermaid image URL from the syntax
            image_url = await generate_mermaid_image(mermaid_syntax)

            # Create an invocation ID
            invocation_id = str(uuid4())

            # Format the response using a Jinja2 template
            template = template_env.get_template("mermaid_response.jinja")
            formatted_response = template.render(url=image_url, syntax=mermaid_syntax)

            # Create the response
            response = [
                ResponseMessageModel(message=image_url, type="image"),
                ResponseMessageModel(message=formatted_response, type="text"),
            ]
            log.info(f"Formatted response: {formatted_response}")
            log.info(f"Final response: {response}")

            return {
                "status": "success",
                "response": response,
                "invocationId": invocation_id,
            }
        except HTTPException as e:
            log.error(f"Error generating Mermaid image: {str(e.detail)}")
            invocation_id = str(uuid4())
            return {
                "status": "error",
                "response": [
                    ResponseMessageModel(
                        message="Could not generate image", type="text"
                    )
                ],
                "invocationId": invocation_id,
            }


async def convert_mermaid_text_to_syntax(mermaid_request: MermaidRequest) -> str:
    # Get the parameters from the request data
    query = mermaid_request.query
    chart_type = mermaid_request.chart_type
    style = mermaid_request.style
    direction = mermaid_request.direction
    max_tokens = 1000

    # Set the prompt template
    prompt_template = format_prompt(
        query="Draw a {chart_type} for the following {query}. Make it {style}. Set the direction to {direction}.",
        max_tokens=max_tokens,
    )

    if chart_type == "sequence diagram":
        prompt_template = format_prompt(
            query="Draw a {chart_type} for the following {query}. Do not include directions or notes",
            max_tokens=max_tokens,
        )

    # Set the model
    model = ChatConsultingAssistants(model="Llama3.1 70b Instruct")

    # Set the prompt template
    prompt = PromptTemplate(
        input_variables=["query", "chart_type", "style", "direction"],
        template=prompt_template,
    )

    # Execute the prompt
    llm_chain = LLMChain(llm=model, prompt=prompt)
    mermaid_syntax = llm_chain.run(
        query=query, chart_type=chart_type, style=style, direction=direction
    )

    return mermaid_syntax


async def generate_mermaid_image(mermaid_syntax: str) -> str:
    # Generate the Mermaid image URL from the syntax
    mermaid_url = syntax_to_image(mermaid_syntax)

    timeout = httpx.Timeout(10.0, read=None)
    async with httpx.AsyncClient() as client:
        response = await client.get(mermaid_url, timeout=timeout)

    if response.status_code == 200:
        filename = f"mermaid_{uuid4()}.png"
        image_path = os.path.join("public", "images", filename)
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        with open(image_path, "wb") as out:
            out.write(response.content)

        base_url = os.getenv("SERVER_NAME", "http://localhost:8080")
        image_url = f"{base_url}/public/images/{filename}"
        return image_url
    else:
        raise HTTPException(
            status_code=response.status_code,
            detail="Failed to generate Mermaid image.",
        )


def format_prompt(query: str, max_tokens: int) -> str:
    """
    Formats the prompt for generating Mermaid syntax.

    Args:
        query (str): The query or text to generate the Mermaid syntax for.
        max_tokens (int): The maximum number of tokens allowed in the generated syntax.

    Returns:
        str: The formatted prompt.
    """
    return f"""Generate a simple Mermaid.js diagram using the text below: {query}
    Give only the mermaid code. Exclude explanations. Escape any special characters in node with quotes. Ensure code is of max {max_tokens} tokens."""
