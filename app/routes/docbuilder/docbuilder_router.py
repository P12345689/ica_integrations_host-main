# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Document Builder - Builds pptx and docx documents from input markdown or topic text.

The main functionality includes:
- Validating input data using Pydantic models.
- Generating markdown content using an LLM if the input text is not already in markdown format.
- Cleaning and preprocessing the markdown content.
- Generating docx and pptx documents asynchronously using the cleaned markdown content.
- Handling errors and providing informative responses to the user.
- Using Jinja2 templates for formatting the prompts and responses.

Example usage:
    # Make a POST request to the /experience/docbuilder/generate_docs/invoke endpoint with the following JSON payload:
    {
        "input_text": "The impact of artificial intelligence on modern society",
        "template_type": "IBM Consulting Green",
        "author_name": "John Doe",
        "author_email": "john.doe@example.com",
        "context": "Previous conversation about AI and its impact on society.",
        "llm_override": "Llama3 8B Instruct"
    }

    The response will contain the URLs of the generated docx and pptx documents, along with the cleaned markdown content.
"""

import asyncio
import json
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List, Literal, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, EmailStr, Field

from app.routes.docbuilder.tools.generate_docs import generate_docx_async, generate_pptx_async

log = logging.getLogger(__name__)

DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/docbuilder/templates"))


class InputModel(BaseModel):
    """Model to validate input data."""

    input_text: str
    template_type: str = Field(default="Styling free template")
    author_name: Optional[str] = None
    author_email: Optional[EmailStr] = None
    context: Optional[str] = None
    llm_override: Optional[str] = None


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text", "image"]


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel] = Field(min_items=1)


def clean_markdown_edge_quotes(input_text: str) -> str:
    """
    Removes any leading text or markdown indicators before the title block and trailing content after the last slide.

    Args:
        input_text (str): The markdown text to clean.

    Returns:
        str: The cleaned markdown text.

    Examples:
        >>> clean_markdown_edge_quotes('Here is a presentation:\\n% AI Impact\\n% John Doe\\n% 2023-08-11\\nContent\\n```')
        '% AI Impact\\n% John Doe\\n% 2023-08-11\\nContent'
        >>> clean_markdown_edge_quotes('```markdown\\n% AI Impact\\n% John Doe\\n% 2023-08-11\\nContent\\n```')
        '% AI Impact\\n% John Doe\\n% 2023-08-11\\nContent'
        >>> clean_markdown_edge_quotes('% AI Impact\\n% John Doe\\n% 2023-08-11\\nContent\\n```')
        '% AI Impact\\n% John Doe\\n% 2023-08-11\\nContent'
        >>> clean_markdown_edge_quotes('Content without title block')
        'Content without title block'
    """
    # Strip leading/trailing whitespace
    input_text = input_text.strip()

    # Remove any leading markdown indicators and text before the title block
    pattern = r"^(```\w*\s*\n*)?(.*?)(% .*\n% .*\n% .*\n)"
    match = re.search(pattern, input_text, re.DOTALL)
    if match:
        input_text = input_text[match.start(3) :]  # Start from the title block

    # Remove any trailing content after the last slide
    # This assumes that the last slide ends with a notes section
    last_notes_index = input_text.rfind(":::")
    if last_notes_index != -1:
        input_text = input_text[: last_notes_index + 3]  # Keep the last ':::'

    return input_text.strip()


def get_ibm_template_name(template_type: str) -> str:
    """
    Get the IBM template name based on the provided template type.

    Args:
        template_type (str): The type of template.

    Returns:
        str: The corresponding IBM template name.

    Examples:
        >>> get_ibm_template_name("IBM Consulting Green")
        'templates/ibm_consulting_green.pptx'
        >>> get_ibm_template_name("IBM Technology Blue")
        'templates/ibm_technology_blue.pptx'
        >>> get_ibm_template_name("Unknown Type")
        'templates/ibm_consulting_green.pptx'
    """
    # Use the default template type as standard
    template_name = "templates/default.pptx"

    # Check the template type
    if template_type == "IBM Consulting Green":
        template_name = "templates/ibm_consulting_green.pptx"
    elif template_type == "IBM Consulting Blue":
        template_name = "templates/ibm_consulting_blue.pptx"
    elif template_type == "IBM Technology Blue":
        template_name = "templates/ibm_technology_blue.pptx"
    elif template_type == "IBM Technology Green":
        template_name = "templates/ibm_technology_green.pptx"
    elif template_type == "Services Integration Hub":
        template_name = "templates/sih_template.pptx"
    elif template_type == "Corporate Strategy":
        template_name = "templates/corporate_strategy_template.pptx"
    elif template_type == "OIC":
        template_name = "templates/oic_template.pptx"

    return template_name


async def call_llm_async(prompt: str, model_override: Optional[str] = None) -> str:
    """
    Call the LLM with the given prompt asynchronously.

    Args:
        prompt (str): The prompt to send to the LLM.
        model_override (Optional[str]): The model to use instead of the default one.

    Returns:
        str: The response from the LLM.

    Raises:
        HTTPException: If there is an error calling the LLM.
    """
    try:
        log.debug(f"Calling LLM with prompt: {prompt}")
        client = ICAClient()
        model_id_or_name = model_override or DEFAULT_MODEL
        log.info(f"Using model: {model_id_or_name}")
        response = await asyncio.to_thread(client.prompt_flow, model_id_or_name=model_id_or_name, prompt=prompt)
        log.debug(f"Received response from LLM: {response}")
        return response
    except Exception as e:
        log.error(f"Error calling LLM: {e}")
        raise HTTPException(status_code=500, detail="Error calling LLM")


def add_custom_routes(app: FastAPI) -> None:
    """Adds custom routes to the FastAPI application for agent invocation and result retrieval."""

    @app.api_route("/docbuilder/invoke", methods=["POST"])
    async def docbuilder_orig(request: Request):
        return await docbuilder(request)

    @app.api_route("/experience/docbuilder/generate_docs/invoke", methods=["POST"])
    async def docbuilder(request: Request):
        """
        Handles the POST request to build documents from input markdown or topic text.

        Args:
            request (Request): The incoming request object.

        Returns:
            Dict[str, Any]: The response containing the generated document URLs and markdown content.

        Raises:
            HTTPException: If there is an error processing the request or generating the documents.
        """
        try:
            data = await request.json()
            input_data = InputModel(**data)
        except json.JSONDecodeError:
            data = await request.form()
            input_data = InputModel(**data)

        input_text = input_data.input_text.strip()
        template_type = input_data.template_type
        author_name = input_data.author_name or "Anonymous"
        author_email = input_data.author_email or "anonymous@example.com"
        context = input_data.context or ""
        llm_override = input_data.llm_override

        log.debug(f"Received input text: {input_text}")
        log.debug(f"Selected template type: {template_type}")
        log.debug(f"Author name: {author_name}")
        log.debug(f"Author email: {author_email}")
        log.debug(f"Context: {context}")
        log.debug(f"LLM override: {llm_override}")

        markdown_content = input_text

        template_name = get_ibm_template_name(template_type)
        log.info(f"Selected template name: {template_name}")

        if not input_text.startswith("%"):
            log.info("Input text is not in markdown format, calling LLM")
            prompt_template = template_env.get_template("prompt_template.jinja")
            full_prompt = prompt_template.render(
                input_text=input_text,
                author_name=author_name,
                author_email=author_email,
                context=context,
                date=datetime.now().strftime("%Y-%m-%d"),
            )
            log.debug(f"{full_prompt}")

            model_output = await call_llm_async(full_prompt, llm_override)

            log.debug(f"Received from LLM:\n{model_output}")

            markdown_content = clean_markdown_edge_quotes(model_output)
            log.debug(f"Cleaned markdown:\n{markdown_content}")

        os.makedirs("temp", exist_ok=True)
        os.makedirs("public/documents", exist_ok=True)
        os.makedirs("public/documents/docx", exist_ok=True)
        os.makedirs("public/documents/pptx", exist_ok=True)

        log.info("Generating docx and pptx documents asynchronously")

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            docx_future = executor.submit(asyncio.run, generate_docx_async(markdown_content))
            pptx_future = executor.submit(asyncio.run, generate_pptx_async(markdown_content, template_name))

        docx_url = docx_future.result()
        pptx_url = pptx_future.result()

        log.info(f"Generated docx URL: {docx_url}")
        log.info(f"Generated pptx URL: {pptx_url}")

        invocation_id = str(uuid4())

        template = template_env.get_template("response_template.jinja")
        rendered_response = template.render(docx_url=docx_url, pptx_url=pptx_url, markdown_content=markdown_content)

        response_dict = ResponseMessageModel(message=rendered_response, type="text")
        response_data = OutputModel(invocationId=invocation_id, response=[response_dict])

        return response_data
