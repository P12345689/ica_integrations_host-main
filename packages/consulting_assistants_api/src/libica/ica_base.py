# -*- coding: utf-8 -*-
"""
LIBICA - IBM Consulting Assistants Extensions API - Python SDK.

Description: base library supporting the IBM Consulting Assistants API v 4.5.

Authors: Mihai Criveti

Usage examples (with doctest):

# Load libica and initialize a client
>>> from libica.ica_base import ICABase
>>> base = ICABase()
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import random
import sys
import time
from datetime import datetime, timedelta
from importlib.metadata import version
from typing import Any, Optional, Union

import requests
from libica.ica_error import ICAClientError
from libica.ica_settings import REQUESTS_TIMEOUT, Settings

# --------------------------------------------------------------------
# Initialize logging
# --------------------------------------------------------------------

log = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------
class ICABase:
    """
    API Client to interact with IBM Consulting Assistants Extensions v4.5.

    This client provides methods to call API endpoints for managing models, tags, roles, assistants, collections, chat IDs, and executing prompts.
    It supports caching for models and tags to reduce network requests.

    Examples:
        >>> ica_base = ICABase()
    """

    def __init__(self, settings: Optional[Settings] = None):
        """
        Initialize the ICABase with specific settings.

        Args:
            settings (Optional[Settings]): An instance of the Settings class with configuration for the client.
        """
        self.settings = settings or Settings()
        self.configure_logging()

    # --------------------------------------------------------------------
    # Configure debug logging
    # --------------------------------------------------------------------
    def configure_logging(self):
        """
        Configure logging based on the 'debug' environment variable from settings.

        This is sourced from the ASSISTANTS_DEBUG env. variable by the configuration module using `pydantic`.
        """
        if self.settings.assistants_debug:
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(asctime)s - %(levelname)s - %(message)s",
                stream=sys.stderr,
            )
        else:
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s - %(levelname)s - %(message)s",
                stream=sys.stderr,
            )

    # --------------------------------------------------------------------
    # Cache Functions
    # --------------------------------------------------------------------
    def cache_path(self, file_name: str) -> str:
        """
        Return cache path, after expanding home directory, if provided.

        Constructs the path to the cache file specific to a team, from:
        settings.assistants_cache_directory + sha256(settings.assistants_api_key) + file_name.

        For example, DEFAULT_CACHE_DIRECTORY/SHA256_OF_THE_API_KEY/models.json

        Will create the directory if it does not exist.

        It securely hashes the team API key (settings.assistants_api_key) using SHA256.

        Args:
            file_name (str): Name of the file.

        Returns:
            str: The full path to the cache file.

        Raises:
            ValueError: If the 'ASSISTANTS_API_KEY' is not set in settings.

        Examples:
            >>> base = ICABase()
            >>> expanded_path = base.cache_path('models.json')
            >>> print(base.cache_path('models.json'))  # doctest: +ELLIPSIS
            /tmp/.../models.json

        Notes:
            This function could also add the extension id + key to this if required, but currently only uses the ASSISTANTS_API_KEY.
        """
        if not self.settings.assistants_api_key:
            raise ValueError("ASSISTANTS_API_KEY is not set")
        team_sha256_hash = hashlib.sha256(self.settings.assistants_api_key.encode()).hexdigest()
        team_sha256_dir = f"{self.settings.assistants_cache_directory}/{team_sha256_hash}"

        # Create the directory if it does not exist
        if not os.path.exists(team_sha256_dir):
            os.makedirs(team_sha256_dir, exist_ok=True)

        team_cache_file_path = f"{team_sha256_dir}/{file_name}"

        # Expand the user's home directory (~) if present in the path
        return os.path.expanduser(team_cache_file_path)

    def is_cache_valid(self, file_name: str) -> bool:
        """
        Check if the cache file is valid based on its modification time being within the cache duration hours from the current time.

        Args:
            file_name (str): Name of the cache file.

        Returns:
            bool: True if the cache is valid, False otherwise.

        Examples:
            >>> base = ICABase()
            >>> base.is_cache_valid('/tmp/this-cache-file-does-not-exist')
            False
        """
        path = self.cache_path(file_name)
        logging.debug(f"is_cache_valid: {path}")

        if not os.path.exists(path):
            return False

        cache_time = datetime.fromtimestamp(os.path.getmtime(path))

        if datetime.now() - cache_time < timedelta(hours=self.settings.assistants_cache_duration_hours):
            return True
        return False

    def write_cache(self, file_name: str, data):
        """
        Write data to a cache file.

        Args:
            file_name (str): Name of the file.
            data (any): Data to be cached, will be stored as file_name.json (even if it's not a valid json).

        Examples:
            >>> base = ICABase()
            >>> cache_file = "ica-example-cache-file-tags.json"
            >>> data = {"name": "tag"}
            >>> base.write_cache(cache_file, data)
        """
        with open(self.cache_path(file_name), "w", encoding="utf-8") as f:
            json.dump(data, f)

    def read_cache(self, file_name: str) -> Any:
        """
        Read data from a cache file.

        Args:
            file_name (str): Name of the cache file.

        Returns:
            Any: Data retrieved from the cache file,

        Examples:
            >>> base = ICABase()
            >>> cache_file = "models.json"
            >>> try:
            ...     cached_json = base.read_cache(cache_file)
            ... except json.decoder.JSONDecodeError:
            ...     cached_json = None  # Handle the error as appropriate
        """
        with open(self.cache_path(file_name), encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.decoder.JSONDecodeError as e:
                logging.error(f"Failed to decode JSON from cache file {file_name}: {e}")
                # Handle the error as appropriate, e.g., by returning None or raising a custom exception
                return None

    # --------------------------------------------------------------------
    # Helpers: get_headers, request_wrapper, get_model_id_by_name
    # --------------------------------------------------------------------
    def get_headers(self) -> dict:
        """
        Return the common headers for making API requests using the instance's settings.

        Returns:
            dict: A dictionary of common headers used in API requests.

        Examples:
            >>> base = ICABase()
            >>> headers = base.get_headers()
        """
        libica_version = version("libica")  # This should be moved to a class or instance variable
        return {
            "x-access-token": self.settings.assistants_access_token,
            "x-extension-app-id": self.settings.assistants_app_id,
            "x-security-key": self.settings.assistants_api_key,
            "Content-Type": "application/json",
            "accept": "application/json",
            "User-Agent": f"libica {libica_version}",
        }

    def get_stream_headers(self) -> dict:
        """
        Return the common headers for making streaming API requests using the instance's settings.

        Returns:
            dict: A dictionary of common headers used in API requests.

        Examples:
            >>> base = ICABase()
            >>> headers = base.get_headers()
        """
        libica_version = version("libica")  # This should be moved to a class or instance variable
        return {
            "x-access-token": self.settings.assistants_access_token,
            "x-extension-app-id": self.settings.assistants_app_id,
            "x-security-key": self.settings.assistants_api_key,
            "Content-Type": "application/json",
            "User-Agent": f"libica {libica_version}",
        }

    def request_wrapper(self, method, url, **kwargs) -> Union[str, dict]:
        """
        Wrap requests with error handling and logging.

        Args:
            method (str): HTTP method to use for the request.
            url (str): URL for the request.
            **kwargs: Arbitrary keyword arguments for requests.request.

        Returns:
            Union[str, dict]: The response from the API, parsed as a JSON decoded object if possible, or raw text if JSON parsing fails.

        Raises:
            ValueError: If decoding of the JSON response fails.
            ICAClientError: For API-related errors, providing details of the encountered issue.

        Examples:
            >>> base = ICABase()
            >>> settings = Settings()
            >>> url = f"{settings.assistants_base_url}/getCollections"
            >>> data = base.request_wrapper("GET", url, headers=base.get_headers())
        """
        try:
            retries = self.settings.assistants_retry_attempts
            base_delay = self.settings.assistants_retry_base_delay
            max_delay = self.settings.assistants_retry_max_delay

            for attempt in range(1, retries + 1):
                try:
                    response = requests.request(method, url, **kwargs, timeout=REQUESTS_TIMEOUT)
                    response.raise_for_status()

                    # create_chat_id API no longer returns JSON in 4.5, returns string chat_id instead.
                    try:
                        json_data = response.json()
                        logging.debug(f"Request successful. URL: {url}, Method: {method}, Response: {json_data}")
                        return json_data
                    except ValueError:  # JSON parsing failed
                        logging.debug(
                            f"Received non-JSON response. URL: {url}, Method: {method}, Response: {response.text}"
                        )
                        return response.text  # Return as plain text

                except requests.exceptions.RequestException as e:
                    if attempt < retries:
                        delay = min(max_delay, base_delay * 2**attempt)

                        # Insert random jitter to avoid having all libica clients wake up at the same time
                        # This doesn't require the use of secrets, random is fine - added nosec B311 for bandit linter
                        jitter = random.uniform(0, 1)  # nosec B311
                        time.sleep(delay + jitter)

                        logging.debug(
                            f"Request failed, attempt {attempt+1} of {retries}, retrying with delay of {delay + jitter:.2f} seconds: {e}"
                        )

                        continue
                    logging.debug(f"Request error: {e}")
                    raise ICAClientError(f"Failed after {retries} attempts: {e}")

                except ValueError as e:
                    logging.debug(f"Error decoding JSON response: {e}")
                    raise ValueError(f"JSON decode error: {e}")

        except Exception as e:
            logging.error(f"Unhandled exception: {e}")
            raise ICAClientError(f"Unhandled exception: {e}")

        return ""  # not reached
