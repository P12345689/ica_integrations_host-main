# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Document Comparison Integration Router

This module provides routes for comparing two documents using LangChain and LLMs.
It supports various comparison use cases based on the provided instruction.
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List
from uuid import uuid4

from fastapi import FastAPI, Request
from jinja2 import Environment, FileSystemLoader
from langchain.base_language import BaseLanguageModel
from langchain.schema import HumanMessage
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_consultingassistants import ChatConsultingAssistants
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

# LLM Configuration
LLM_TYPE = os.getenv("LLM_TYPE", "consulting_assistants")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "Llama3.1 70b Instruct")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Other configuration
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
DEFAULT_CONTEXT_LENGTH = int(os.getenv("DEFAULT_CONTEXT_LENGTH", 4096))
DEFAULT_TEMPERATURE = float(os.getenv("DEFAULT_TEMPERATURE", 0.7))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/compare/templates"))


class CompareInputModel(BaseModel):
    """Model to validate input data for document comparison."""

    document1: str = Field(..., description="The first document to compare")
    document2: str = Field(..., description="The second document to compare")
    instruction: str = Field(..., description="The instruction for comparison")
    output_format: str = Field(default="markdown", description="Output format (plain or markdown)")
    context_length: int = Field(default=DEFAULT_CONTEXT_LENGTH, description="Context length for the LLM")
    temperature: float = Field(default=DEFAULT_TEMPERATURE, description="Temperature for the LLM")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_llm(model_name: str, temperature: float, max_tokens: int) -> BaseLanguageModel:
    """Initialize and return the specified language model."""
    if LLM_TYPE == "consulting_assistants":
        return ChatConsultingAssistants(model=model_name, max_tokens=max_tokens)
    elif LLM_TYPE == "openai":
        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not set. Please set the OPENAI_API_KEY environment variable.")
        return ChatOpenAI(model_name=model_name, temperature=temperature, max_tokens=max_tokens)
    elif LLM_TYPE == "ollama":
        return Ollama(model=model_name, base_url=OLLAMA_BASE_URL)
    else:
        raise ValueError(f"Unsupported LLM type: {LLM_TYPE}")


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/experience/compare/compare_documents/invoke")
    async def compare_documents(request: Request) -> OutputModel:
        """
        Handle POST requests to compare two documents based on the given instruction.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Example:
            >>> from fastapi.testclient import TestClient
            >>> client = TestClient(app)
            >>> headers = { "Content-Type": "application/json", "Integrations-API-Key": "dev-only-token" }
            >>> response = client.post("/experience/compare/compare_documents/invoke",
            ...     json={"document1": "Content of first document...",
            ...           "document2": "Content of second document...",
            ...           "instruction": "Compare these legal documents and identify differences",
            ...           "output_format": "markdown"}, headers=headers)
            >>> assert response.status_code == 200
            >>> assert "invocationId" in response.json()
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = CompareInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=f"Invalid input: {str(e)}")],
            )

        try:
            # Initialize LLM
            llm = get_llm(DEFAULT_MODEL, input_data.temperature, input_data.context_length)

            # Load comparison prompt template
            compare_prompt_template = template_env.get_template("compare_prompt.jinja").render(
                document1=input_data.document1,
                document2=input_data.document2,
                instruction=input_data.instruction,
                output_format=input_data.output_format,
            )

            # Log the formatted prompt for debugging
            log.debug(f"Formatted prompt: {compare_prompt_template}")

            # Run the comparison in a separate thread
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                compare_future = executor.submit(
                    asyncio.run,
                    asyncio.to_thread(lambda: llm.invoke([HumanMessage(content=compare_prompt_template)])),
                )
                result = compare_future.result()
                comparison_result = result if isinstance(result, str) else result.content

            # Render the response
            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(comparison=comparison_result)

            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=rendered_response)],
            )

        except Exception as e:
            log.error(f"Error during document comparison: {str(e)}")
            return OutputModel(
                status="success",
                invocationId=invocation_id,
                response=[ResponseMessageModel(message=f"An error occurred during document comparison: {str(e)}")],
            )
