# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Document collection tool for retrieving collections and querying documents.

This module provides tools that use the document collection functionality from the main router.
"""

import json
from typing import Union

from langchain.agents import tool

# Import the functions from the main router
from app.routes.ask_docs.ask_docs_router import ICAClient, get_collections


@tool
def get_collections_tool(refresh: Union[bool, str] = False) -> str:
    """
    Tool for getting the list of available document collections.

    Args:
        refresh (Union[bool, str]): Whether to refresh the collections data.
                                    Can be a boolean or a string 'true'/'false'. Defaults to False.

    Returns:
        str: A formatted string containing information about the available collections.

    Example:
        >>> get_collections_tool(refresh=True)
        'Available document collections: ...'
        >>> get_collections_tool(refresh='true')
        'Available document collections: ...'
    """
    # Convert string input to boolean if necessary
    if isinstance(refresh, str):
        refresh = refresh.lower() == "true"

    # Your existing code to get collections goes here
    collections = get_collections(refresh)

    if not collections:
        return "No document collections found."

    result = "Available document collections:\n\n"
    for collection in collections:
        result += f"Name: {collection.collectionName}\n"
        result += f"ID: {collection.id}\n"
        result += f"Created By: {collection.userName} ({collection.userEmail})\n"
        result += f"Visibility: {collection.visibility}\n"
        result += f"Documents: {', '.join(collection.documentNames)}\n\n"

    return result


@tool
def query_documents_tool(input_str: str) -> str:
    """
    Tool for querying documents in specified collections.

    Args:
        input_str (str): A JSON string containing the query parameters.
            Required keys:
            - collection_ids (List[str]): List of collection IDs to query.
            - query (str): The query to ask about the documents.
            Optional key:
            - document_names (Optional[List[str]]): List of document names to query within the collections.

    Returns:
        str: The response from querying the documents.

    Example:
        >>> query_documents_tool('{"collection_ids": ["id1", "id2"], "query": "What is AI?", "document_names": ["doc1.pdf"]}')
        'Response from querying documents: ...'
    """
    try:
        input_data = json.loads(input_str)
    except json.JSONDecodeError:
        return "Error: Invalid JSON input. Please provide a valid JSON string."

    collection_ids = input_data.get("collection_ids")
    query = input_data.get("query")
    document_names = input_data.get("document_names")

    if not collection_ids or not query:
        return "Error: Both 'collection_ids' and 'query' are required in the input."

    if not isinstance(collection_ids, list):
        return "Error: 'collection_ids' must be a list of strings."

    client = ICAClient()
    responses = []

    for collection_id in collection_ids:
        response = client.prompt_flow(collection_id=collection_id, document_names=document_names, prompt=query)
        responses.append(response)

    return "\n\n".join(responses)
