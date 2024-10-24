# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: IBM Watson Discovery V2 Integration Router

This module provides FastAPI routes for querying IBM Watson Discovery V2.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)

# Business rules

1. **Discovery Query Input Validation**: The `DiscoveryQueryInputModel` class defines the structure of the input data for Discovery queries, which includes a required `query` string, an optional `collection_ids` list of strings, and an optional `project_id` string.

2. **Response Message Structure**: The `ResponseMessageModel` class defines the structure of the response message, which includes a required `message` string and an optional `type` string with a default value of "text".

3. **Output Response Structure**: The `OutputModel` class defines the structure of the output response, which includes a required `status` string with a default value of "success", a required `invocationId` string, and a required `response` list of `ResponseMessageModel` objects.

4. **Discovery Client Initialization**: The `init_discovery_client` function initializes a Watson Discovery V2 client with an authenticator, version, and service URL.

5. **Query Discovery**: The `query_discovery` function handles POST requests to query Watson Discovery, which includes:
        * Validating the input data using the `DiscoveryQueryInputModel`.
        * Executing the query using the `discovery_client.query` method.
        * Rendering the response using a Jinja template.
        * Returning an `OutputModel` object with the response message.

6. **Ask Discovery**: The `ask_discovery` function handles POST requests to ask questions based on Discovery results, which includes:
        * Validating the input data using the `DiscoveryQueryInputModel`.
        * Executing the query using the `discovery_client.query` method.
        * Rendering the response using a Jinja template.
        * Returning an `OutputModel` object with the response message.

7. **Error Handling**: The code includes error handling for invalid input data, Discovery query failures, and Ask Discovery process failures, which raises HTTP exceptions with error messages.

8. **Thread Pool Executor**: The code uses a `ThreadPoolExecutor` to execute the query and process functions asynchronously, with a maximum number of threads defined by `DEFAULT_MAX_THREADS`.

9. **FastAPI Routing**: The code defines two routes for the FastAPI application: `/system/discovery/retrievers/query/invoke` for querying Watson Discovery and `/experience/discovery/ask_discovery/invoke` for asking questions based on Discovery results.
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import DiscoveryV2
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

# Environment variables and constants
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")

DISCOVERY_API_KEY = os.getenv("WATSON_DISCOVERY_API_KEY")
DISCOVERY_URL = os.getenv("WATSON_DISCOVERY_URL")
DISCOVERY_PROJECT_ID = os.getenv("WATSON_DISCOVERY_PROJECT_ID")
DISCOVERY_VERSION = "2023-03-31"

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/discovery/templates"))


class DiscoveryQueryInputModel(BaseModel):
    """Model to validate input data for Discovery queries."""

    query: str = Field(..., description="The query string to search for in Discovery")
    collection_ids: Optional[List[str]] = Field(None, description="List of collection IDs to search in")
    project_id: Optional[str] = Field(None, description="Project ID to search in")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def init_discovery_client() -> DiscoveryV2:
    """Initialize and return a Watson Discovery V2 client."""
    try:
        authenticator = IAMAuthenticator(DISCOVERY_API_KEY)
        discovery = DiscoveryV2(version=DISCOVERY_VERSION, authenticator=authenticator)
        discovery.set_service_url(DISCOVERY_URL)
        return discovery
    except Exception as e:
        log.error(f"Failed to initialize Discovery client: {str(e)}")
        raise


def add_custom_routes(app: FastAPI):
    if DISCOVERY_API_KEY and DISCOVERY_URL and DISCOVERY_PROJECT_ID:
        discovery_client = init_discovery_client()
    else:
        log.error("Need to set DISCOVERY_API_KEY, DISCOVERY_URL and DISCOVERY_PROJECT_ID")

    @app.post("/system/discovery/retrievers/query/invoke")
    async def query_discovery(request: Request) -> OutputModel:
        """
        Handle POST requests to query Watson Discovery.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or the query fails.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = DiscoveryQueryInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        async def execute_query():
            try:
                response = discovery_client.query(
                    project_id=input_data.project_id or DISCOVERY_PROJECT_ID,
                    collection_ids=input_data.collection_ids,
                    query=input_data.query,
                ).get_result()
                return response
            except Exception as e:
                log.error(f"Discovery query failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Discovery query failed: {str(e)}")

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            query_result_future = executor.submit(asyncio.run, execute_query())
            query_result = query_result_future.result()

        response_template = template_env.get_template("discovery_response.jinja")
        rendered_response = response_template.render(result=query_result)

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/experience/discovery/ask_discovery/invoke")
    async def ask_discovery(request: Request) -> OutputModel:
        """
        Handle POST requests to ask questions based on Discovery results.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or the process fails.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = DiscoveryQueryInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        async def process_query():
            try:
                # Query Discovery
                discovery_response = discovery_client.query(
                    project_id=input_data.project_id or DISCOVERY_PROJECT_ID,
                    collection_ids=input_data.collection_ids,
                    query=input_data.query,
                ).get_result()

                # Prepare prompt
                prompt_template = template_env.get_template("discovery_prompt.jinja")
                prompt = prompt_template.render(query=input_data.query, discovery_results=discovery_response)

                # Call LLM
                client = ICAClient()
                llm_response = await asyncio.to_thread(
                    client.prompt_flow, model_id_or_name=DEFAULT_MODEL, prompt=prompt
                )

                return llm_response
            except Exception as e:
                log.error(f"Ask Discovery process failed: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Ask Discovery process failed: {str(e)}")

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            result_future = executor.submit(asyncio.run, process_query())
            result = result_future.result()

        response_template = template_env.get_template("discovery_llm_response.jinja")
        rendered_response = response_template.render(result=result)

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])


if __name__ == "__main__":
    import uvicorn

    app = FastAPI()
    add_custom_routes(app)
    uvicorn.run(app, host="0.0.0.0", port=8000)
