# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Creates diagrams using graphviz, returning a PNG

This module provides routes for graphviz, including a system route
for generating a PNG from graphviz syntax, and an experience route that
uses an LLM to generate graphviz syntax and then create a PNG.
"""

import asyncio
import logging
import os
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

# Set up logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set to INFO in production

# Set default model and max threads from environment variables
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/graphviz/templates"))


class GraphvizInputModel(BaseModel):
    """Model to validate input data for graphviz generation."""

    syntax: str = Field(..., description="The graphviz syntax to generate the diagram")


class ExperienceInputModel(BaseModel):
    """Model to validate input data for the experience route."""

    query: str = Field(..., description="The input query describing the desired diagram")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def generate_png(syntax: str) -> str:
    """
    Generate a PNG file from graphviz syntax using the dot command.

    Args:
        syntax (str): The graphviz syntax.

    Returns:
        str: The URL of the generated PNG file.

    Raises:
        RuntimeError: If the PNG generation fails.
    """
    try:
        log.debug(f"Generating PNG from syntax: {syntax}")
        with tempfile.NamedTemporaryFile(mode="w", suffix=".dot", delete=False) as dot_file:
            dot_file.write(syntax)
            dot_file_path = dot_file.name

        png_file_path = f"public/graphviz/diagram_{uuid4()}.png"
        os.makedirs(os.path.dirname(png_file_path), exist_ok=True)

        result = subprocess.run(
            ["dot", "-Tpng", dot_file_path, "-o", png_file_path],
            capture_output=True,
            text=True,
            check=True,
        )

        png_url = f"{SERVER_NAME}/{png_file_path}"
        log.debug(f"Generated PNG URL: {png_url}")
        return png_url
    except subprocess.CalledProcessError as e:
        log.error(f"Error generating PNG: {e}")
        raise RuntimeError("Failed to generate PNG")
    finally:
        if os.path.exists(dot_file_path):
            os.remove(dot_file_path)


def add_custom_routes(app: FastAPI):
    @app.post("/system/graphviz/generate_png/invoke")
    async def generate_png_route(request: Request) -> OutputModel:
        """
        Handle POST requests to generate a PNG from graphviz syntax.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or PNG generation fails.
        """
        log.info("Received request to generate PNG")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = GraphvizInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(generate_png, input_data.syntax)
                png_url = future.result()
        except RuntimeError as e:
            log.error(f"Error generating PNG: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate PNG")

        log.info(f"Generated PNG: {png_url}")
        response_message = ResponseMessageModel(
            message=f"{png_url}\n\nGraphviz syntax that generated this image:\n\n```\n{input_data.syntax}\n```"
        )
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/graphviz/generate_diagram/invoke")
    async def generate_diagram_experience(request: Request) -> OutputModel:
        """
        Handle POST requests for the graphviz diagram generation experience.

        This route uses an LLM to generate graphviz syntax from a query,
        then generates a PNG from that syntax.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        log.info("Received request for graphviz diagram generation experience")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ExperienceInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        # Render the prompt using Jinja2
        prompt_template = template_env.get_template("prompt.jinja")
        rendered_prompt = prompt_template.render(query=input_data.query)
        log.debug(f"Rendered prompt: {rendered_prompt}")

        # Call the LLM
        client = ICAClient()

        async def call_prompt_flow():
            """Async wrapper for the LLM call."""
            log.debug("Calling LLM")
            return await asyncio.to_thread(
                client.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_prompt,
            )

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                graphviz_syntax_future = executor.submit(asyncio.run, call_prompt_flow())
                graphviz_syntax = graphviz_syntax_future.result()
            log.debug(f"Received LLM response: {graphviz_syntax}")
        except Exception as e:
            log.error(f"Error calling LLM: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing request")

        # Generate PNG from the graphviz syntax
        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                png_url_future = executor.submit(generate_png, graphviz_syntax)
                png_url = png_url_future.result()
        except RuntimeError as e:
            log.error(f"Error generating PNG: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate PNG")

        # Render the response
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(png_url=png_url, syntax=graphviz_syntax)
        log.debug(f"Rendered response: {rendered_response}")

        response_message = ResponseMessageModel(message=rendered_response)
        log.info("Graphviz diagram generation experience request processed successfully")
        return OutputModel(invocationId=invocation_id, response=[response_message])
