# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Streaming API
"""

import asyncio
import json
import logging
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field, ValidationError
from starlette.responses import StreamingResponse

app = FastAPI()
log = logging.getLogger(__name__)


class InputModel(BaseModel):
    """Model for incoming request data to specify delay and filename."""

    delay: float = Field(default=0.1, gt=0, description="Delay between messages in seconds.")
    filename: str = Field(default="tox.ini", description="File name to stream line by line.")


class OutputModel(BaseModel):
    """Output format for streamed data."""

    status: str = Field(default="success")
    invocationId: str
    event_id: str
    is_final_event: bool
    message: str
    type: str = Field(default="text")


async def file_line_streamer(filename: str, delay: float, invocation_id: str) -> asyncio.streams.StreamReader:
    """Stream a file line by line with a delay."""
    try:
        with open(filename, "r") as file:
            event_id = 0
            for line in file:
                event_id += 1
                is_final_event = False

                # Here we are keeping the newline in the `message` itself
                formatted_response = json.dumps(
                    {
                        "status": "success",
                        "invocationId": invocation_id,
                        "event_id": str(event_id),
                        "is_final_event": is_final_event,
                        "response": [
                            {
                                "message": line,  # `line` includes the newline character at the end if it was there in the file
                                "type": "text",
                            }
                        ],
                    }
                )
                yield formatted_response + "\n"  # Ensuring each JSON object is separated by a newline in the stream
                await asyncio.sleep(delay)

            # Send a final event to indicate the end of the stream
            event_id += 1
            is_final_event = True
            formatted_response = json.dumps(
                {
                    "status": "success",
                    "invocationId": invocation_id,
                    "event_id": str(event_id),
                    "is_final_event": is_final_event,
                    "response": [],
                }
            )
            yield formatted_response + "\n"
    except FileNotFoundError:
        yield json.dumps({"status": "error", "message": "File not found"}) + "\n"


def add_custom_routes(app: FastAPI) -> None:
    @app.api_route("/streaming_test/invoke", methods=["POST"])
    async def streaming_test(request: Request):
        """Handle POST requests to the invoke endpoint and stream a file line by line."""
        try:
            data = await request.json()
            input_data = InputModel(**data)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            raise HTTPException(status_code=422, detail=json.loads(e.json()))

        invocation_id = str(uuid4())  # Generate once per request
        response = StreamingResponse(
            file_line_streamer(input_data.filename, input_data.delay, invocation_id),
            media_type="application/json",
        )
        return response
