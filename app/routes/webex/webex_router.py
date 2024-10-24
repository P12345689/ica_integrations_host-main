# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: WebEx Integration for retrieving and summarizing call transcripts

This module provides routes for various WebEx operations, including retrieving
transcript lists, specific transcripts, and summarizing transcripts using an LLM.
"""

import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
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
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Mixtral 8x7b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

# WebEx API base URL
WEBEX_API_BASE_URL = "https://webexapis.com/v1"

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/webex/templates"))


class WebExInputModel(BaseModel):
    """Model to validate input data for WebEx operations."""

    action: str = Field(
        ...,
        description="Action to perform (e.g., 'list_transcripts', 'get_transcript')",
    )
    params: dict = Field(default={}, description="Additional parameters for the action")
    webex_token: str = Field(..., description="WebEx access token")


class ExperienceInputModel(BaseModel):
    """Model to validate input data for the experience route."""

    query: str = Field(..., description="The input query describing the desired WebEx operation")
    webex_token: str = Field(..., description="WebEx access token")


class SummarizeTranscriptInputModel(BaseModel):
    """Model to validate input data for the summarize transcript route."""

    transcript_id: str = Field(..., description="The ID of the transcript to summarize")
    query: Optional[str] = Field(None, description="Custom query for summarization")
    webex_token: str = Field(..., description="WebEx access token")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def webex_operation(token: str, action: str, params: dict) -> str:
    """
    Perform a WebEx operation based on the given action using REST API.

    Args:
        token (str): WebEx access token.
        action (str): Action to perform.
        params (dict): Additional parameters for the action.

    Returns:
        str: Result of the operation.

    Raises:
        ValueError: If the action is not supported or if required parameters are missing.
    """
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    if action == "list_transcripts":
        url = f"{WEBEX_API_BASE_URL}/meetingTranscripts"
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        transcripts = response.json().get("items", [])
        return "\n".join([f"Transcript ID: {t['id']}, Meeting Topic: {t['meetingTopic']}" for t in transcripts])

    elif action == "get_transcript":
        transcript_id = params.get("transcript_id")
        if not transcript_id:
            raise ValueError("Transcript ID is required to get a transcript")

        url = f"{WEBEX_API_BASE_URL}/meetingTranscripts/{transcript_id}/download"
        format_param = params.get("format", "vtt")
        response = requests.get(url, headers=headers, params={"format": format_param})
        response.raise_for_status()
        return response.text

    elif action == "list_meetings":
        url = f"{WEBEX_API_BASE_URL}/meetings"
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        meetings = response.json().get("items", [])
        return "\n".join(f"Meeting ID: {m['id']}, Meeting title: {m['title']}, Meeting start time: {m['start']}, Meeting end time: {m['end']}, Timezone: {m['timezone']}" for m in meetings)

    elif action == "invite_people":
        meeting_id = params.get("meetingId")
        if not meeting_id:
            raise ValueError("Meeting ID is required to invite other people")

        url = f"{WEBEX_API_BASE_URL}/meetingInvitees"
        response = requests.post(url, headers=headers, json=params)
        response.raise_for_status()
        return response.text

    elif action == "list_meeting_invitees":
        meeting_id = params.get("meetingId")
        if not meeting_id:
            raise ValueError("Meeting ID is required to invite other people")

        url = f"{WEBEX_API_BASE_URL}/meetingInvitees?meetingId={meeting_id}"
        breakpoint()
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        invitees = response.json().get("items", [])
        return "\n".join(f"Invitee name: {i['displayName']}, Invitee email address: {i['email']}" for i in invitees)

    else:
        raise ValueError(f"Unsupported action: {action}")


def add_custom_routes(app: FastAPI):
    @app.post("/system/webex/invoke")
    async def webex_route(request: Request) -> OutputModel:
        """
        Handle POST requests for WebEx operations.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or the WebEx operation fails.
        """
        log.info("Received request for WebEx operation")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = WebExInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                future = executor.submit(
                    webex_operation,
                    input_data.webex_token,
                    input_data.action,
                    input_data.params,
                )
                result = future.result()
        except ValueError as e:
            log.error(f"Error in WebEx operation: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except requests.HTTPError as e:
            log.error(f"WebEx API error: {str(e)}")
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except Exception as e:
            log.error(f"Error performing WebEx operation: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to perform WebEx operation")

        log.info(f"WebEx operation completed: {input_data.action}")
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(result=result, action=input_data.action)
        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/webex/invoke")
    async def webex_experience(request: Request) -> OutputModel:
        """
        Handle POST requests for WebEx operations with LLM support.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        log.info("Received request for WebEx experience")
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
                llm_response_future = executor.submit(asyncio.run, call_prompt_flow())
                llm_response = llm_response_future.result()
            log.debug(f"Received LLM response: {llm_response}")

            # Process LLM response and perform WebEx operation if needed
            action_data = json.loads(llm_response)
            if action_data.get("action"):
                webex_result = webex_operation(
                    input_data.webex_token,
                    action_data["action"],
                    action_data.get("params", {}),
                )
                if action_data["action"] == "list_transcripts":
                    # Get the most recent transcript
                    transcript_id = webex_result.split("\n")[0].split(": ")[1].split(",")[0]
                    webex_result += "\n\nRetrieving the most recent transcript:\n"
                    webex_result += webex_operation(
                        input_data.webex_token,
                        "get_transcript",
                        {"transcript_id": transcript_id},
                    )
                final_response = f"LLM Analysis:\n{action_data.get('analysis', '')}\n\nWebEx Operation Result:\n{webex_result}"
            else:
                final_response = f"LLM Analysis:\n{action_data.get('analysis', '')}"

        except json.JSONDecodeError as e:
            log.error(f"Error parsing JSON from LLM response: {str(e)}")
            raise HTTPException(status_code=500, detail="Error processing LLM response")
        except Exception as e:
            log.error(f"Error in WebEx experience: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to process WebEx experience")

        log.info("WebEx experience request processed successfully")
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(
            result=final_response,
            action=action_data.get("action"),
            analysis=action_data.get("analysis"),
        )
        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/webex/summarize_transcript")
    async def summarize_transcript(request: Request) -> OutputModel:
        """
        Handle POST requests to summarize a specific transcript.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or processing fails.
        """
        log.info("Received request to summarize transcript")
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            log.debug(f"Received input data: {data}")
            input_data = SummarizeTranscriptInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            # Get the transcript
            transcript = webex_operation(
                input_data.webex_token,
                "get_transcript",
                {"transcript_id": input_data.transcript_id},
            )

            # Prepare the summarization prompt
            default_query = "Please provide a concise summary of the following meeting transcript:"
            query = input_data.query if input_data.query else default_query
            prompt = f"{query}\n\n{transcript}"

            # Call the LLM for summarization
            client = ICAClient()
            summary = await asyncio.to_thread(client.prompt_flow, model_id_or_name=DEFAULT_MODEL, prompt=prompt)

            final_response = f"Transcript Summary:\n\n{summary}"

        except Exception as e:
            log.error(f"Error in transcript summarization: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to summarize transcript")

        log.info("Transcript summarization completed successfully")
        response_template = template_env.get_template("response.jinja")
        rendered_response = response_template.render(result=final_response, action="summarize_transcript")
        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])


# TODO: Add any additional routes or helper functions as needed for your integration
