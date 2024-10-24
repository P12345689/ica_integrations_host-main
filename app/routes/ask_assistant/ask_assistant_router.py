# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Assistant integration router.

This module provides routes for retrieving assistant information and asking questions about assistants.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3 8B Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/ask_assistant/templates"))


class AssistantInputModel(BaseModel):
    """Model to validate input data for assistant retrieval."""

    tags: Optional[List[str]] = Field(default=None, description="List of tags to filter assistants")
    roles: Optional[List[str]] = Field(default=None, description="List of roles to filter assistants")
    search_term: Optional[str] = Field(default=None, description="Search term for assistant name or description")
    assistant_id: Optional[str] = Field(default=None, description="Specific assistant ID to retrieve")
    refresh: Optional[bool] = Field(default=False, description="Whether to refresh the assistants data")


class TagModel(BaseModel):
    """Model to validate a tag."""

    name: str


class RoleModel(BaseModel):
    """Model to validate a role."""

    name: str


class AssistantModel(BaseModel):
    """Model to structure individual assistant data."""

    id: str
    createdAt: str  # noqa: N815
    updatedAt: str  # noqa: N815
    modelId: str  # noqa: N815
    title: str
    description: str
    welcomeMessage: str  # noqa: N815
    expectedOutcome: str  # noqa: N815
    visibility: str
    tags: List[TagModel]
    roles: List[RoleModel]
    isAvailableToPublic: bool  # noqa: N815
    isRemix: bool  # noqa: N815


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_assistants(
    tags: Optional[List[str]] = None,
    roles: Optional[List[str]] = None,
    search_term: Optional[str] = None,
    assistant_id: Optional[str] = None,
    refresh: bool = False,
) -> List[AssistantModel]:
    """
    Retrieve and filter assistants based on the given criteria.

    Args:
        tags (Optional[List[str]]): List of tags to filter assistants.
        roles (Optional[List[str]]): List of roles to filter assistants.
        search_term (Optional[str]): Search term for assistant title or description.
        assistant_id (Optional[str]): Specific assistant ID to retrieve.
        refresh (bool): Whether to refresh the assistants data. Defaults to False.

    Returns:
        List[AssistantModel]: List of filtered assistants.

    Example:
        >>> assistants = get_assistants(tags=["unified"], roles=["Software Developer"], refresh=True)
        >>> len(assistants) > 0
        True
    """
    client = ICAClient()
    all_assistants = client.get_assistants(tags=tags, roles=roles, refresh_data=refresh)

    filtered_assistants = []
    for assistant in all_assistants:
        if assistant_id and assistant["id"] != assistant_id:
            continue
        if search_term and search_term.lower() not in assistant["title"].lower() and search_term.lower() not in assistant["description"].lower():
            continue

        filtered_assistants.append(AssistantModel(**assistant))

    return filtered_assistants


def add_custom_routes(app: FastAPI):
    """Adds custom routes to the FastAPI application for agent invocation and result retrieval."""

    @app.post("/system/assistant/retrievers/get_assistants/invoke")
    async def get_assistants_route(request: Request) -> OutputModel:
        """
        Handle POST requests to retrieve and filter assistants.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or an error occurs during processing.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = AssistantInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                assistants_future = executor.submit(
                    get_assistants,
                    tags=input_data.tags,
                    roles=input_data.roles,
                    search_term=input_data.search_term,
                    assistant_id=input_data.assistant_id,
                    refresh=input_data.refresh,
                )
                filtered_assistants = assistants_future.result()

            response_template = template_env.get_template("assistants_response.jinja")
            rendered_response = response_template.render(assistants=filtered_assistants)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error processing request: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @app.post("/experience/assistant/ask_assistant/invoke")
    async def ask_assistant(request: Request) -> OutputModel:
        """
        Handle POST requests to ask questions about assistants using an LLM.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or an error occurs during processing.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = AssistantInputModel(**data)
            query = data.get("query")
            if not query:
                raise ValueError("Query is required for this endpoint")
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                assistants_future = executor.submit(
                    get_assistants,
                    tags=input_data.tags,
                    roles=input_data.roles,
                    search_term=input_data.search_term,
                    assistant_id=input_data.assistant_id,
                    refresh=input_data.refresh,
                )
                filtered_assistants = assistants_future.result()

            prompt_template = template_env.get_template("prompt_template.jinja")
            rendered_prompt = prompt_template.render(query=query, assistants=filtered_assistants)

            client = ICAClient()
            response = await asyncio.to_thread(
                client.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_prompt,
            )

            response_template = template_env.get_template("llm_response.jinja")
            rendered_response = response_template.render(result=response, assistants=filtered_assistants)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error processing request: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
