
import asyncio
import json
import logging
import os
from typing import Dict, List, Literal
from uuid import uuid4
from typing_extensions import Annotated
from fastapi import HTTPException
from pydantic import BaseModel, Field
from libica import ICAClient


logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class ExecutionRequest(BaseModel):
    """
    Represents the request for executing an assistant.

    Attributes:
        assistant_id (str): The ID of the assistant to be executed.
        prompt (str): The prompt to be passed to the assistant.
    """

    assistant_id: str
    prompt: str


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text", "image"]


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: Annotated[List[ResponseMessageModel], Field(min_length=1)]


DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

async def assistant_executor(request: Dict) -> OutputModel:
        """
        Function for executing an assistant based on the provided assistant ID and prompt.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If there's an error processing the request.
        """
        try:
            # Convert the request dictionary to a JSON string
            formatted_json = json.dumps(request)
            log.info(f"Received request body as JSON: {formatted_json}")

            execution_request = ExecutionRequest.model_validate_json(formatted_json)
            log.info(f"Parsed JSON data successfully: {execution_request}")
        except json.JSONDecodeError as e:
            log.error(f"Failed to decode JSON: {str(e)}")
            raise HTTPException(status_code=400, detail="Invalid JSON input")

        try:
            client = ICAClient()

            llm_response = await asyncio.to_thread(
                client.prompt_flow,
                assistant_id=execution_request.assistant_id,
                prompt=execution_request.prompt,
            )
            log.info(f"LLM response: {llm_response}")

            response_message = ResponseMessageModel(message=llm_response.strip(), type="text")
            output_model = OutputModel(invocationId=str(uuid4()), response=[response_message])

            return output_model

        except Exception as e:
            log.error(f"Failed to process the request: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

