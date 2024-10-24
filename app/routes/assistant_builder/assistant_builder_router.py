# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Generates assistants from provided description

This module provides an API endpoint for generating assistants based on a user's description.
It uses Jinja2 templates to render prompts and responses, and makes asynchronous calls to
an LLM (Language Model) using the ICAClient.

Examples:
    >>> from fastapi.testclient import TestClient
    >>> client = TestClient()
    >>> response = client.post("/assistant_builder/invoke", json={"input": "A helpful assistant to generate user stories"})
    >>> response.status_code
    200
    >>> response.json()["status"]
    "success"
"""

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from libica import ICAClient
from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# app = FastAPI()

DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/assistant_builder/templates"))
log.debug("Jinja2 environment initialized with template directory.")


class UserPrompt(BaseModel):
    """
    Represents the user's prompt for generating an assistant.

    Attributes:
        input (str): The description of the assistant to be generated.
    """

    input: str


def add_custom_routes(app: FastAPI) -> None:
    """
    Adds custom routes to the FastAPI application.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.post("/assistant_builder/invoke")
    async def assistant_builder(request: Request) -> JSONResponse:
        """
        Endpoint for generating assistants based on a user's description.

        Args:
            request (Request): The incoming request object.

        Returns:
            JSONResponse: The response containing the generated assistant's task and examples.

        Raises:
            HTTPException: If there's an error processing the request or if templates are not found.
        """
        try:
            body_text = await request.body()
            log.info(f"Received raw request body: {body_text}")

            clean_text = body_text.replace(b"\r\n", b"\n").decode("utf-8")
            formatted_json = clean_text.replace("\n", "\\n")
            log.info(f"Cleaned request text from Windows newlines: {formatted_json}")

            user_prompt = UserPrompt.parse_raw(formatted_json)
            log.info(f"Parsed JSON data successfully: {user_prompt}")
        except json.JSONDecodeError as e:
            log.error(f"Failed to decode JSON: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid JSON input")

        try:
            client = ICAClient()

            # Check and log template availability first
            try:
                prompt_template = template_env.get_template("prompt_template.jinja")
                examples_prompt_template = template_env.get_template("examples_prompt_template.jinja")
                task_prompt_template = template_env.get_template("task_prompt_template.jinja")
                log.info("Templates found and loaded successfully.")
            except TemplateNotFound:
                log.error("Template files not found.")
                raise HTTPException(status_code=500, detail="Internal server error")

            # Render the task prompt template with the user's input
            task_prompt = task_prompt_template.render(user_input=user_prompt.input)
            log.info(f"Task prompt rendered: {task_prompt}")

            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                # First call to LLM to determine the task
                task_future = executor.submit(
                    client.prompt_flow,
                    model_id_or_name=DEFAULT_MODEL,
                    prompt=task_prompt,
                )

                # Wait for the task response
                task_response = task_future.result()
                log.info(f"LLM task response: {task_response}")

                # Render the examples prompt template with the task response
                examples_prompt = examples_prompt_template.render(task=task_response)
                log.info(f"Examples prompt rendered: {examples_prompt}")

                # Second call to LLM to generate examples for the task
                examples_future = executor.submit(
                    client.prompt_flow,
                    model_id_or_name=DEFAULT_MODEL,
                    prompt=examples_prompt,
                )

                # Wait for the examples response
                examples_response = examples_future.result()
                log.info(f"LLM examples response: {examples_response}")

            # Render the response template
            result = prompt_template.render(response={"task": task_response, "examples": examples_response})
            log.info("Template rendered successfully.")

            return JSONResponse(
                content={
                    "status": "success",
                    "response": [{"message": result, "type": "text"}],
                    "invocationId": str(uuid4()),
                }
            )

        except Exception as e:
            log.error(f"Failed to process the request: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")


# add_custom_routes(app)
