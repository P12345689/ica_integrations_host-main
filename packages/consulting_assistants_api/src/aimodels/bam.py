# -*- coding: utf-8 -*-
"""
LIBICA - IBM Consulting Assistants Extensions API - BAM APIs.

Description: base library supporting BAM for IBM Consulting Assistants SDK

Authors: Mihai Criveti

Example:
    >>> import os
    >>> from aimodels import BAMClient
    >>> bam_token = os.getenv("ASSISTANTS_BAM_TOKEN")
    >>> client = BAMClient(bam_token)
    >>> response = client.post_request(input_text="What is OpenShift in 1 sentence?")
    >>> type(response)
    <class 'str'>
"""

from __future__ import annotations

import logging
from typing import Any, Dict

import httpx
import requests

# --------------------------------------------------------------------
# Initialize logging
# --------------------------------------------------------------------

log = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------


class BAMClient:
    """
    A client to interact with the BAM API.

    Attributes:
        api_key (str): Your API key for the BAM API.
        base_url (str): Base URL for the BAM API.
    """

    def __init__(
        self,
        api_key,
        base_url="https://bam-api.res.ibm.com/v2/text/generation?version=2024-03-19",
    ):
        """
        Initialize the BAMClient with necessary authorization and base URL.

        Args:
            api_key (str): Your API key for the BAM API.
            base_url (str): Base URL for the BAM API. Defaults to the standard production URL.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": f"Bearer {api_key}",
        }

    def post_request(
        self,
        model_id: str = "meta-llama/llama-3-70b-instruct",
        input_text: str = "",
        parameters: Dict[str, Any] = None,
    ) -> str:
        """
        Send a POST request to the API with the specified parameters.

        Args:
            model_id (str): The model identifier. Default is 'meta-llama/llama-3-70b-instruct'.
            input_text (str): The input text for the model.
            parameters (dict, optional): Additional parameters for the model, such as temperature and max_new_tokens.
                If not provided, defaults to {'temperature': 0.7, 'max_new_tokens': 200}.

        Returns:
            str: The string response from the BAM API, extracting ["results"][0]["generated_text"]

        Examples:
            >>> import os
            >>> from aimodels import BAMClient
            >>> bam_token = os.getenv("ASSISTANTS_BAM_TOKEN")
            >>> client = BAMClient(bam_token)
            >>> response = client.post_request(input_text="What is OpenShift?")
            >>> type(response)
            <class 'str'>
        """
        try:
            if parameters is None:
                parameters = {"temperature": 0.7, "max_new_tokens": 200}
            data = {"model_id": model_id, "input": input_text, "parameters": parameters}

            log.debug(f"Calling BAM with {data}")

            response = requests.post(self.base_url, headers=self.headers, json=data, timeout=100)
            try:
                response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
            except requests.exceptions.HTTPError as e:
                log.error(f"HTTP error occurred: {e}")
                return ""
            except requests.exceptions.RequestException as e:
                log.error(f"Request to BAM API failed: {e}")
                return ""
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

            response_json = response.json()
            generated_text = response_json.get("results", [{}])[0].get("generated_text", "")
            if not generated_text:
                log.error("No generated text found in the BAM response.")
                return ""
            return generated_text
        except Exception as e:
            log.error(f"An error occurred: {e}")
            return ""

    async def post_request_async(
        self,
        model_id: str = "meta-llama/llama-3-70b-instruct",
        input_text: str = "",
        parameters: Dict[str, Any] = None,
    ) -> str:
        """
        Send an asynchronous POST request to the API with the specified parameters.

        Args:
            model_id (str): The model identifier. Default is 'meta-llama/llama-3-70b-instruct'.
            input_text (str): The input text for the model.
            parameters (dict, optional): Additional parameters for the model, such as temperature and max_new_tokens.
                If not provided, defaults to {'temperature': 0.7, 'max_new_tokens': 200}.

        Returns:
            str: The string response from the BAM API, extracting ["results"][0]["generated_text"]

        Examples:
            >>> import os
            >>> import asyncio  # Import asyncio to use asyncio.run
            >>> from aimodels import BAMClient
            >>> bam_token = os.getenv("ASSISTANTS_BAM_TOKEN")
            >>> client = BAMClient(bam_token)
            >>> async def get_response():
            ...     response = await client.post_request_async(input_text="What is OpenShift in 1 sentence?")
            ...     return response
            >>> response = asyncio.run(get_response())  # Wrap inside asyncio.run as doctest does not support async
            >>> type(response)
            <class 'str'>
        """
        try:
            if parameters is None:
                parameters = {"temperature": 0.7, "max_new_tokens": 200}
            data = {"model_id": model_id, "input": input_text, "parameters": parameters}

            log.debug(f"Calling BAM with {data}")

            async with httpx.AsyncClient() as client:
                response = await client.post(self.base_url, headers=self.headers, json=data, timeout=100)
                try:
                    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
                except httpx.HTTPStatusError as e:
                    log.error(f"HTTP error occurred: {e}")
                    return ""
                except httpx.RequestError as e:
                    log.error(f"Request to BAM API failed: {e}")
                    return ""

                response_json = response.json()
                generated_text = response_json.get("results", [{}])[0].get("generated_text", "")
                if not generated_text:
                    log.error("No generated text found in the BAM response.")
                    return ""
                return generated_text

        except Exception as e:
            log.error(f"An error occurred: {e}")
            return ""
