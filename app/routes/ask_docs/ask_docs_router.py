# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Document collection integration router.

This module provides routes for retrieving document collections and asking questions about documents.

Example:
    >>> from fastapi import FastAPI
    >>> app = FastAPI()
    >>> add_custom_routes(app)
"""

import asyncio
import logging
import os
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from jinja2 import Environment, FileSystemLoader
from libica import ICAClient
from pydantic import BaseModel, Field

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # Set to DEBUG for more verbose logging

DEFAULT_MODEL = os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3 8B Instruct")
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", "4"))

# Load Jinja2 environment
template_env = Environment(loader=FileSystemLoader("app/routes/ask_docs/templates"))


class CollectionInputModel(BaseModel):
    """Model to validate input data for collection retrieval and querying."""

    collection_ids: Optional[List[str]] = Field(default=None, description="List of collection IDs to query")
    document_names: Optional[List[str]] = Field(
        default=None,
        description="List of document names to query within the collections",
    )
    query: str = Field(..., description="The query to ask about the documents")
    refresh: Optional[bool] = Field(default=False, description="Whether to refresh the collections data")


class CollectionModel(BaseModel):
    """Model to structure individual collection data."""

    id: str = Field(alias="_id")
    createdAt: str
    updatedAt: str
    teamId: str
    userEmail: str
    userName: str
    documentNames: List[str]
    visibility: str
    collectionName: str
    status: str
    tags: List[str]
    roles: List[str]

    class Config:
        """Configuration settings for the CollectionModel."""

        populate_by_name = True

    def __init__(self, **data):
        super().__init__(**data)
        if "_id" in data:
            self.id = data["_id"]
        log.debug(f"CollectionModel initialized with id: {self.id}")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]


def get_collections(refresh: bool = False) -> List[CollectionModel]:
    """
    Retrieve document collections.

    Args:
        refresh (bool): Whether to refresh the collections data. Defaults to False.

    Returns:
        List[CollectionModel]: List of document collections.

    Example:
        >>> collections = get_collections(refresh=True)
        >>> len(collections) > 0
        True
    """
    client = ICAClient()
    collections_data = client.get_collections(refresh_data=refresh)
    log.debug(f"Raw collections data: {collections_data}")
    collections = [CollectionModel(**collection) for collection in collections_data.get("collections", [])]
    log.debug(f"Processed collections: {collections}")
    return collections


def add_custom_routes(app: FastAPI) -> None:
    """Adds custom routes to the FastAPI application for agent invocation and result retrieval."""

    @app.post("/system/docs/retrievers/get_collections/invoke")
    async def get_collections_route(request: Request) -> OutputModel:
        """
        Handle POST requests to retrieve document collections.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If an error occurs during processing.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            refresh = data.get("refresh", False)
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            with ThreadPoolExecutor(max_workers=DEFAULT_MAX_THREADS) as executor:
                collections_future = executor.submit(get_collections, refresh)
                collections = collections_future.result()

            response_template = template_env.get_template("collections_response.jinja")
            rendered_response = response_template.render(collections=collections)

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error processing request: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal server error")

    @app.post("/experience/docs/ask_docs/invoke")
    async def ask_docs(request: Request) -> OutputModel:
        """
        Handle POST requests to ask questions about documents in collections.

        Args:
            request (Request): The request object containing the input data.

        Returns:
            OutputModel: The structured output response.

        Raises:
            HTTPException: If the input is invalid or an error occurs during processing.
        """
        invocation_id = str(uuid4())

        try:
            data = await request.json()
            input_data = CollectionInputModel(**data)
            log.debug(f"Input data: {input_data}")
        except Exception as e:
            log.error(f"Invalid input: {str(e)}")
            raise HTTPException(status_code=422, detail=str(e))

        try:
            client = ICAClient()
            responses = []

            collections = get_collections(refresh=input_data.refresh)
            log.debug(f"Retrieved collections: {collections}")
            collection_dict = {c.id: c for c in collections}
            log.debug(f"Collection dictionary: {collection_dict}")

            if input_data.collection_ids:
                for collection_id in input_data.collection_ids:
                    log.debug(f"Processing collection ID: {collection_id}")
                    collection = collection_dict.get(collection_id)
                    if not collection:
                        log.warning(f"Collection with ID {collection_id} not found")
                        continue

                    log.debug(f"Found collection: {collection}")
                    # Use all documents if none specified, otherwise use the specified ones
                    doc_names = input_data.document_names or collection.documentNames
                    log.debug(f"Document names for collection {collection_id}: {doc_names}")

                    # Render the prompt template
                    prompt_template = template_env.get_template("prompt_template.jinja")
                    rendered_prompt = prompt_template.render(query=input_data.query, document_names=doc_names)
                    log.debug(f"Rendered prompt: {rendered_prompt}")

                    response = await asyncio.to_thread(
                        client.prompt_flow,
                        collection_id=collection_id,
                        document_names=doc_names,
                        prompt=rendered_prompt,
                    )
                    log.debug(f"Response from prompt_flow: {response}")
                    responses.append(response)

            response_template = template_env.get_template("docs_response.jinja")
            rendered_response = response_template.render(responses=responses, query=input_data.query)
            log.debug(f"Rendered response: {rendered_response}")

            response_message = ResponseMessageModel(message=rendered_response)
            return OutputModel(invocationId=invocation_id, response=[response_message])
        except Exception as e:
            log.error(f"Error processing request: {str(e)}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")
