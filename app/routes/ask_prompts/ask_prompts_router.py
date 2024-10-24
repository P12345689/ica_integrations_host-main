# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Prompt integration router.

This module provides routes for retrieving and filtering prompts.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
import re
from concurrent.futures import ThreadPoolExecutor
from enum import Enum
from fnmatch import fnmatch
from typing import List, Optional, Union
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3 8B Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/ask_prompts/templates"))


class Visibility(str, Enum):
    """Enum for prompt visibility options."""

    PRIVATE = "PRIVATE"
    TEAM = "TEAM"
    PUBLIC = "PUBLIC"


class TagModel(BaseModel):
    """Model to validate a tag."""

    name: str


class RoleModel(BaseModel):
    """Model to validate a role."""

    name: str


class PromptInputModel(BaseModel):
    """Model to validate input data for prompt retrieval."""

    tags: Optional[List[str]] = Field(default=None, description="List of tags to filter prompts (supports glob)")
    roles: Optional[List[str]] = Field(default=None, description="List of roles to filter prompts")
    search_term: Optional[str] = Field(
        default=None,
        description="Search term for prompt title or description (supports regex and glob)",
    )
    visibility: Optional[Union[Visibility, str]] = Field(
        default=None,
        description="Visibility filter (PRIVATE, TEAM, PUBLIC, or * for any)",
    )
    user_email: Optional[str] = Field(default=None, description="Filter by user email")
    prompt_id: Optional[str] = Field(default=None, description="Specific prompt ID to retrieve")
    refresh: Optional[bool] = Field(default=False, description="Whether to refresh the prompts data")


class PromptModel(BaseModel):
    """Model to structure individual prompt data."""

    promptId: str  # noqa: N815
    promptTitle: str  # noqa: N815
    description: str
    prompt: str
    tags: List[TagModel]
    roles: List[RoleModel]
    visibility: Visibility
    userEmail: str  # noqa: N815


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    prompts: List[PromptModel]
    type: str = "json"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def match_pattern(text: str, pattern: str) -> bool:
    """
    Match the pattern against the text using regex and glob patterns.

    Args:
        text (str): The text to search in.
        pattern (str): The search pattern (regex or glob).

    Returns:
        bool: True if the pattern matches, False otherwise.
    """
    if pattern == "*":
        return True
    try:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    except re.error:
        # If it's not a valid regex, try glob matching
        return fnmatch(text.lower(), pattern.lower())
    return False


def get_prompts(
    tags: Optional[List[str]] = None,
    roles: Optional[List[str]] = None,
    search_term: Optional[str] = None,
    visibility: Optional[Union[Visibility, str]] = None,
    user_email: Optional[str] = None,
    prompt_id: Optional[str] = None,
    refresh: bool = False,
) -> List[PromptModel]:
    """
    Retrieve and filter prompts based on the given criteria.

    Args:
        tags (Optional[List[str]]): List of tags to filter prompts (supports glob).
        roles (Optional[List[str]]): List of roles to filter prompts.
        search_term (Optional[str]): Search term for prompt title or description (supports regex and glob).
        visibility (Optional[Union[Visibility, str]]): Visibility filter (PRIVATE, TEAM, PUBLIC, or * for any).
        user_email (Optional[str]): Filter by user email.
        prompt_id (Optional[str]): Specific prompt ID to retrieve.
        refresh (bool): Whether to refresh the prompts data. Defaults to False.

    Returns:
        List[PromptModel]: List of filtered prompts.

    Example:
        >>> prompts = get_prompts(tags=["crew*"], visibility="*", refresh=True)
        >>> len(prompts) > 0
        True
    """
    client = ICAClient()
    all_prompts = client.get_prompts(roles=roles, refresh_data=refresh)

    filtered_prompts = []
    for prompt in all_prompts:
        if prompt_id and prompt["promptId"] != prompt_id:
            continue
        if visibility and visibility != "*":
            if Visibility(prompt["visibility"].upper()) != Visibility(visibility.upper()):
                continue
        if user_email and prompt["userEmail"].lower() != user_email.lower():
            continue
        if search_term:
            if not match_pattern(prompt["promptTitle"], search_term) and not match_pattern(prompt["description"], search_term):
                continue
        if tags:
            prompt_tags = [tag["name"].lower() for tag in prompt["tags"]]
            if not any(any(match_pattern(prompt_tag, tag_pattern.lower()) for tag_pattern in tags) for prompt_tag in prompt_tags):
                continue
        if roles:
            prompt_roles = [role["name"].lower() for role in prompt["roles"]]
            if not all(role.lower() in prompt_roles for role in roles):
                continue

        filtered_prompts.append(
            PromptModel(
                promptId=prompt["promptId"],
                promptTitle=prompt["promptTitle"],
                description=prompt["description"],
                prompt=prompt["prompt"],
                tags=[TagModel(name=tag["name"]) for tag in prompt["tags"]],
                roles=[RoleModel(name=role["name"]) for role in prompt["roles"]],
                visibility=Visibility(prompt["visibility"].upper()),
                userEmail=prompt["userEmail"],
            )
        )

    return filtered_prompts


def add_custom_routes(app: FastAPI):
    """Adds custom routes to the FastAPI application for agent invocation and result retrieval."""

    @app.post("/system/prompt/retrievers/get_prompts/invoke")
    async def get_prompts_route(request: Request) -> OutputModel:
        """
        Handle POST requests to retrieve and filter prompts.

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
            input_data = PromptInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                prompts_future = executor.submit(
                    get_prompts,
                    tags=input_data.tags,
                    roles=input_data.roles,
                    search_term=input_data.search_term,
                    visibility=input_data.visibility,
                    user_email=input_data.user_email,
                    prompt_id=input_data.prompt_id,
                    refresh=input_data.refresh,
                )
                filtered_prompts = prompts_future.result()

            response_message = ResponseMessageModel(prompts=filtered_prompts)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error processing request: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @app.post("/experience/prompt/ask_prompts/invoke")
    async def ask_prompts(request: Request) -> OutputModel:
        """
        Handle POST requests to ask questions about prompts using an LLM.

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
            input_data = PromptInputModel(**data)
            query = data.get("query")
            if not query:
                raise ValueError("Query is required for this endpoint")
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                prompts_future = executor.submit(
                    get_prompts,
                    tags=input_data.tags,
                    roles=input_data.roles,
                    search_term=input_data.search_term,
                    visibility=input_data.visibility,
                    user_email=input_data.user_email,
                    prompt_id=input_data.prompt_id,
                    refresh=input_data.refresh,
                )
                filtered_prompts = prompts_future.result()

            prompt_template = template_env.get_template("prompt_template.jinja")
            rendered_prompt = prompt_template.render(query=query, prompts=filtered_prompts)

            client = ICAClient()
            response = await asyncio.to_thread(
                client.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_prompt,
            )

            response_template = template_env.get_template("response_template.jinja")
            rendered_response = response_template.render(result=response)

            response_message = ResponseMessageModel(
                prompts=[
                    PromptModel(
                        promptId="N/A",
                        promptTitle="LLM Response",
                        description="Response from LLM about prompts",
                        prompt=rendered_response,
                        tags=[],
                        roles=[],
                        visibility=Visibility.PRIVATE,
                        userEmail="system@example.com",
                    )
                ]
            )
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error processing request: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")
