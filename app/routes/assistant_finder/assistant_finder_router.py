# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Find the right assistants based on provided input description using cosine similarity and a language model.

This module defines an integration endpoint to find the most suitable assistants based on a given description.
It uses cosine similarity to rank assistants and a language model to finalize the recommendation.

Input:
- Input Description
- Optional Tags (comma-separated)
- Optional Roles (comma-separated)

Output:
- A rendered response containing the recommended assistant and the top X assistants (up to 10)
"""

import json
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Literal, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field, ValidationError
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing_extensions import Annotated

# Set up logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/assistant_finder/templates"))
log.debug("Jinja2 environment initialized with template directory.")


class InputModel(BaseModel):
    """Model to validate input data."""

    description: str
    tags: Optional[str] = None  # Comma-separated tags
    roles: Optional[str] = None  # Comma-separated roles


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: Literal["text", "image"]


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: Annotated[List[ResponseMessageModel], Field(min_length=1)]


def calculate_similarity(assistants: List[Dict[str, Any]], description: str) -> List[Dict[str, Any]]:
    """
    Calculate the cosine similarity between a list of assistant descriptions and a given description.

    Args:
        assistants (List[Dict[str, Any]]): List of dictionaries representing assistants.
        description (str): Input description to compare against.

    Returns:
        List[Dict[str, Any]]: Assistants sorted by similarity in descending order.

    Example:
        >>> test_assistants = [{'id': '1', 'description': 'Data analysis'}, {'id': '2', 'description': 'Web development'}]
        >>> test_description = 'Data science'
        >>> calculate_similarity(test_assistants, test_description) # doctest: +ELLIPSIS
        [{'id': ..., 'description': ..., 'similarity': ..., 'match_percentage': ...}]
    """
    log.debug("Calculating cosine similarity")
    descriptions = [assistant["description"] for assistant in assistants]
    descriptions.insert(0, description)  # Include the input description as the first element

    # Vectorize the descriptions
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(descriptions)
    vectors_array = vectors.toarray()

    log.debug(f"TF-IDF Vectors: {vectors_array}")

    # Calculate cosine similarity
    cosine_similarities = cosine_similarity([vectors_array[0]], vectors_array[1:])[0]
    log.debug(f"Cosine Similarities: {cosine_similarities}")

    # Attach similarity scores to assistants
    for idx, assistant in enumerate(assistants):
        assistant["similarity"] = cosine_similarities[idx]
        assistant["match_percentage"] = round(cosine_similarities[idx] * 100, 2)
        log.debug(f"Assistant ID {assistant['id']} similarity: {assistant['similarity']}, match_percentage: {assistant['match_percentage']}%")

    # Sort assistants by similarity score in descending order
    return sorted(assistants, key=lambda x: x["similarity"], reverse=True)


def add_custom_routes(app: FastAPI) -> None:
    """
    Add custom routes to the FastAPI app.
    """

    @app.api_route("/assistant_finder/invoke", methods=["POST"])
    async def invoke(request: Request) -> OutputModel:
        """
        Handles POST requests to recommend assistants based on description similarity.

        Args:
            request (Request): The incoming HTTP request with JSON payload.

        Returns:
            OutputModel: The structured output response containing the assistant recommendations.

        Raises:
            HTTPException: If the JSON is invalid or if validation fails.

        Example:
            >>> invoke({'description': 'Data science'})
            {'status': 'success', ...}
        """
        invocation_id = str(uuid4())  # Generate a unique invocation ID
        log.info(f"Invocation ID: {invocation_id}")
        request_type = request.method
        log.debug(f"Received {request_type} request")

        try:
            data = await request.json()
            input_data = InputModel(**data)
            log.debug(f"Input data: {data}")
        except json.JSONDecodeError:
            log.error("Invalid JSON received")
            raise HTTPException(status_code=400, detail="Invalid JSON")
        except ValidationError as e:
            log.error(f"Validation error: {e.errors()}")
            raise HTTPException(status_code=422, detail=e.errors())

        consulting_assistants_model = ICAClient()
        log.info("ICAClient instantiated")
        tags = input_data.tags.split(",") if input_data.tags else []
        roles = input_data.roles.split(",") if input_data.roles else []
        log.debug(f"Parsed tags: {tags}")
        log.debug(f"Parsed roles: {roles}")

        with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
            assistants_list_future = executor.submit(
                consulting_assistants_model.get_assistants,
                tags=tags,
                roles=roles,
                refresh_data=True,
            )
            assistants_list = assistants_list_future.result()
            log.info(f"Retrieved {len(assistants_list)} assistants from ICAClient")

            similar_assistants = calculate_similarity(assistants_list, input_data.description)[:10]
            num_similar_assistants = len(similar_assistants)
            log.info(f"Top {num_similar_assistants} similar assistants identified")

            template = template_env.get_template("prompt_template.jinja")
            rendered_input = template.render(
                similar_assistants=similar_assistants,
                input_description=input_data.description,
            )
            log.info(f"Rendered input for LLM: {rendered_input}")

            llm_response_future = executor.submit(
                consulting_assistants_model.prompt_flow,
                model_id_or_name=DEFAULT_MODEL,
                prompt=rendered_input,
            )
            llm_response = llm_response_future.result()
            log.info(f"LLM response: {llm_response}")

        if llm_response is None:
            llm_response = "No response from LLM"
            log.warning("No response from LLM")

        template = template_env.get_template("response_template.jinja")
        rendered_response = template.render(
            llm_response=llm_response,
            assistants=similar_assistants,
            num_similar_assistants=num_similar_assistants,
        )
        log.debug(f"Rendered response: {rendered_response}")

        response_dict = ResponseMessageModel(message=rendered_response, type="text")
        response_data = OutputModel(invocationId=invocation_id, response=[response_dict])
        log.info("Response data prepared")

        return response_data
