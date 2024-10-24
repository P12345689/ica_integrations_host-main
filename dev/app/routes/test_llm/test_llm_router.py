# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Test ica_container_host returns back input parameters + llm output using ICAClient
"""

import json
import logging
from uuid import uuid4

from fastapi import FastAPI, Request
from libica import ICAClient

log = logging.getLogger(__name__)


def add_custom_routes(app: FastAPI):
    @app.api_route("/test_llm/invoke", methods=["POST"])
    async def test_llm(request: Request):
        # get the type of request
        request_type = request.method
        log.debug(f"Received {request_type}")

        # get the data
        try:
            data = await request.json()
        except json.JSONDecodeError:
            data = await request.form()

        # format the curl command
        curl_cmd = f"curl -X {request_type} {request.url}"
        if data:
            curl_cmd += f" -d '{json.dumps(data)}'"

        # instantiate the LLM client and get the response if it's a POST request
        llm_response = {}
        if request_type == "POST":
            model_id = data.get("model")
            prompt = data.get("prompt")
            if model_id and prompt:
                consulting_assistants_model = ICAClient()
                llm_response = consulting_assistants_model.prompt_flow(model_id_or_name=model_id, prompt=prompt)

        # format the result
        formatted_result = {
            "requestType": request_type,
            "requestData": data,
            "curlCommand": curl_cmd,
            "llmResponse": llm_response,
        }

        invocation_id = str(uuid4())  # Generate a unique invocation ID

        response = {
            "status": "success",
            "invocationId": invocation_id,
            "response": [{"message": json.dumps(formatted_result), "type": "text"}],
        }

        return response
