# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Website content retriever and text extractor

This module provides a tool for retrieving the content of a website and converting it to plain text.
It uses requests for HTTP requests and BeautifulSoup for HTML parsing.

Examples:
    >>> from retriever_website_tool import retrieve_website_content
    >>> input_json = '{"url": "https://example.com"}'
    >>> content = retrieve_website_content(input_json)
    >>> print(content)
    "This is the text content of the website..."
"""

import json
import logging
import os
from typing import Any

import requests
from bs4 import BeautifulSoup
from langchain.agents import tool
from langchain_text_splitters import TokenTextSplitter

DEFAULT_MAX_TOKENS = int(os.getenv("RETRIEVER_WEBSITE_MAX_TOKENS", 2000))

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def clean_input_json(input_str: str) -> str:
    """
    Cleans the input JSON string by removing any trailing characters after the JSON object.

    Args:
        input_str (str): The input JSON string.

    Returns:
        str: The cleaned JSON string.
    """
    try:
        # Find the end of the JSON object
        end_index = input_str.rfind("}")
        if end_index != -1:
            return input_str[: end_index + 1]
    except Exception as e:
        log.error(f"Error cleaning input JSON: {str(e)}")
    return input_str


def truncate_output(text: str) -> str:
    """
    Truncates the retriever output to fit into the LLM context.
    The maximum number of allowed tokens is set by the env variable RETRIEVER_WEBSITE_MAX_TOKENS.
    Default it will return max 2000 tokens

    Args:
    input_str (str): The input JSON string.

    Returns:
        str: The truncated text
    """
    text_splitter = TokenTextSplitter(chunk_size=DEFAULT_MAX_TOKENS, chunk_overlap=0)
    chunks = text_splitter.split_text(text)
    return chunks[0] if chunks else ""


@tool
def retrieve_website_content(input_json: Any) -> str:
    """
    Retrieves the content of a website and converts it to plain text.

    Args:
        input_json (Any): A JSON string or dictionary containing a 'url' key with the website URL.

    Returns:
        str: The plain text content of the website.

    Raises:
        ValueError: If the input JSON is invalid or missing the required 'url' key.
        requests.exceptions.RequestException: If there's an error retrieving the website content.
    """
    log.info("Entering retrieve_website_content")
    log.info(f"Received input: {input_json} as {type(input_json)}")

    # Ensure the input is a dictionary
    if isinstance(input_json, str):
        cleaned_json_str = clean_input_json(input_json)
        try:
            input_dict = json.loads(cleaned_json_str.strip())
            url = input_dict.get("url")
        except json.JSONDecodeError as e:
            url = cleaned_json_str
    elif isinstance(input_json, dict):
        input_dict = input_json
    else:
        raise ValueError(f"Invalid input format. Expected JSON string or dictionary with a 'url' key. Received {input_json}")

    # Validate the URL

    if not url:
        log.error("Missing 'url' key in input data.")
        raise ValueError("Invalid input format. Expected JSON with a 'url' key.")

    log.info(f"Retrieving content from URL: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # Break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # Drop blank lines
        text = "\n".join(chunk for chunk in chunks if chunk)

        log.info(f"Successfully retrieved and parsed content from {url}")
        return truncate_output(text)

    except requests.exceptions.HTTPError as http_error:
        log.error(f"HTTP Error: {str(http_error)}")
        match http_error.response.status_code:
            case 404:
                return "Cannot find the website you are looking for"
            case 403:
                return "Cannot access the website you are looking for"
            case _:
                return "Cannot retrieve the website content"

    except requests.exceptions.ReadTimeout as timeout_error:
        log.error(f"Time out: {str(timeout_error)}")
        return "The website took too long to respond"

    except requests.exceptions.ConnectionError as conn_error:
        log.error(f"Connection error: {str(conn_error)}")
        return "Could not connect to the website"

    except requests.exceptions.RequestException as error:
        log.error(f"Request exception: {str(error)}")
        return "Failed to retrieve the website content"

# Example usage
if __name__ == "__main__":
    response = retrieve_website_content(
        "{\"url\":\"https://techmeme.com\"}")
    print(response)