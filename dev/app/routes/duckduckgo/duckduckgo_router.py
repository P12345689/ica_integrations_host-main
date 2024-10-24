# -*- coding: utf-8 -*-
import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Dict
from uuid import uuid4

from fastapi import FastAPI, Request
from jinja2 import Environment, FileSystemLoader
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.tools import DuckDuckGoSearchResults
# langchain import
from langchain_consultingassistants import ChatConsultingAssistants
from pydantic import BaseModel

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("dev/app/routes/duckduckgo/templates"))

DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")


class DuckDuckGoSearchRequest(BaseModel):
    input: Dict[str, str]


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str
    response: list[ResponseMessageModel]
    invocationId: str


def add_custom_routes(app: FastAPI):
    @app.post("/duckduckgo/invoke")
    async def duck_search(request: Request):
        """
        Handles the POST request to perform a DuckDuckGo Search and generate a succinct answer.

        This function takes the input data from the request, validates it using Pydantic models,
        makes an asynchronous call to the DuckDuckGo Search API, generates a succinct answer based on
        the search results using LangChain and ChatConsultingAssistants, and returns a structured response.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The response model containing the status, response messages, and invocation ID.

        Raises:
            HTTPException: If there is an error processing the request or performing the DuckDuckGo Search.

        Example:
            >>> import requests
            >>> url = "http://localhost:8080/duckduckgo/invoke"
            >>> data = {
            ...     "input": {
            ...         "query": "What is Python programming?"
            ...     }
            ...
            ... }
            >>> headers = {"Content-Type": "application/json", "Integrations-API-Key:dev-only-token"}
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
        search = DuckDuckGoSearchResults()

        # Get the model
        model = ChatConsultingAssistants(model=DEFAULT_MODEL)

        try:
            # Validate input data using Pydantic model
            data = DuckDuckGoSearchRequest(**await request.json())

            # Get the search query
            query = data.input["query"]

            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                search_result = await loop.run_in_executor(executor, search.run, query)

                # Format the query using a Jinja2 template
                query_template = template_env.get_template("duckduckgo_query.jinja")
                formatted_query = query_template.render(query=query, search_result=search_result)

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

            invocation_id = str(uuid4())

            # Format the response using a Jinja2 template
            response_template = template_env.get_template("duckduckgo_response.jinja")
            formatted_response = response_template.render(result=formatted_result)

            # Create a structured response using Pydantic model
            response = OutputModel(
                status="success",
                response=[ResponseMessageModel(message=formatted_response, type="text")],
                invocationId=invocation_id,
            )

            return response.dict()
        except Exception as e:
            invocation_id = str(uuid4())
            response = OutputModel(
                status="error",
                response=[
                    ResponseMessageModel(
                        message=f"I'm sorry but I couldn't find a response. Please try with a different query: {e}",
                        type="text",
                    )
                ],
                invocationId=invocation_id,
            )
            return response.dict()
