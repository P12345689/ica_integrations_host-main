# -*- coding: utf-8 -*-
"""
Author: Andrei Colhon
Description: An integration for Microsoft Teams, allowing commpands via LLM

This module provides routes for ms_teams providing an experience route that allows to call the Teams API via LLM commands
"""

import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import List
from uuid import uuid4

import requests
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

TEAMS_BASE_URL = "https://graph.microsoft.com/v1.0"

# Load Jinja2 environment
# TODO: Update the template directory path if needed
template_env = Environment(loader=FileSystemLoader("dev/app/routes/ms_teams/templates"))


# TODO: Update these models to match your integration's input requirements
class TeamsInputModel(BaseModel):
    """Model to validate input data for Teams operations."""

    action: str = Field(..., description="Action to perform")
    params: dict = Field(default={}, description="Additional data needed for action")
    token: str = Field(..., description="User's Graph API token")


class ExperienceInputModel(BaseModel):
    """Model to validate input data for the experience route."""

    query: str = Field(..., description="The input query about an action in Teams")
    access_token: str = Field(..., description="Teams access token")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


# TODO: Replace this function with your own implementation that generates the desired output for your integration. This is just a sample function.
def teams_operation(action: str, params: dict, token: str) -> str:
    """
    Perform an action on MS Teams

    Args:
        token (str): Teams access token.
        action (str): Action to perform.
        params (dict): Additional parameters for the action.

    Returns:
        str: Result of the operation.

    Raises:
        ValueError: If the action is not supported or if required parameters are missing.
    """

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    if action == "create_meeting":
        url = f"{TEAMS_BASE_URL}/me/events"
        response = requests.post(url=url, headers=headers, data=json.dumps(params))
        response.raise_for_status()
        return response.json()

    if action == "list_meetings":
        end_date = params.get("end_date")
        url = f"{TEAMS_BASE_URL}/me/calendarview?startdatetime={datetime.now()}&enddatetime={end_date}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        events = response.json()
        event_list = events.get("value", [])
        meeting_info = [
            f"Meeting Id: {e['id']}, Meeting subject: {e['subject']}, Meeting start time: {e.get('start', {}).get('dateTime')}, Meeting end time: {e.get('end', {}).get('dateTime')}"
            for e in event_list
        ]
        return "/n".join(meeting_info)

    if action == "get_meeting":
        id = params.get("id")
        url = f"{TEAMS_BASE_URL}/me/events/{id}"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        e = response.json()
        attendees = e.get("attendees", [])

        meeting_info = [
            f"Meeting subject: {e['subject']}",
            f"Meeting start time: {e.get('start', {}).get('dateTime')}",
            f"Meeting end time: {e.get('end', {}).get('dateTime')}",
            "Meeting attendees:",
        ]

        attendee_info = [
            f"{a.get('emailAddress', {}).get('name')} ({a.get('emailAddress', {}).get('address')})" for a in attendees
        ]

        return "\n".join(meeting_info + attendee_info)

    if action == "find_timeslots":
        url = f"{TEAMS_BASE_URL}/me/findMeetingTimes"
        response = requests.post(url, headers=headers, data=json.dumps(params))
        response.raise_for_status()
        timeslots = response.json().get("meetingTimeSuggestions")
        meeting_timeslots = [
            f"Timeslot:\nDate: {t.get('meetingTimeSlot').get('start').get('dateTime')[:10]},\nTime: {t.get('meetingTimeSlot').get('start').get('dateTime')[11:16]} - {t.get('meetingTimeSlot').get('end').get('dateTime')[11:16]}"
            for t in timeslots
        ]
        return "\n".join(meeting_timeslots)


def add_custom_routes(app: FastAPI):
    @app.post("/system/ms_teams/invoke")
    async def teams_route(request: Request) -> OutputModel:
        """
        Handle POST requests for Teams operations.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or the Teams operation fails.
        """
        log.info("Received request for Teams Operation")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = TeamsInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(
                    teams_operation,
                    input_data.action,
                    input_data.params,
                    input_data.token,
                )
                result = future.result()
        except ValueError as e:
            log.error(f"Error in Teams operation: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except requests.HTTPError as e:
            log.error(f"Teams API error: {str(e)}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            log.error(f"Error performing Teams operation: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to perform Teams operation")

        log.info(f"Teams operation completed: {input_data.action}")
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(result=result, action=input_data.action)
        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/ms_teams/invoke")
    async def teams_experience(request: Request) -> OutputModel:
        """
        Handle POST requests for Teams operations with LLM support.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """

        log.info("Received request for Teams experience")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = ExperienceInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        input_data.query = f"{input_data.query}. The current date-time is {datetime.now()}"
        prompt_template = template_env.get_template("prompt.jinja")
        rendered_prompt = prompt_template.render(query=input_data.query)

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
                llm_response_future = executor.submit(asyncio.run, call_prompt_flow())
                llm_response = llm_response_future.result()
            log.debug(f"Received LLM response: {llm_response}")
            operation_data = json.loads(llm_response)
            if operation_data.get("action"):
                teams_result = teams_operation(
                    operation_data["action"],
                    operation_data["params"],
                    input_data.access_token,
                )
                final_response = (
                    f"LLM Analysis:\n{operation_data.get('analysis', '')}\n\nTeams Operation Result:\n{teams_result}"
                )
            else:
                final_response = f"LLM Analysis:\n{operation_data.get('analysis', '')}"
        except json.JSONDecodeError as e:
            log.error(f"Error parsing JSON from LLM response: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing LLM response")

        except Exception as e:
            log.error(f"Error in Teams experience: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to process Teams experience")

        log.info("Teams experience executed successfully")
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(
            result=final_response,
            action=operation_data.get("action"),
            analysis=operation_data.get("analysis"),
        )

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])
