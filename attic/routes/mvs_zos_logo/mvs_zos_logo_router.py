# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: MVS/z/OS Logo Generator integration router.

This module provides routes for generating custom logos for MVS and z/OS systems
in assembly language format.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/mvs_zos_logo/templates"))


class LogoInputModel(BaseModel):
    """Model to validate input data for logo generation."""

    logo_text: str = Field(..., description="The text-based logo to convert")
    start_line: int = Field(default=7, description="The starting line number for the logo")
    start_column: int = Field(default=15, description="The starting column number for the logo")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def generate_logo_assembly(logo_text: str, start_line: int, start_column: int) -> str:
    """
    Generate assembly language code for displaying a logo on MVS/z/OS.

    Args:
        logo_text (str): The text-based logo to convert.
        start_line (int): The starting line number for the logo.
        start_column (int): The starting column number for the logo.

    Returns:
        str: The generated assembly language code.

    Example:
        >>> logo = "ABC\\nDEF"
        >>> result = generate_logo_assembly(logo, 7, 15)
        >>> assert "$SBA   (7,15)" in result
        >>> assert "DC     C'ABC'" in result
        >>> assert "$SBA   (8,15)" in result
        >>> assert "DC     C'DEF'" in result
    """
    assembly_code = []
    for i, line in enumerate(logo_text.split("\n"), start=start_line):
        assembly_code.extend(
            [
                f"         $SBA   ({i},{start_column})",
                f"         DC     C'{line}'",
                "         $SF    (SKIP,HI)",
            ]
        )
    return "\n".join(assembly_code)


def add_custom_routes(app: FastAPI):
    @app.post("/system/mvs_zos_logo/generate/invoke")
    async def generate_logo(request: Request) -> OutputModel:
        """
        Handle POST requests to generate MVS/z/OS logo assembly code.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or an error occurs during generation.

        Example:
            >>> from fastapi.testclient import TestClient
            >>> client = TestClient(app)
            >>> response = client.post("/system/mvs_zos_logo/generate/invoke",
            ...     json={"logo_text": "ABC\\nDEF"})
            >>> assert response.status_code == 200
            >>> assert "invocationId" in response.json()
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = LogoInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input data: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                assembly_code = await asyncio.to_thread(
                    generate_logo_assembly,
                    input_data.logo_text,
                    input_data.start_line,
                    input_data.start_column,
                )
        except Exception as e:
            log.error(f"Error generating logo assembly: {str(e)}")
            raise HTTPException(status_code=500, detail="Error generating logo assembly")

        response_message = ResponseMessageModel(message=assembly_code)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/mvs_zos_logo/generate_creative/invoke")
    async def generate_creative_logo(request: Request) -> OutputModel:
        """
        Handle POST requests to generate a creative MVS/z/OS logo using an LLM.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or an error occurs during generation.

        Example:
            >>> from fastapi.testclient import TestClient
            >>> client = TestClient(app)
            >>> response = client.post("/experience/mvs_zos_logo/generate_creative/invoke",
            ...     json={"theme": "Space exploration"})
            >>> assert response.status_code == 200
            >>> assert "invocationId" in response.json()
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            theme = data.get("theme", "")
        except Exception as e:
            log.error(f"Invalid input data: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        # Render the prompt using Jinja2
        prompt_template = template_env.get_template("prompt_template.jinja")
        rendered_prompt = prompt_template.render(theme=theme)

        # Call the LLM
        client = ICAClient()

        async def call_prompt_flow():
            try:
                return await asyncio.to_thread(
                    client.prompt_flow,
                    model_id_or_name=DEFAULT_MODEL,
                    prompt=rendered_prompt,
                )
            except Exception as e:
                log.error(f"Error calling prompt_flow: {str(e)}")
                raise HTTPException(status_code=500, detail="Error generating creative logo")

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            try:
                logo_text_future = executor.submit(asyncio.run, call_prompt_flow())
                logo_text = logo_text_future.result()
            except Exception as e:
                log.error(f"Error in ThreadPoolExecutor: {str(e)}")
                raise HTTPException(status_code=500, detail="Error processing request")

        # Generate assembly code from the created logo
        try:
            assembly_code = generate_logo_assembly(logo_text, 7, 15)
        except Exception as e:
            log.error(f"Error generating logo assembly: {str(e)}")
            raise HTTPException(status_code=500, detail="Error generating logo assembly")

        # Render the response
        response_template = template_env.get_template("response_template.jinja")
        rendered_response = response_template.render(logo_text=logo_text, assembly_code=assembly_code)

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])
