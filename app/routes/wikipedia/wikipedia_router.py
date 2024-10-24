# -*- coding: utf-8 -*-
"""
Authors: Mihai Criveti
Description: This module provides an integration with the Wikipedia API for searching and retrieving article or summaries.

The main functionality includes:
- Validating input data using Pydantic models.
- Making asynchronous API calls to search Wikipedia and retrieve article summaries or the full article.
- Handling errors and providing informative responses to the user.
- Using Jinja2 templates for formatting the response.

Note: these are not LLM generated summaries, just what wikipedia defines as the abstract.

The module uses FastAPI for handling HTTP requests, Pydantic for input validation and output structuring,
and Jinja2 for templating the responses.

Example usage:
    # Make a POST request to the /wikipedia/invoke endpoint with the following JSON payload:
    {
        "search_string": "Python programming",
        "results_type": "summary"
    }
"""

import logging
from enum import Enum
from typing import Any, Dict
from uuid import uuid4

import httpx
from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel, Field

# Configuration Management
from .config import Settings

# Settings from pydantic
settings = Settings()

# Configure logging
log = logging.getLogger(__name__)

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/wikipedia/templates"))


class ResultsType(str, Enum):
    summary = "summary"
    full = "full"


class WikipediaSearchInput(BaseModel):
    search_string: str = Field(..., description="The phrase to search for on Wikipedia.")
    results_type: ResultsType = Field(
        default=ResultsType.summary,
        description="Type of results: summary for abstract, full for full page.",
    )
    # TODO: use field and pick from LLM list..
    llm: str = ""


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str
    response: list[ResponseMessageModel]
    invocationId: str  # noqa: N815


