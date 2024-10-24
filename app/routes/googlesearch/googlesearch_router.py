# -*- coding: utf-8 -*-
"""
Author: Chris Hay, Mihai Criveti
Description: Google Search Integration, uses an LLM to summarize the results.

The main functionality includes:
- Validating input data using Pydantic models.
- Making asynchronous Google Search API calls using the GoogleSearchAPIWrapper.
- Generating succinct answers based on the search results using LangChain and ChatConsultingAssistants.
- Handling errors and providing informative responses to the user.
- Using Jinja2 templates for formatting the query and response.

The module uses FastAPI for handling HTTP requests, Pydantic for input validation and output structuring,
and Jinja2 for templating the query and responses.

Example usage:
    # Make a POST request to the /googlesearch/invoke endpoint with the following JSON payload:
    {
        "query": "What is Python programming?"
    }
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from uuid import uuid4

from fastapi import FastAPI, Request
from jinja2 import Environment, FileSystemLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_consultingassistants import ChatConsultingAssistants
from langchain_google_community.search import GoogleSearchAPIWrapper
from pydantic import BaseModel

log = logging.getLogger(__name__)

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/googlesearch/templates"))

DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")


class GoogleSearchRequest(BaseModel):
    query: str


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str
    response: list[ResponseMessageModel]
    invocationId: str  # noqa: N815


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/googlesearch/invoke")
    async def googlesearch_search(request: Request):
        """
        Handles the POST request to perform a Google Search and generate a succinct answer.

        This function takes the input data from the request, validates it using Pydantic models,
        makes an asynchronous call to the Google Search API, generates a succinct answer based on
        the search results using LangChain and ChatConsultingAssistants, and returns a structured response.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The response model containing the status, response messages, and invocation ID.

        Raises:
            HTTPException: If there is an error processing the request or performing the Google Search.

        Example:
            >>> import requests
            >>> url = "http://localhost:8080/googlesearch/invoke"
            >>> data = {
            ...     "query": "What is Python programming?"
            ... }
            >>> headers = {"Content-Type": "application/json"}
            >>> response = requests.post(url, json=data, headers=headers)
            >>> response.json()
            {
                "status": "success",
                "response": [
                    {
                        "message": "Python is a high-level, interpreted, general-purpose programming language.",
                        "type": "text"
                    }
                ],
                "invocationId": "92f8d7a6-f0b5-4e2a-8d2d-1e9b9f4c6e3e"
            }
        """
        log.debug(f"Received request: {request}")

        # Initialize the Google Search API wrapper
        search = GoogleSearchAPIWrapper()

        # Get the model
        model = ChatConsultingAssistants(model=DEFAULT_MODEL)

        try:
            # Validate input data using Pydantic model
            data = GoogleSearchRequest(**await request.json())

            # Get the search query
            query = data.query
            log.info(f"Search query: {query}")

            # Use ThreadPoolExecutor for running blocking tasks asynchronously
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                # Perform the Google Search
                search_result = await loop.run_in_executor(executor, search.run, query)
                log.debug(f"Search result: {search_result}")

                # Format the query using a Jinja2 template
                query_template = template_env.get_template("googlesearch_query.jinja")
                formatted_query = query_template.render(query=query, search_result=search_result)
                log.debug(f"Formatted query: {formatted_query}")

                # Set the prompt template
                prompt = PromptTemplate(
                    input_variables=["query"],
                    template=formatted_query,
                )

                # Create an LLMChain instance
                llm_chain = LLMChain(llm=model, prompt=prompt)

                # Generate the succinct answer using the LLMChain
                llm_chain_run = partial(llm_chain.run, query=query)
                formatted_result = await loop.run_in_executor(executor, llm_chain_run)
                log.debug(f"Formatted result: {formatted_result}")

            # Create an invocation ID
            invocation_id = str(uuid4())

            # Format the response using a Jinja2 template
            response_template = template_env.get_template("googlesearch_response.jinja")
            formatted_response = response_template.render(result=formatted_result)
            log.debug(f"Formatted response: {formatted_response}")

            # Create a structured response using Pydantic model
            response = OutputModel(
                status="success",
                response=[ResponseMessageModel(message=formatted_response, type="text")],
                invocationId=invocation_id,
            )
            log.info(f"Final response: {response}")

            return response.dict()

        except Exception as e:
            log.exception(f"Error invoking Google Search: {e}")
            invocation_id = str(uuid4())
            response = OutputModel(
                status="error",
                response=[
                    ResponseMessageModel(
                        message="I'm sorry but I couldn't find a response. Please try with a different query.",
                        type="text",
                    )
                ],
                invocationId=invocation_id,
            )
            return response.dict()
