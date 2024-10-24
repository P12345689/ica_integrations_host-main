# -*- coding: utf-8 -*-
"""
Author: wwwwen@cn.ibm.com
Description: these integrations is provided by GreenStar team. With these integrations, you can generate more relevant,
comprehensive and insightful results to user's question.

Notes for integration developers:
1. Use Pydantic v2 models to validate all inputs and all outputs
2. All functions should be defined as async
3. Ensure that all code has full docstring coverage in Google docstring format
4. Full unit test coverage (can also use doctest)
"""

import json
import logging
from typing import Any, Dict, List, Literal

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError
from starlette.responses import StreamingResponse
from typing_extensions import Annotated

from .gs_agents import aget_agent_results

log = logging.getLogger(__name__)

DEFAULT_MODEL = "Llama3.1 70b Instruct"


class InputModel(BaseModel):
    """Model to validate input data."""

    prompt: str


class LLMResponseModel(BaseModel):
    """Model to structure the LLM response data."""

    requestType: str
    requestData: Dict[str, Any]
    curlCommand: str
    llmResponse: str


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text", "image"]


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str
    response: Annotated[List[ResponseMessageModel], Field(min_length=1)]


def add_custom_routes(app: FastAPI) -> None:
    """Add custom routes to the FastAPI app.

    Args:
        app (FastAPI): The FastAPI application instance.
    """

    @app.api_route("/gs_agents/researcher/invoke", methods=["POST"])
    async def gs_researcher_agent(request: Request):
        """Handle POST requests to the invoke endpoint.

        Args:
            request (Request): The request object containing the input data.
        Raises:
            HTTPException: If the JSON is invalid or if validation fails.
        """
        try:
            data = await request.json()
            prompt = InputModel(**data).prompt
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=e.errors())

        agent_type = "researcher-agent-v2"
        params = {"kb_name": "ASKISC_GENERAL_KB"}
        return StreamingResponse(aget_agent_results(agent_type, prompt, params))