async def search_wikipedia(search_input: WikipediaSearchInput) -> Dict[str, Any]:
    """
    Asynchronously searches Wikipedia based on the specified input parameters and returns
    formatted response data.

    This function first performs a search query to identify relevant Wikipedia pages. If the
    search results include disambiguation pages, it provides a list of potential relevant topics.
    If a specific page is identified, it fetches a summary or the full content depending on
    the `results_type` specified in `search_input`.

    Args:
        search_input (WikipediaSearchInput): An instance of WikipediaSearchInput containing
                                             the search string and the desired type of results
                                             ('summary' or 'full').

    Returns:
        Dict[str, Any]: A dictionary containing the status of the operation and the response.
                        The response may include text and/or an image URL. The text includes
                        the content fetched from Wikipedia along with a source URL, and if
                        available, an image URL associated with the page.

    Raises:
        httpx.HTTPError: If there is a problem with the network request.
        json.JSONDecodeError: If the response cannot be decoded from JSON.
        Exception: For other unforeseen errors that may occur during processing.
    """
    async with httpx.AsyncClient() as client:
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "utf8": 1,
            "srlimit": 5,
            "srsearch": search_input.search_string,
        }
        response = await client.get(settings.wiki_api_url, params=params)
        log.debug(f"Search response: {response.json()}")
        search_results = response.json().get("query", {}).get("search", [])

        if not search_results:
            return {"summary": "", "content": "", "article_url": "", "image_url": ""}

        first_result = search_results[0]
        is_disambiguation = "may refer to:" in first_result.get("snippet", "")

        if is_disambiguation:
            titles = [result["title"] for result in search_results]
            disambiguation_text = "This may refer to several topics:\n" + "\n".join(f"- {title}" for title in titles)
            return {
                "summary": disambiguation_text,
                "content": "",
                "article_url": "",
                "image_url": "",
            }

        page_id = first_result["pageid"]
        params = {
            "action": "query",
            "format": "json",
            "prop": "extracts|pageimages",
            "pageids": page_id,
            "explaintext": True,
            "exlimit": 1,
            "pithumbsize": 500,
        }

        if search_input.results_type == ResultsType.summary:
            params["exintro"] = True
        else:
            params["exsectionformat"] = "plain"
            params["exlimit"] = "max"

        response = await client.get(settings.wiki_api_url, params=params)
        log.debug(f"Page response: {response.json()}")
        page = next(iter(response.json().get("query", {}).get("pages", {}).values()))
        text = page.get("extract", "")
        page_url = f"{settings.wiki_page_url}{first_result['title'].replace(' ', '_')}"
        image_url = page.get("thumbnail", {}).get("source", "")

        return {
            "summary": text if search_input.results_type == ResultsType.summary else "",
            "content": text if search_input.results_type == ResultsType.full else "",
            "article_url": page_url,
            "image_url": image_url,
        }


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/wikipedia/invoke")
    @app.post("/system/wikipedia/retrievers/search/invoke")
    async def search(request: Request):
        """
        Handles the POST request to search Wikipedia.

        This function takes the input data from the request, validates it using Pydantic models,
        makes an asynchronous call to the Wikipedia search function, and returns a structured response.

        Args:
            request (Request): The incoming request object.

        Returns:
            OutputModel: The response model containing the status, response messages, and invocation ID.

        Raises:
            HTTPException: If there is an error processing the request or searching Wikipedia.

        Example:
            >>> import requests
            >>> url = "http://127.0.0.1:8080/wikipedia/invoke"
            >>> data = {
            ...     "search_string": "Python programming",
            ...     "results_type": "summary"
            ... }
            >>> headers = {"Content-Type": "application/json"}
            >>> response = requests.post(url, json=data, headers=headers)
            >>> response.json()
            {
                "status": "success",
                "response": [
                    {
                        "message": "Python is a high-level, general-purpose programming language...",
                        "type": "text"
                    },
                    {
                        "message": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/500px-Python-logo-notext.svg.png",
                        "type": "image"
                    }
                ],
                "invocationId": "5d6c63d2-1a88-4e68-a9f5-c37776f6e1f9"
            }
        """
        log.info(f"Received {request.method} request")

        # Create an invocation ID
        invocation_id = str(uuid4())

        try:
            # Parse JSON data from the request
            data = await request.json()

            # Validate input data using Pydantic model
            search_input = WikipediaSearchInput(**data)
            log.info(f"Search input: {search_input}")
        except Exception as e:
            log.error(f"Error parsing request data: {e}")
            raise HTTPException(status_code=400, detail="Invalid request data")

        try:
            # Conduct the Wikipedia search asynchronously
            wikipedia_response = await search_wikipedia(search_input)
            log.debug(f"Wikipedia response: {wikipedia_response}")
        except Exception as e:
            log.error(f"Error during Wikipedia search: {e}")
            raise HTTPException(status_code=500, detail="Failed to search Wikipedia")

        if not wikipedia_response["summary"] and not wikipedia_response["content"]:
            formatted_response = f"I'm sorry, but I couldn't find a Wikipedia article for \"{search_input.search_string}\". Please try searching for a different topic or keyword."
            response = OutputModel(
                status="success",
                response=[
                    ResponseMessageModel(message=formatted_response, type="text"),
                    ResponseMessageModel(message="", type="image"),
                ],
                invocationId=invocation_id,
            )
        else:
            # Format the response using a Jinja2 template
            template = template_env.get_template("wikipedia_response.jinja")
            formatted_response = template.render(
                summary=wikipedia_response.get("summary", ""),
                content=wikipedia_response.get("content", ""),
                search_string=search_input.search_string,
                article_url=wikipedia_response.get("article_url", ""),
                image_url=wikipedia_response.get("image_url", ""),
                results_type=search_input.results_type,
            )
            log.debug(f"Formatted response: {formatted_response}")
            response = OutputModel(
                status="success",
                response=[
                    ResponseMessageModel(message=formatted_response, type="text"),
                    ResponseMessageModel(message=wikipedia_response.get("image_url", ""), type="image"),
                ],
                invocationId=invocation_id,
            )
            log.debug(f"Final response: {response}")

        return response
