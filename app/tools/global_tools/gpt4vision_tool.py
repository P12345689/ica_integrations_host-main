# -*- coding: utf-8 -*-
"""
Description: GPT-4 Vision API client for image-to-text transformation

This module provides a client function for calling the GPT-4 Vision API to perform image-to-text transformation.
It sends a request to the specified GPT-4 Vision API endpoint with the provided image URL and query, and returns
the response from the API.

The module uses environment variables to configure the GPT-4 Vision API endpoint URL and the maximum number of tokens
for the generated response.

Examples:
    >>> from gpt4vision_tool import call_gpt4_vision_api
    >>> input_json = '{"image": "https://example.com/image.jpg", "query": "What is in the image?"}'
    >>> response = call_gpt4_vision_api(input_json)
    >>> print(response)
    "The image shows..."
"""

import json
import logging
import os
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import urlopen

import requests
from langchain.tools import Tool

DEFAULT_MODEL = os.getenv(
    "GPT4VISION_MODEL_URL",
    "https://essentialsdalle3.openai.azure.com/openai/deployments/essentialsgpt4vision/chat/completions?api-version=2024-02-15-preview",
)
DEFAULT_MAX_TOKENS = int(os.getenv("GPT4VISION_DEFAULT_MAX_TOKENS", 500))
DEFAULT_IMAGE_FORMATS = ("image/png", "image/jpeg", "image/gif")
MAX_FILE_SIZE = int(os.getenv("GPT4VISION_MAX_FILE_SIZE", 10 * 1024 * 1024))  # 10 MB default

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def validate_image(image_url: str) -> None:
    """
    Validates the provided image URL
    - checks if the URL has a valid format (schema and network location are present)
    - checks if the URL is accessible and contains a valid image format

    raises ValueError

    """
    # perform quick URL validation
    url_parse_result = urlparse(image_url)
    if not all([url_parse_result.scheme, url_parse_result.netloc]):
        log.error(f"Malformed image URL {image_url}")
        raise ValueError("Malformed image URL")

    # check if the URL contains a valid image type
    try:
        image_response = urlopen(image_url)

        # check the returned content-type
        content_type = image_response.getheader("Content-Type", "")
        if content_type not in DEFAULT_IMAGE_FORMATS:
            log.error(f"The URL does not contain an image with a supported format. Got {content_type} but expected {DEFAULT_IMAGE_FORMATS}")
            raise ValueError(f"Unsupported image type {content_type}")

        # check the image size
        content_length = int(image_response.getheader("Content-Length", 0))
        if content_length > MAX_FILE_SIZE:
            log.error(f"File size exceeds limit. Received {content_length} but max is {MAX_FILE_SIZE}")
            raise ValueError("The image file is too large. Please try a smaller image.")

    except URLError as e:
        log.error(f"Failed to open the image URL: {str(e)}")
        raise ValueError("Cannot open the image URL")


def call_gpt4_vision_api(input_json: str) -> str:
    """
    Calls the GPT-4 Vision API to perform image-to-text transformation.

    Args:
        input_json (str): A JSON string containing 'image' (URL of the image) and 'query' (question about the image) keys.

    Returns:
        str: The content of the response from the GPT-4 Vision API.

    Raises:
        ValueError: If the input JSON is invalid or missing required keys.
        requests.exceptions.RequestException: If there's an error sending the request to the GPT-4 Vision API.
    """
    try:
        input_data = json.loads(input_json)

        # validate the image
        image_url = input_data["image"]
        if not image_url:
            log.error("Missing value for 'image' key.")
            raise ValueError("Missing value for image URL")

        validate_image(image_url)

        # validate the image query
        query = input_data["query"]
        if not query:
            log.error("Missing 'query' key in input data.")
            raise ValueError("Empty query string")

    except (json.JSONDecodeError, KeyError) as e:
        log.error(f"Error parsing input JSON: {str(e)}")
        raise ValueError("Expected JSON string with 'image' and 'query' keys.") from e

    url = DEFAULT_MODEL
    headers = {
        "api-key": os.environ["GPT4VISION_API_KEY"],
        "Content-Type": "application/json",
    }
    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": query},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": "high"},
                    },
                ],
            }
        ],
        "max_tokens": DEFAULT_MAX_TOKENS,
        "stream": False,
    }

    log.info(f"Sending request to GPT-4 Vision API: URL={url}, Headers={headers}, Payload={payload}")

    try:
        response = requests.post(url, json=payload, headers=headers)
        log.info(f"Received response from GPT-4 Vision API: Status={response.status_code}, Content={response.text}")

        response.raise_for_status()

        try:
            response_json = response.json()
            log.info(f"Parsed response JSON: {response_json}")
            return response_json["choices"][0]["message"]["content"]
        except (ValueError, KeyError) as e:
            log.error(f"Failed to parse response JSON or extract content: {str(e)}")
            raise requests.exceptions.RequestException("Failed to parse response JSON or extract content") from e

    except requests.exceptions.RequestException as e:
        log.error(f"Request to GPT-4 Vision API failed: {str(e)}")
        raise


gpt4_vision_tool = Tool(
    name="GPT-4 Vision",
    func=call_gpt4_vision_api,
    description="A tool that uses GPT-4 Vision API to analyze images. Input should be a JSON string with 'image' (URL of the image) and 'query' (question about the image) keys.",
)
