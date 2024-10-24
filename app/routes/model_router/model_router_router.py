# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Intelligent Router for Prompt to Model, Document Collection and Assistant integration.

This module provides routes for routing prompts to the best model, assistant, or document collection.

This is a 'middleware' route (just like the pii_data or prompt_defender).

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)

Use Cases:
1. Select the right document collection, assistant, or model.
2. Dynamically generate the 'top 10' tools from the catalog to use in *every* single agent call.
3. Select the right agent (dynamic agent selection).
4. Dynamically inject prompt_defender or pii_data... middleware.
5. Select a list of 'gold sites' or 'collection names' to use!
- Instead of pick document collection, you could pick.. the right sites to use (top 20 sites).
- Blocklist sites like linkedin.in that don't let you use.
- Allowlist of websites
"""

import asyncio
import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
CONFIG_FILE_PATH = os.getenv("CONFIG_FILE_PATH", "app/routes/model_router/config/prompt_router_config.json")

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/model_router/templates"))


class PromptInputModel(BaseModel):
    """Model to validate input data for prompt routing."""

    prompt: str = Field(..., description="The prompt to be routed")
    context: Dict[str, Any] = Field(
        default={},
        description="Additional context for routing, e.g., {'preferred_type': 'model'}",
    )


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def load_configuration() -> Dict[str, Any]:
    """
    Load the configuration from the JSON file.

    Returns:
        Dict[str, Any]: The loaded configuration.

    Raises:
        FileNotFoundError: If the configuration file is not found.
        json.JSONDecodeError: If the configuration file is not valid JSON.
    """
    try:
        with open(CONFIG_FILE_PATH, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        log.error(f"Configuration file not found: {CONFIG_FILE_PATH}")
        raise
    except json.JSONDecodeError:
        log.error(f"Invalid JSON in configuration file: {CONFIG_FILE_PATH}")
        raise


def compute_cosine_similarity(text1: str, text2: str) -> float:
    """
    Compute the cosine similarity between two texts.

    Args:
        text1 (str): The first text.
        text2 (str): The second text.

    Returns:
        float: The cosine similarity score.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]


def rank_options(prompt: str, context: Dict[str, Any], options: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Rank the available options based on the prompt and context using cosine similarity.

    Args:
        prompt (str): The input prompt.
        context (Dict[str, Any]): Additional context for ranking.
        options (List[Dict[str, Any]]): List of available options.

    Returns:
        List[Dict[str, Any]]: Ranked list of options.
    """
    for option in options:
        option_text = f"{option['name']} {option['description']}"
        similarity_score = compute_cosine_similarity(prompt, option_text)

        # Consider context if available
        context_boost = 0
        if "preferred_type" in context and context["preferred_type"] == option["type"]:
            context_boost = 0.2  # Boost score if the type matches the preferred type

        option["score"] = similarity_score + context_boost

    # Sort options by score in descending order
    ranked_options = sorted(options, key=lambda x: x["score"], reverse=True)

    # Log the ranking results for debugging
    log.debug(f"Prompt: {prompt}")
    for option in ranked_options:
        log.debug(f"Option: {option['name']}, Type: {option['type']}, Score: {option['score']}")

    return ranked_options


async def route_prompt(prompt: str, context: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Route the prompt to the best option based on the configuration.

    Args:
        prompt (str): The input prompt.
        context (Dict[str, Any]): Additional context for routing.
        config (Dict[str, Any]): The loaded configuration.

    Returns:
        Dict[str, Any]: A dictionary containing the response and the selected option.
    """
    options = config.get("options", [])
    ranked_options = rank_options(prompt, context, options)

    if not ranked_options:
        raise ValueError("No valid options available for routing")

    selected_option = ranked_options[0]

    client = ICAClient()

    if selected_option["type"] == "model":
        response = await asyncio.to_thread(client.prompt_flow, model_id_or_name=selected_option["id"], prompt=prompt)
    elif selected_option["type"] == "assistant":
        # TODO: Implement assistant routing
        response = f"Assistant routing not yet implemented. Would use assistant: {selected_option['name']}"
    elif selected_option["type"] == "document_collection":
        # TODO: Implement document collection routing
        response = f"Document collection routing not yet implemented. Would use collection: {selected_option['name']}"
    else:
        raise ValueError(f"Unknown option type: {selected_option['type']}")

    return {"response": response, "selected_option": selected_option}


def add_custom_routes(app: FastAPI) -> None:
    @app.post("/experience/prompt_router/route_prompt/invoke")
    async def route_prompt_experience(request: Request) -> OutputModel:
        """
        Handle POST requests to route prompts to the best option.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or an error occurs during routing.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = PromptInputModel(**data)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            config = load_configuration()
        except Exception as e:
            log.error(f"Error loading configuration: {str(e)}")
            raise HTTPException(status_code=500, detail="Error loading configuration")

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                result_future = executor.submit(
                    asyncio.run,
                    route_prompt(input_data.prompt, input_data.context, config),
                )
                result = result_future.result()
        except Exception as e:
            log.error(f"Error routing prompt: {str(e)}")
            raise HTTPException(status_code=500, detail="Error routing prompt")

        # Render the response
        response_template = template_env.get_template("response_template.jinja")
        rendered_response = response_template.render(result=result["response"], selected_option=result["selected_option"])

        response_message = ResponseMessageModel(message=rendered_response)
        return OutputModel(invocationId=invocation_id, response=[response_message])

    @app.post("/system/prompt_router/get_configuration/invoke")
    async def get_configuration_system(request: Request) -> OutputModel:
        """
        Handle POST requests to get the current prompt router configuration.

        Args:
            request (Request): The request object.

        Returns:
            OutputModel: The structured output response containing the configuration.

        Raises:
            HTTPException: If an error occurs while loading the configuration.
        """
        invocation_id = str(uuid4())

        try:
            config = load_configuration()
        except Exception as e:
            log.error(f"Error loading configuration: {str(e)}")
            raise HTTPException(status_code=500, detail="Error loading configuration")

        response_message = ResponseMessageModel(message=json.dumps(config, indent=2))
        return OutputModel(invocationId=invocation_id, response=[response_message])
