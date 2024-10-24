# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Test LLM returns back input parameters + llm output using ICAClient
"""

import logging
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel

from .webex import download_transcript, summarize_call

log = logging.getLogger(__name__)


class WebexSummarizationRequest(BaseModel):
    bearer_token: str
    from_date: str
    to_date: str
    max_results: int = 10  # Default to 10 if not provided


def add_custom_routes(app: FastAPI):
    @app.api_route(methods=["POST"], path="/webex_summarizer/invoke")
    async def test_llm(request: Request):
        # Parse the JSON body using the Pydantic model
        body = await request.json()
        data = WebexSummarizationRequest(**body)

        log.debug(f"Received POST request with data: {data}")

        if not data.bearer_token:
            raise HTTPException(status_code=400, detail="Bearer token is required.")

        transcript = download_transcript(data.bearer_token, data.from_date, data.to_date, data.max_results)
        # Generate a unique invocation ID for structured response
        invocation_id = str(uuid4())

        if transcript:
            log.debug(f"Transcript received: {transcript}")
            summarized_data = summarize_call(transcript)
        else:
            return {
                "status": "Error",
                "invocationId": invocation_id,
                "message": "Failed to download or process the transcript.",
                "type": "text",
            }

        response = {
            "status": "success",
            "invocationId": invocation_id,
            "response": [{"message": summarized_data, "type": "text"}],
        }

        return response
