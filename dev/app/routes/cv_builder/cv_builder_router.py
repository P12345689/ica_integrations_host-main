# -*- coding: utf-8 -*-
"""
Author: Freddy Hernandez Rojas
Description: CV Builder integration

TODO: Remember to update the module-level docstring with specific details about your integration
and remove / address the TODOs in this template.
Remplace the example timestamp with a function of your choice.

This module provides routes for cv_builder, including a system route
for generating a timestamp, an experience route that wraps the system
functionality with LLM interaction, and a file generation route that creates
a timestamped file and returns its URL.

Integration Development Guidelines:
1. Use Pydantic v2 models to validate all inputs and outputs.
2. All functions should be defined as async.
3. Ensure that all code has full docstring coverage in Google docstring format.
4. Implement full unit test coverage (can also use doctest).
5. Use Jinja2 templates for LLM prompts and response formatting.
6. Implement proper error handling and logging.
7. Use environment variables for configuration where appropriate.
8. Follow PEP 8 style guidelines.

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

import httpx
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
BEARER_TOKEN_API_CV = os.getenv("BEARER_TOKEN_API_CV", "")
CV_API_URL = "https://cv-service-prod.dal1a.cirrus.ibm.com"  # CV Api URL

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")  # Default URL as fallback

# Load Jinja2 environment
# TODO: Update the template directory path if needed
template_env = Environment(loader=FileSystemLoader("dev/app/routes/cv_builder/templates"))


class ProfileUpdateRequestModel(BaseModel):
    """Model to validate input data for profile enhance."""

    user_id: str = Field(..., description="The user ID for fetching the CV")
    intent: str = Field(..., description="The intent for enhancing the profile description")
    section: str = Field(..., description="The Section of the profile intended to be enhanced")


class ProfilePostRequestModel(BaseModel):
    """Model to validate input data for profile update."""

    user_id: str = Field(..., description="The user ID for fetching the CV")
    section: str = Field(..., description="The Section of the profile intended to be enhanced")
    enhanced_section: str = Field(..., description="The enhanced section content")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


async def update_cv(user_id: str, updated_cv: dict):
    """
    Update the CV on the external API.

    Args:
        user_id (str): The user ID for updating the CV.
        updated_cv (dict): The updated CV data.

    Returns:
        dict: The API response.

    Raises:
        HTTPException: If the CV update fails.
    """
    BEARER_TOKEN = BEARER_TOKEN_API_CV
    async with httpx.AsyncClient() as client:
        headers = {
            "Authorization": f"Bearer {BEARER_TOKEN}",
            "Content-Type": "application/json",
        }
        print("URL API", f"{CV_API_URL}/cv/overview")
        response = await client.put(f"{CV_API_URL}/cv/overview", headers=headers, json=updated_cv)
        response.raise_for_status()
        return response.json()


async def fetch_cv(user_id: str):
    """
    Fetch the CV from the external API.

    Args:
        user_id (str): The user ID for fetching the CV.

    Returns:
        dict: The fetched CV data.

    Raises:
        HTTPException: If the CV fetching fails.
    """
    BEARER_TOKEN = BEARER_TOKEN_API_CV
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
        response = await client.get(f"{CV_API_URL}/cv/{user_id}", headers=headers)
        response.raise_for_status()
        return response.json()


def add_custom_routes(app: FastAPI):
    @app.post("/cv_builder/enhance_profile/invoke")
    async def enhance_profile_route(request: Request) -> OutputModel:
        """
        Handle POST requests to enhance the profile description.

        This endpoint connects to an external CV API to retrieve the current profile,
        uses an LLM to generate a proposed enhanced profile description using Jinja templates,
        and returns the result.

        Args:
            request (Request): The request object containing the user ID and intent.

        Returns:
            OutputModel: The structured output response with the enhanced profile description.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        log.info("Received request to enhance profile description")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ProfileUpdateRequestModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            # Get the specific CV section we want to enhance
            cv_section = await get_cv_section(input_data)
        except Exception as e:
            log.error(f"Error fetching CV: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch CV")

        if input_data.section == "full":
            # Render the prompt using Jinja2
            prompt_template = template_env.get_template("enhance_cv_full_prompt.jinja")
            rendered_prompt = prompt_template.render(description=cv_section, intent=input_data.intent)
            log.debug(f"Rendered prompt: {rendered_prompt}")
        else:
            # Render the prompt using Jinja2
            prompt_template = template_env.get_template("enhance_cv_prompt.jinja")
            rendered_prompt = prompt_template.render(description=cv_section, intent=input_data.intent)
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
                formatted_result_future = executor.submit(asyncio.run, call_prompt_flow())
                enhanced_description = formatted_result_future.result()
            log.debug(f"Received LLM response: {enhanced_description}")
        except Exception as e:
            log.error(f"Error calling LLM: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing request")

        if input_data.section == "full":
            # Render the response using Jinja2
            response_template = template_env.get_template("enhance_full_response.jinja")
            rendered_response = response_template.render(tailored_cv=enhanced_description, current_CV=cv_section)
            log.debug(f"Rendered response Full: {rendered_response}")
        else:
            # Render the response using Jinja2
            response_template = template_env.get_template("enhance_section_response.jinja")
            rendered_response = response_template.render(
                section=input_data.section,
                enhanced_description=enhanced_description,
                description=cv_section,
            )
            log.debug(f"Rendered response Section: {rendered_response}")

        response_message = ResponseMessageModel(message=rendered_response)
        log.info("Profile enhancement request processed successfully")
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/cv_builder/update_overview/invoke")
    async def update_overview_route(request: Request) -> OutputModel:
        """
        Handle POST requests to enhance the profile description.

        This endpoint connects to an external CV API to retrieve the current profile,
        uses an LLM to generate a proposed enhanced profile description using Jinja templates,
        and returns the result.

        Args:
            request (Request): The request object containing the user ID, section, and enhanced section content.

        Returns:
            OutputModel: The structured output response with the enhanced profile description.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        log.info("Received request to update profile description")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ProfilePostRequestModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            # Fetch the current CV
            cv_data = await fetch_cv(input_data.user_id)
        except Exception as e:
            log.error(f"Error fetching CV: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to fetch CV")

        # Update the specific section with the enhanced content
        cv_overview_and_key_skills = cv_data["cvs"]["EN-GB"]["overviewAndKeySkills"][0]

        if input_data.section == "overview":
            cv_overview_and_key_skills["profile"] = input_data.enhanced_section
        elif input_data.section == "key_skills":
            cv_overview_and_key_skills["keySkills"] = input_data.enhanced_section
        elif input_data.section == "key_courses":
            cv_overview_and_key_skills["keyCourses"] = input_data.enhanced_section
        else:
            raise HTTPException(status_code=400, detail=f"Invalid section: {input_data.section}")

        updated_cv = {
            "overviewAndKeySkills": [cv_overview_and_key_skills],
            "uid": input_data.user_id,
            "language": "EN-GB",
        }

        try:
            # Update the CV
            await update_cv(input_data.user_id, updated_cv)
        except Exception as e:
            log.error(f"Error updating CV: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to update CV")

        # Render the response using Jinja2
        response_template = template_env.get_template("update_section_response.jinja")
        rendered_response = response_template.render(enhanced_section=input_data.enhanced_section)
        log.debug(f"Rendered response Section: {rendered_response}")

        response_message = ResponseMessageModel(message=rendered_response)
        log.info("Profile enhancement request processed successfully")
        return OutputModel(invocationId=invocation_id, response=[response_message])


async def get_cv_section(input_data):
    # Fetch the CV data
    cv_data = await fetch_cv(input_data.user_id)

    # Dictionary to map section names to their corresponding paths in the CV data
    section_mapping = {
        "overview": cv_data["cvs"]["EN-GB"]["overviewAndKeySkills"][0]["profile"],
        "key_skills": cv_data["cvs"]["EN-GB"]["overviewAndKeySkills"][0]["keySkills"],
        "key_courses": cv_data["cvs"]["EN-GB"]["overviewAndKeySkills"][0]["keyCourses"],
        "experience": cv_data["cvs"]["EN-GB"]["workExperience"],
        "education": cv_data["cvs"]["EN-GB"]["education"],
        "languages": cv_data["cvs"]["EN-GB"]["languages"],
        "assignments": cv_data["cvs"]["EN-GB"]["assignmentHistory"],
    }

    # Access the specific section based on input_data.section
    if input_data.section in section_mapping:
        profile_section = section_mapping[input_data.section]
    elif input_data.section == "full":
        profile_section = cv_data["cvs"]["EN-GB"]
    else:
        raise ValueError(f"Invalid section: {input_data.section}")

    print("Profile section to enhance:", profile_section)
    return profile_section
