# -*- coding: utf-8 -*-
"""
LIBICA - IBM Consulting Assistants Extensions API - Python SDK.

Description: library supporting the IBM Consulting Assistants API v 4.5.

Authors: Mihai Criveti

Usage examples (with doctest):

# Load libica and initialize a client
>>> from libica import ICAClient
>>> client = ICAClient()

# Using prompt_flow, will return a string with the response from the LLM
response = client.prompt_flow(model_id_or_name="Mixtral 8x7b Instruct", prompt="What is OpenShift?")
print(response)
"""

from __future__ import annotations

import json
import logging
import time
from datetime import datetime
from typing import List, Optional, Generator
from urllib.parse import quote

import requests
from libica import ica_model
from libica.ica_base import ICABase
from libica.ica_error import ICAClientError
from libica.ica_settings import REQUESTS_TIMEOUT
from pydantic import BaseModel, EmailStr, ValidationError

# --------------------------------------------------------------------
# Initialize logging with log model
# --------------------------------------------------------------------

log = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------
class ICAClient(ICABase):
    """
    API Client to interact with IBM Consulting Assistants Extensions v4.5.

    This client provides methods to call API endpoints for managing models, tags, roles, assistants, collections, chat IDs, and executing prompts.
    It supports caching for models and tags to reduce network requests.

    Examples:
        >>> client = ICAClient()
    """

    # ====================================================================
    # ICAClient classes: Sidekick AI App Management (Service Scope)      #
    # ====================================================================
    # TODO: keep
    def get_model_id_by_name(self, model_name: str, refresh_data: bool = False) -> Optional[str]:
        """
        Retrieve the model ID for a given model name from the cache or API, or return the input if it is already a digit-based ID.

        Args:
            model_name (str): The name of the model.
            refresh_data (bool): Forces the function to bypass the cache and read from the API.

        Returns:
            Optional[str]: The model ID if found, None otherwise.

        Examples:
            Get the model it for the model name "Mixtral 8x7b Instruct"
            >>> client = ICAClient()
            >>> client.get_model_id_by_name("Mixtral 8x7b Instruct")
            '222'
        """
        if model_name and str(model_name).isdigit():
            return str(model_name)

        models = self.get_models(refresh_data=refresh_data)

        for model in models:
            if model["name"] == model_name:
                return model["id"]
        return None

    # --------------------------------------------------------------------
    # Sidekick AI App Management: /apis/v1/sidekick-ai  [Service Scope]
    #
    # remove_security_key DELETE /apis/v1/sidekick-ai/removeSecurityKey Remove Sidekick AI Security Key [Service Scope]
    # remove_chat_id DELETE /apis/v1/sidekick-ai/removeChatId Remove Sidekick AI Chat Id [Service Scope]
    # validate_security_key GET /apis/v1/sidekick-ai/validateSecurityKey Validate Sidekick AI Security Key [Service Scope]
    # validate_extension_app_id GET /apis/v1/sidekick-ai/validateExtensionAppId Validate Sidekick AI Extension App Id [Service Scope]
    # get_transaction_response GET /apis/v1/sidekick-ai/getTransactionResponse Get SidekickAI Execute Prompt Transaction Response [Service Scope]
    # get_tags GET /apis/v1/sidekick-ai/getTags Get Sidekick AI Tags for Assistants and Prompts [Service Scope]
    # get_security_key GET /apis/v1/sidekick-ai/getSecurityKey Get Sidekick AI Security Key [Service Scope]
    # get_roles GET /apis/v1/sidekick-ai/getRoles Get Sidekick AI Roles for Assistants and Prompts [Service Scope]
    # get_models GET /apis/v1/sidekick-ai/getModels Get Sidekick AI Team Models [Service Scope]
    # get_model GET /apis/v1/sidekick-ai/getModel Get Sidekick AI Team Model [Service Scope]
    # get_collections GET /apis/v1/sidekick-ai/getCollections Get Sidekick AI Document Collection [Service Scope]
    # get_prompts POST /apis/v1/sidekick-ai/getPrompts Get Sidekick AI Prompts [Service Scope]
    # get_assistants POST /apis/v1/sidekick-ai/getAssistants Get Sidekick AI Assistants [Service Scope]
    # execute_prompt POST /apis/v1/sidekick-ai/executePrompt Execute Sidekick AI Prompt against a model or assistant [Service Scope]
    # execute_prompt_async POST /apis/v1/sidekick-ai/executePromptAsync Execute Sidekick AI Prompt against a model or assistant asynchronously [Service Scope]
    # create_security_key POST /apis/v1/sidekick-ai/createSecurityKey Create Sidekick AI Security Key [Service Scope]
    # create_prompt POST /apis/v1/sidekick-ai/createPrompt Create Sidekick AI Prompt [Service Scope]
    # create_chat_id POST /apis/v1/sidekick-ai/createChatId Create Sidekick AI ChatId [Service Scope]
    # --------------------------------------------------------------------

    # --------------------------------------------------------------------
    # Get models, tags, roles, prompts, assistants, collections          #
    # --------------------------------------------------------------------
    def get_models(self, refresh_data: bool = False) -> List:
        """
        Retrieve the list of models, using cached data if available.

        This method checks if cached data is valid and uses it unless a refresh of the data is explicitly requested.
        If refreshing, it makes an HTTP GET request to retrieve model data.

        Args:
            refresh_data (bool): Forces the function to bypass the cache and read from the API.

        Returns:
            list: A list containing model details.

        Raises:
            TypeError: If the API does not return a list as expected.

        Examples:
            Get models, and filter to a specific model ID (222):
            >>> client = ICAClient()
            >>> models = client.get_models(refresh_data = False)
            >>> for model in models:
            ...     if model['id'] == "222":
            ...         print(model['id'], model['name'])
            222 Mixtral 8x7b Instruct
            >>> models = client.get_models(refresh_data = True)  # Get model data from the server
        """
        cache_file = "models.json"
        if not refresh_data and self.is_cache_valid(cache_file):
            return self.read_cache(cache_file)

        url = f"{self.settings.assistants_base_url}/getModels"
        data = self.request_wrapper("GET", url, headers=self.get_headers())

        if isinstance(data, list):
            self.write_cache(cache_file, data)
            return data
        raise TypeError(f"Expected a list from the API, but got a different type: {type(data)}")

    def get_tags(self, refresh_data: bool = False) -> List:
        """
        Retrieve the list of tags, using cached data if available.

        Args:
            refresh_data (bool): Forces the function to bypass the cache and read from the API.

        Returns:
            list: A JSON response containing the list of tags.

        Raises:
            TypeError: If the API response is not a list as expected.

        Examples:
            Get tags, filter to a specific tag:
            >>> client = ICAClient()
            >>> tags = client.get_tags(refresh_data = False)
            >>> for tag in tags:
            ...     if tag == 'unified':
            ...         print(tag)
            unified

            Or, you can return the data directly from the server by setting `refresh_data = True`:
            >>> tags = client.get_tags(refresh_data = True)
        """
        cache_file = "tags.json"
        if not refresh_data and self.is_cache_valid(cache_file):
            return self.read_cache(cache_file)

        url = f"{self.settings.assistants_base_url}/getTags"
        data = self.request_wrapper("GET", url, headers=self.get_headers())

        # Check if the data is a list before writing to cache
        if isinstance(data, list):
            self.write_cache(cache_file, data)
            return data
        raise TypeError(f"Expected a list from the API, but got a different type: {type(data)}")

    def get_roles(self, refresh_data: bool = False) -> List:
        """
        Retrieve the list of roles, using cached data if available.

        This method decides whether to use cached data based on the `refresh_data` parameter. If `refresh_data` is False
        and the cache is valid, it returns the cached data. Otherwise, it fetches the data from the API and updates the cache.

        Args:
            refresh_data (bool): Forces the function to bypass the cache and read from the API.

        Raises:
            TypeError: If the response from the API is not a list as expected.

        Examples:
            Get roles, printing only if we find a role that matches 'methodx'
            >>> client = ICAClient()
            >>> roles = client.get_roles(refresh_data = False)  # Get data from cache
            >>> for role in roles:
            ...     if role == 'methodx':
            ...         print(role)
            methodx
            >>> roles = client.get_roles(refresh_data = True)  # Get data from the server
        """
        cache_file = "roles.json"
        if not refresh_data and self.is_cache_valid(cache_file):
            return self.read_cache(cache_file)

        url = f"{self.settings.assistants_base_url}/getRoles"
        data = self.request_wrapper("GET", url, headers=self.get_headers())

        # Check if the data is a list before writing to cache
        if isinstance(data, list):
            self.write_cache(cache_file, data)
            return data
        raise TypeError(f"Expected a list from the API, but got a different type: {type(data)}")

    def get_prompts(
        self,
        tags: Optional[List[str]] = None,
        roles: Optional[List[str]] = None,
        refresh_data: bool = False,
    ) -> List:
        """
        Retrieve prompts with specific tags and roles, using cached data if available, or fetching from the API.

        This method filters prompts based on provided tags and roles. It uses caching to optimize data retrieval,
        refreshing the cache as specified. The cache key is uniquely defined based on the combination of tags and roles.

        Args:
            tags (Optional[List[str]]): A list of tags to filter prompts by; if None, no tag filter is applied.
            roles (Optional[List[str]]): A list of roles to filter prompts by; if None, no role filter is applied.
            refresh_data (bool): If True, bypasses the cache to fetch fresh data from the API.

        Returns:
            list: A list containing the filtered prompts.

        Raises:
            TypeError: If the response from the API is not a list as expected.

        Examples:
            Get prompts
            >>> client = ICAClient()
            >>> prompts = client.get_prompts(refresh_data = False)  # from cache
            >>> prompts = client.get_prompts(refresh_data = True)   # refresh data from the server
        """
        cache_file = "prompts.json"
        cache_key = f"{','.join(tags or [])}-{','.join(roles or [])}"
        if not refresh_data and self.is_cache_valid(cache_file):
            cached_data = self.read_cache(cache_file)
            if cache_key in cached_data:
                return cached_data[cache_key]

        url = f"{self.settings.assistants_base_url}/getPrompts"
        json_input_data = {"tags": tags or [], "roles": roles or []}

        response_data = self.request_wrapper("POST", url, json=json_input_data, headers=self.get_headers())

        # Validate response data type
        if not isinstance(response_data, list):
            raise TypeError(f"Expected a list from the API, but got a different type: {type(response_data)}")

        # Cache the valid response
        if self.is_cache_valid(cache_file):
            cached_data = self.read_cache(cache_file)
        else:
            cached_data = {}

        cached_data[cache_key] = response_data
        self.write_cache(cache_file, cached_data)

        return response_data

    def get_assistants(
        self,
        tags: Optional[List[str]] = None,
        roles: Optional[List[str]] = None,
        refresh_data: bool = False,
    ) -> List:
        """
        Retrieve assistants with specified tags and roles, using cached data if available, or fetching from the API.

        This method filters assistants based on provided tags and roles. It uses a caching strategy, fetching data from
        the API only when necessary or explicitly requested by setting `refresh_data` to True.
        A unique cache key is created based on the concatenated tags and roles to store and retrieve the relevant data.

        Args:
            tags (Optional[List[str]]): A list of tags to filter the assistants by. If None, no tag-based filtering is applied.
            roles (Optional[List[str]]): A list of roles to filter the assistants by. If None, no role-based filtering is applied.
            refresh_data (bool): If True, forces the method to bypass the cache and fetch fresh data from the API.

        Returns:
            list: A list containing the filtered assistants. Each assistant is represented as a dictionary.

        Raises:
            TypeError: If the response from the API is not a list as expected.

        Examples:
            Get assistants by tag
            >>> client = ICAClient()
            >>> assistants = client.get_assistants(tags=['unified'])  # Get data from cache
            >>> for assistant in assistants:
            ...     if assistant['id'] == "3903": # Assistants are NOT printed in order
            ...         print(assistant['id'], assistant['title'])
            3903 UNIFIED 01: Epic and User Story Creator
            >>> assistants = client.get_assistants(tags=['unified'], refresh_data=True)  # Get data from the server
        """
        cache_file = "assistants.json"
        cache_key = f"{','.join(tags or [])}-{','.join(roles or [])}"
        if not refresh_data and self.is_cache_valid(cache_file):
            cached_data = self.read_cache(cache_file)
            if cache_key in cached_data:
                return cached_data[cache_key]

        url = f"{self.settings.assistants_base_url}/getAssistants"
        json_input_data = {"tags": tags or [], "roles": roles or []}
        response_data = self.request_wrapper("POST", url, json=json_input_data, headers=self.get_headers())

        # Validate response data type
        if not isinstance(response_data, list):
            raise TypeError(f"Expected a list from the API, but got a different type: {type(response_data)}")

        # Cache the valid response
        if self.is_cache_valid(cache_file):
            cached_data = self.read_cache(cache_file)
        else:
            cached_data = {}

        cached_data[cache_key] = response_data
        self.write_cache(cache_file, cached_data)

        return response_data

    def get_collections(self, refresh_data: bool = False) -> dict:
        """
        Retrieve the list of document collections available, using cached data when possible.

        This method fetches data about document collections. If `refresh_data` is set to False and the cache is valid,
        it returns the cached data. If `refresh_data` is True or the cache is invalid, it fetches fresh data from the API.

        Args:
            refresh_data (bool): If True, bypasses the cached data and fetches directly from the API.

        Returns:
            dict: A dictionary containing the list of collections, structured as a JSON response.

        Raises:
            TypeError: If the response from the API is not a dictionary as expected.

        Examples:
            Get collections from cache
            >>> client = ICAClient()
            >>> collections = client.get_collections(refresh_data = False) # From cache
            >>> collections = client.get_collections(refresh_data = True)  # From the server
        """
        cache_file = "collections.json"
        if not refresh_data and self.is_cache_valid(cache_file):
            return self.read_cache(cache_file)

        url = f"{self.settings.assistants_base_url}/getCollections"
        response_data = self.request_wrapper("GET", url, headers=self.get_headers())

        # Validate response data type
        if not isinstance(response_data, dict):
            raise TypeError(f"Expected a dictionary from the API, but got a different type: {type(response_data)}")

        # Cache the valid response
        self.write_cache(cache_file, response_data)

        return response_data

    # --------------------------------------------------------------------
    # create_chat_id, remove_chat_id
    # --------------------------------------------------------------------
    def create_chat_id(
        self,
        model_id_or_name: Optional[str] = None,
        assistant_id: Optional[str] = None,
        collection_id: Optional[str] = None,
        refresh_data: bool = False,
    ) -> str:
        """
        Create a chat ID for interaction, using either a model ID, model name, an assistant ID, or a collection ID.

        This method generates a unique chat ID for interactions based on specified model, assistant, or collection identifiers.
        It requires at least one identifier to be provided and can optionally bypass the cache.

        Args:
            model_id_or_name (Optional[str]): The model ID or model name to use for creating a chat ID.
            assistant_id (Optional[str]): The assistant ID to use for creating a chat ID.
            collection_id (Optional[str]): The collection ID to use for creating a chat ID. One of model_id_or_name,
                                            assistant_id, or collection_id must be provided.
            refresh_data (bool): If True, forces the bypass of cache data.

        Returns:
            str: The chat ID as a plain string.

        Raises:
            ValueError: If no identifier (model_id_or_name, assistant_id, or collection_id) is provided.
            TypeError: If received response (chat_id) is not a string.
            ICAClientError: For HTTP errors or other request issues.

        Examples:
            chat_id will be a string, such as '661e40be6dd6607c6d67e5de'
            >>> client = ICAClient()
            >>> chat_id = client.create_chat_id(model_id_or_name='222')
            >>> print(type(chat_id))
            <class 'str'>
        """
        # Validate that at least one identifier is provided
        if not any([model_id_or_name, assistant_id, collection_id]):
            raise ValueError("Either model_id/model_name, assistant_id, or collection_id must be provided.")

        model_id = None
        if model_id_or_name:
            model_id = self.get_model_id_by_name(model_id_or_name, refresh_data=refresh_data)

        url = f"{self.settings.assistants_base_url}/createChatId"
        data = {
            "modelId": model_id,
            "assistantId": assistant_id,
            "collectionId": collection_id,
        }

        # Filter out None values from data dictionary
        data = {k: v for k, v in data.items() if v is not None}

        try:
            logging.debug(f"Calling {url} with payload: {data} and {self.get_headers()}")
            ica_response = self.request_wrapper("POST", url, json=data, headers=self.get_headers())
            logging.debug(f"Received response: {ica_response}")

            if isinstance(ica_response, str):
                return ica_response
            raise TypeError(
                f"Expected a string from the API (the chat_id), but got a different type: {type(ica_response)}"
            )

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise ICAClientError(f"HTTP error: {e.response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            raise ICAClientError(f"Error during requests to {url}: {e}")

    def remove_chat_id(self, chat_id: str) -> dict:
        """
        Remove a specific chat ID and return a message indicating the outcome.

        This method deletes a chat ID using an API call and handles potential errors that may occur during the request.
        It logs the request and response data for debugging purposes.
        Note that chat IDs are normally removed automatically after 15 minutes.

        Args:
            chat_id (str): The chat ID to be deleted.

        Returns:
            dict: A dictionary with a message indicating the success or failure of the operation. The message is contained in a 'message' key.

        Raises:
            ICAClientError: For HTTP errors or other request issues, providing details of the specific error encountered.
            ValueError: If the JSON response is malformed and cannot be parsed.
            TypeError: If the response from the server is neither a string nor a dictionary as expected.

        Examples:
            chat_id will be a string, such as '661e40be6dd6607c6d67e5de'
            >>> client = ICAClient()
            >>> chat_id = client.create_chat_id(model_id_or_name='222')
            >>> remove_chat_id_response = client.remove_chat_id(chat_id)
        """
        url = f"{self.settings.assistants_base_url}/removeChatId"
        data = {"chatId": chat_id}

        try:
            ica_response = self.request_wrapper("DELETE", url, json=data, headers=self.get_headers())

            if isinstance(ica_response, dict):
                response_data = ica_response

            elif isinstance(ica_response, str):
                try:
                    response_data = json.loads(ica_response)
                except ValueError:
                    response_data = {"message": ica_response}
            else:
                raise TypeError(
                    f"Expected a dict or a string from the API, but got a different type: {type(ica_response)}"
                )

            logging.debug(f"Delete chat ID response: {response_data}")
            return response_data

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise ICAClientError(f"HTTP error: {e.response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            raise ICAClientError(f"Error during requests to {url}: {e}")

    # --------------------------------------------------------------------
    # execute_prompt, execute_prompt_async, get_transaction_response
    # --------------------------------------------------------------------
    def execute_prompt(
        self,
        prompt: str,
        chat_id: str,
        model_id_or_name: Optional[str] = None,
        assistant_id: Optional[str] = None,
        collection_id: Optional[str] = None,
        document_names: Optional[list] = None,
        system_prompt: Optional[str] = None,
        parameters: Optional[dict] = None,
        substitution_parameters: Optional[dict] = None,
        refresh_data: bool = False,
        retrieve_chunks: bool = False,
    ) -> dict:
        """
        Execute a prompt synchronously using identifiers like model ID, model name, assistant ID, or collection ID.

        This method sends a prompt to an API for execution.
        It can utilize various identifiers to specify the execution context and includes parameters for customizing the execution.
        The function ensures that at least one of the model, assistant, or collection identifiers is provided.

        Args:
            prompt (str): The text prompt to execute.
            chat_id (str): The chat ID associated with the session in which the prompt will be executed.
            model_id_or_name (Optional[str]): The model ID or name for selecting the processing model. Required if neither assistant_id nor collection_id is provided.
            assistant_id (Optional[str]): The assistant ID to use for the execution. Required if neither model_id_or_name nor collection_id is provided.
            collection_id (Optional[str]): The collection ID to use. Required if neither model_id_or_name nor assistant_id is provided.
            document_names (Optional[list]): The list of documents to query. You can select one or more documents.
            system_prompt (Optional[str]): An additional system-level prompt to include in the execution.
            parameters (Optional[dict]): Key-value pairs defining execution parameters where keys are parameter names and values are the parameters' values.
            substitution_parameters (Optional[dict]): Key-value pairs for parameters that can be substituted into the prompt text.
            refresh_data (bool): If True, bypasses any cached data to ensure the latest information is used.
            retrieve_chunks (bool): If True, retrieves and includes chunks in the response. Defaults to False.

        Returns:
            dict: A dictionary containing the results of the prompt execution, including chunks if requested.

        Raises:
            ValueError: If no model_id_or_name, assistant_id, or collection_id is provided.
            TypeError: If the API response is not a dictionary.

        Examples:
            You first need to create a chat_id. To do everything in one go, see prompt_flow instead.
            >>> client = ICAClient()
            >>> chat_id = client.create_chat_id(model_id_or_name='Llama2 70B Chat')
            >>> prompt_response = client.execute_prompt(chat_id = chat_id, model_id_or_name='Llama2 70B Chat', prompt="Hi")
            >>> print(prompt_response['modelId'])
            41
        """
        model_id = None
        if model_id_or_name:
            model_id = self.get_model_id_by_name(model_id_or_name, refresh_data=refresh_data)

        logging.debug(f"Received collection_id and document_names: {collection_id}: {document_names}")
        if collection_id and isinstance(document_names, list):
            logging.debug(f"Calling document names validator for {document_names}!")
            self.validate_document_names(collection_id=collection_id, document_names=document_names)

        logging.debug(f"Resolved model_id_or_name: {model_id_or_name} to {model_id}")

        url = f"{self.settings.assistants_base_url}/executePrompt"

        data = {
            "prompt": prompt,
            "chatId": chat_id,
            "modelId": model_id,
            "assistantId": assistant_id,
            "systemPrompt": system_prompt,
            "parameters": parameters,
            "substitutionParameters": substitution_parameters,
            "collectionId": collection_id,
            "documentNames": document_names,
            "retrieveChunks": retrieve_chunks,
        }

        data = {k: v for k, v in data.items() if v is not None}

        logging.debug(f"Calling {url} with payload: {data}")

        ica_response = self.request_wrapper("POST", url, json=data, headers=self.get_headers())

        if not isinstance(ica_response, dict):
            raise TypeError(f"Expected a dictionary from the API, but got a different type: {type(ica_response)}")

        logging.debug(f"Received response: {ica_response}")

        return ica_response

    # TODO: Add error handling
    def execute_prompt_stream(
        self,
        prompt: str,
        chat_id: str,
        model_id_or_name: Optional[str] = None,
        assistant_id: Optional[str] = None,
        collection_id: Optional[str] = None,
        document_names: Optional[list] = None,
        system_prompt: Optional[str] = None,
        parameters: Optional[dict] = None,
        substitution_parameters: Optional[dict] = None,
        refresh_data: bool = False,
        response_wait_time: int = 10,
        streaming_prefix: bool = False,
        response_chunk_size: int = 1024
    ) -> Generator[str, None, None]:
        """
        Execute a prompt stream using identifiers like model ID, model name, assistant ID, or collection ID.

        This method sends a prompt to an API for execution.
        It can utilize various identifiers to specify the execution context and includes parameters for customizing the execution.
        The function ensures that at least one of the model, assistant, or collection identifiers is provided.

        Args:
            prompt (str): The text prompt to execute.
            chat_id (str): The chat ID associated with the session in which the prompt will be executed.
            model_id_or_name (Optional[str]): The model ID or name for selecting the processing model. Required if neither assistant_id nor collection_id is provided.
            assistant_id (Optional[str]): The assistant ID to use for the execution. Required if neither model_id_or_name nor collection_id is provided.
            collection_id (Optional[str]): The collection ID to use. Required if neither model_id_or_name nor assistant_id is provided.
            document_names (Optional[list]): The list of documents to query. You can select one or more documents.
            system_prompt (Optional[str]): An additional system-level prompt to include in the execution.
            parameters (Optional[dict]): Key-value pairs defining execution parameters where keys are parameter names and values are the parameters' values.
            substitution_parameters (Optional[dict]): Key-value pairs for parameters that can be substituted into the prompt text.
            refresh_data (bool): If True, bypasses any cached data to ensure the latest information is used.
            response_wait_time (int): Sets the maximum waiting time between responses.
            streaming_prefix (bool): If True, returns 'data:' as suffix to each word.
            response_chunk_size (int): The size of the chunk to be returned.

        Returns:
            dict: A stream of string containing the results of the prompt execution.

        Raises:
            ValueError: If no model_id_or_name, assistant_id, or collection_id is provided.
        """
        model_id = None
        if model_id_or_name:
            model_id = self.get_model_id_by_name(
                model_id_or_name, refresh_data=refresh_data
            )

        logging.debug(
            f"Received collection_id and document_names: {collection_id}: {document_names}"
        )
        if collection_id and isinstance(document_names, list):
            logging.debug(f"Calling document names validator for {document_names}!")
            self.validate_document_names(
                collection_id=collection_id, document_names=document_names
            )

        logging.debug(f"Resolved model_id_or_name: {model_id_or_name} to {model_id}")

        url = f"{self.settings.assistants_base_url}/executePromptStream"

        # Include collection_id in the data payload if provided
        data = {
            "prompt": prompt,
            "chatId": chat_id,
            "modelId": model_id,
            "assistantId": assistant_id,
            "systemPrompt": system_prompt,
            "parameters": parameters,
            "substitutionParameters": substitution_parameters,
            "collectionId": collection_id,
            "documentNames": document_names,
            "responseWaitTime": response_wait_time,
            "streamingPrefix": streaming_prefix
        }

        # Filter out None values from data dictionary
        data = {k: v for k, v in data.items() if v is not None}

        logging.debug(f"Calling {url} with payload: {data}")

        # TODO: Fix request_wrapper to accept 'stream=True'.
        # Currently throws: 'ICAClientError(f"Unhandled exception: {e}") 406 Client Error: Not Acceptable for url'
        # TODO: Fix unnecessary quotes and newlines
        ica_response = requests.post("POST", url, json=data, headers=self.get_stream_headers(), stream=True)
        for chunk in ica_response.iter_content(chunk_size=response_chunk_size):
            if chunk:
                # chunk_decoded = chunk.decode("utf-8")
                # chunk_decoded = chunk_decoded.strip().replace('"', '').replace('\n', '')
                yield chunk.strip()

    def validate_document_names(
        self, collection_id: str, document_names: List[str], refresh_data: bool = False
    ) -> bool:
        """
        Validate whether all given document names exist within a specific collection.

        This function fetches the current list of collections and checks if all provided document names are present
        within the collection specified by the `collection_id`. The collections data is fetched either from a cache
        or directly from the API depending on the `refresh_data` flag.

        Args:
            collection_id (str): The unique identifier for the collection to be validated against.
            document_names (List[str]): A list of document names to be validated.
            refresh_data (bool): If True, bypasses the cached data and fetches directly from the API.

        Returns:
            bool: True if all document names exist in the collection, False otherwise.

        Raises:
            Exception: If there is an issue fetching the collection data.

        Examples:
            >>> client = ICAClient()
            >>> client.validate_document_names('650affe1c4cf748ea11ce5b5', ['1c) Building Intelligent Solutions Guide FY24PP.pptx.pdf'], refresh_data=False)
            True
            >>> client.validate_document_names('650affe1c4cf748ea11ce5b5', ['nonexistent_document.pdf'], refresh_data=True)
            False
        """
        logging.debug(f"Document validation received: {collection_id} {document_names}")

        try:
            collections = self.get_collections(refresh_data=refresh_data)
        except Exception as e:
            logging.error(f"Failed to fetch collections: {str(e)}")
            raise Exception("Failed to fetch collection data") from e

        # Find the specified collection
        for collection in collections.get("collections", []):
            if collection["_id"] == collection_id:
                missing_documents = [doc for doc in document_names if doc not in collection["documentNames"]]
                if missing_documents:
                    logging.debug(f"Documents not found: {missing_documents}")
                    return False
                logging.debug(f"All documents validated for collection ID {collection_id}")
                return True

        logging.error(f"Collection ID not found: {collection_id}")
        return False

    def execute_prompt_async(
        self,
        prompt: str,
        chat_id: str,
        model_id_or_name: Optional[str] = None,
        assistant_id: Optional[str] = None,
        collection_id: Optional[str] = None,
        document_names: Optional[list] = None,
        system_prompt: Optional[str] = None,
        parameters: Optional[dict] = None,
        substitution_parameters: Optional[dict] = None,
        refresh_data: bool = False,
        retrieve_chunks: bool = False,
    ) -> str:
        """
        Execute a prompt asynchronously, using identifiers such as a model ID, model name, assistant ID, or collection ID.

        This method sends a prompt for execution via an API and returns a transaction ID that can be used to poll for or retrieve the result asynchronously.
        It validates that exactly one identifier (model, assistant, or collection) is provided, and accepts additional parameters to configure the execution.

        Args:
            prompt (str): The text prompt to be executed.
            chat_id (str): The chat ID associated with the session.
            model_id_or_name (Optional[str]): The model ID or name to use for execution. Exactly one identifier must be provided.
            assistant_id (Optional[str]): The assistant ID for execution. Exactly one identifier must be provided.
            collection_id (Optional[str]): The collection ID for the execution. Exactly one identifier must be provided.
            document_names (Optional[list]): The list of documents to query. You can select one or more documents.
            system_prompt (Optional[str]): An additional system-level prompt to include in the execution.
            parameters (Optional[dict]): Key-value pairs that define execution parameters.
            substitution_parameters (Optional[dict]): Key-value pairs for substitution parameters that replace parts of the prompt text.
            refresh_data (bool): If True, bypasses any cached data to ensure the most up-to-date information is used.
            retrieve_chunks (bool): If True, retrieves and includes chunks in the response. Defaults to False.

        Returns:
            str: A transaction ID that can be used to track the asynchronous execution.

        Raises:
            ValueError: If zero or more than one identifier is provided.
            TypeError: If the API response is not a dictionary.
            ICAClientError: If there is an error in the API response, or missing expected data like the transaction ID.

        Examples:
             You first need to create a chat_id. To do everything in one go, see prompt_flow instead.
             >>> client = ICAClient()  # doctest: +SKIP
             >>> chat_id = client.create_chat_id(model_id_or_name='Llama3.1 70b Instruct')  # doctest: +SKIP
             >>> transaction_id = client.execute_prompt_async(chat_id = chat_id, model_id_or_name='Llama3.1 70b Instruct', prompt="What is 1+1, just the response, a single integer")  # doctest: +SKIP
             >>> response = client.get_async_response(transaction_id)  # doctest: +SKIP
             >>> print(response['response'])  # doctest: +SKIP
             2
             >>> client.remove_chat_id(chat_id) # optionally delete your chat_id  # doctest: +SKIP
             {'message': ''}

        """
        model_id = None
        if model_id_or_name:
            model_id = self.get_model_id_by_name(model_id_or_name, refresh_data=refresh_data)

        logging.debug(f"Received collection_id and document_names: {collection_id}: {document_names}")
        if collection_id and isinstance(document_names, list):
            logging.debug(f"Calling document names validator for {document_names}!")
            self.validate_document_names(collection_id=collection_id, document_names=document_names)

        identifiers_provided = sum(x is not None for x in [model_id_or_name, assistant_id, collection_id])
        if identifiers_provided != 1:
            raise ValueError("Exactly one of model_id_or_name, assistant_id, or collection_id must be provided.")

        url = f"{self.settings.assistants_base_url}/executePromptAsync"
        data = {
            "prompt": prompt,
            "chatId": chat_id,
            "modelId": model_id,
            "assistantId": assistant_id,
            "collectionId": collection_id,
            "documentNames": document_names,
            "systemPrompt": system_prompt,
            "parameters": parameters,
            "substitutionParameters": substitution_parameters,
            "retrieveChunks": retrieve_chunks,
        }

        data = {k: v for k, v in data.items() if v is not None}

        logging.debug(f"Calling {url} with payload: {data}")

        ica_response = self.request_wrapper("POST", url, json=data, headers=self.get_headers())

        logging.debug(f"Received response: {ica_response}")

        if not isinstance(ica_response, dict):
            raise TypeError(f"Expected a dictionary from the API, but got a different type: {type(ica_response)}")

        if "error" in ica_response:
            raise ICAClientError(f"API Error: {ica_response}")

        transaction_id = ica_response.get("transactionId")
        if not transaction_id:
            raise ICAClientError(f"Failed to retrieve transaction ID from response: {ica_response}")

        return transaction_id

    # --------------------------------------------------------------------
    # get_transaction_response, get_async_response
    # --------------------------------------------------------------------
    def get_transaction_response(self, transaction_id: str) -> dict:
        """
        Retrieve the response for a given transaction ID using the instance's settings.

        Args:
            transaction_id (str): The transaction ID to query.

        Returns:
            str: A string response containing the transaction result.

        Raises:
            TypeError: If the API response is not a dictionary as expected.

        Examples:
             >>> client = ICAClient()  # doctest: +SKIP
             >>> chat_id = client.create_chat_id(model_id_or_name='Llama2 70B Chat')  # doctest: +SKIP
             >>> transaction_id = client.execute_prompt_async(chat_id = chat_id, model_id_or_name='Llama2 70B Chat', prompt="Hi")  # doctest: +SKIP
             >>> import time  # doctest: +SKIP
             >>> time.sleep(70) # Sleep for 70 seconds waiting for the transaction to process  # doctest: +SKIP
             >>> response = client.get_transaction_response(transaction_id=transaction_id)  # doctest: +SKIP
             >>> client.remove_chat_id(chat_id) # optionally delete your chat_id  # doctest: +SKIP
             {'message': ''}
        """
        url = f"{self.settings.assistants_base_url}/getTransactionResponse?transactionId={str(transaction_id)}"
        response_data = self.request_wrapper("GET", url, headers=self.get_headers())
        logging.debug(f"response_data: {response_data}")

        if not isinstance(response_data, dict):
            raise TypeError(
                f"Unexpected response type from API: Expected a dictionary, received: {type(response_data)}"
            )

        return response_data

    def get_async_response(self, transaction_id: str, max_wait_time: int = 60, interval: int = 5) -> Optional[dict]:
        """
        Poll for the transaction response at specified intervals until a 'response' field is found or the maximum wait time is exceeded.

        This method is used to retrieve the result of an asynchronous prompt execution.
        It repeatedly checks for the result of a given transaction ID by polling the API at specified intervals.
        If the 'response' field is detected in the API's response, it returns this field as part of the response dictionary.
        If the maximum waiting time is reached without a response, it returns None.

        Args:
            transaction_id (str): The transaction ID for which to poll the response.
            max_wait_time (int, optional): The maximum time to wait for a response, in seconds. Defaults to 60.
            interval (int, optional): The interval at which to poll the API, in seconds. Defaults to 5.

        Returns:
            Optional[dict]: The transaction response if a 'response' field is found within the maximum wait time; None if the maximum wait time is exceeded.

        Raises:
            RuntimeError: If an error occurs during the API call or if unexpected data structure is received.


        Example:
            >>> client = ICAClient()
            >>> chat_id = client.create_chat_id(model_id_or_name='180')
            >>> transaction_id = client.execute_prompt_async(chat_id = chat_id, model_id_or_name='180', prompt="Hi")
            >>> response = client.get_async_response(transaction_id)
        """
        start_time = time.time()

        while True:
            response = self.get_transaction_response(transaction_id)

            # Check if 'response' field exists in the response
            if "response" in response:
                return response

            # Check if max_wait_time has passed
            if time.time() - start_time > max_wait_time:
                logging.warning(f"get_async_prompt max wait time: {max_wait_time} seconds exceeded. Stopping.")
                return None

            # Wait for 'interval' seconds before next check
            time.sleep(interval)

    # --------------------------------------------------------------------
    # prompt_flow
    # --------------------------------------------------------------------
    def prompt_flow(
        self,
        prompt: str,
        model_id_or_name: Optional[str] = None,
        assistant_id: Optional[str] = None,
        collection_id: Optional[str] = None,
        document_names: Optional[list] = None,
        system_prompt: Optional[str] = None,
        parameters: Optional[dict] = None,
        substitution_parameters: Optional[dict] = None,
        refresh_data: bool = False,
        retrieve_chunks: bool = False,
    ) -> Optional[str]:
        """
        Handle the complete flow of creating a chat ID and executing a prompt using that chat ID.

        This method simplifies user interactions by automating the sequence of creating a chat ID based on provided identifiers (model ID/name, assistant ID, or collection ID)
        and subsequently using that chat ID to execute a prompt.

        Args:
            prompt (str): The prompt to execute.
            model_id_or_name (Optional[str]): The model ID or model name to use for creating the chat ID and executing the prompt.
                Exactly one of model_id_or_name, assistant_id, or collection_id must be provided.
            assistant_id (Optional[str]): The assistant ID to use. Either model_id_or_name, assistant_id, or collection_id must be provided, but not more than one.
            collection_id (Optional[str]): The collection ID to use. Either model_id_or_name, assistant_id, or collection_id must be provided, but not more than one.
            document_names (Optional[list]): The list of documents to query. You can select one or more documents.
            system_prompt (Optional[str]): An additional system-level prompt to include in the execution.
            parameters (Optional[dict]): A dictionary of parameters defined on the model, where key-value pairs must match the model's parameter names and their respective values.
            substitution_parameters (Optional[dict]): A dictionary of substitution parameters defined on the model.
                Key-value pairs must match the model's substitution parameter names and respective values.
                If the prompt contains replaceable parameters, values for all expected substitutions must be provided.
            refresh_data (bool): If set to True, forces the bypass of any cached data to ensure the most current information is used.
            retrieve_chunks (bool): If True, retrieves and includes chunks in the response. Defaults to False.

        Returns:
            Optional[str]: The execution response as a string, or None if no response data is returned.

        Raises:
            ValueError: If neither model_id/model_name, assistant_id, nor collection_id is provided, or if more than one is provided.
            ICAClientError: For errors encountered during the creation of the chat ID or the execution of the prompt.


        Examples:
            >>> client = ICAClient()
            >>> response = client.prompt_flow(model_id_or_name="Llama3.1 70b Instruct", prompt="What is 1+1? Just give me the result, as a single integer, nothing else")
            >>> print(f"LLM Response: {response}")  # doctest: +ELLIPSIS
            LLM Response: ...

            Prompt a model, using advanced options. Here, I'm prompting a model by ID (Granite 13B V2.1)
            But you can also specify the model by name.
            See `get_models` for a list of parameters supported by each model.
            >>> response = client.prompt_flow(model_id_or_name="180", prompt="What is 1+1?", system_prompt="Talk like a pirate", parameters={'temperature':1, 'max_new_tokens': 100}) # doctest: +SKIP

            Prompt an assistant
            >>> response = client.prompt_flow(assistant_id="6858", prompt='Function to add 2 numbers') # doctest: +SKIP

            Prompt a document collection
            >>> response = client.prompt_flow(collection_id='66142f5a2dd4fae8aa4d5781', prompt='How do I list a collection using the API') # doctest: +SKIP
        """
        # Validate input parameters
        identifiers = [model_id_or_name, assistant_id, collection_id]
        if sum(x is not None for x in identifiers) != 1:
            raise ValueError(
                f"Exactly one of model_id_or_name, assistant_id, or collection_id must be provided. You provided {identifiers}"
            )

        model_id = None
        if model_id_or_name:
            model_id = self.get_model_id_by_name(model_id_or_name, refresh_data=refresh_data)

        # Create chat ID
        try:
            chat_id = self.create_chat_id(
                model_id_or_name=model_id,
                assistant_id=assistant_id,
                collection_id=collection_id,
                refresh_data=refresh_data,
            )
        except Exception as e:
            raise ICAClientError(f"Failed to create chat ID: {e}")

        # Execute prompt
        try:
            ica_response = self.execute_prompt(
                prompt=prompt,
                chat_id=chat_id,
                model_id_or_name=model_id,
                assistant_id=assistant_id,
                collection_id=collection_id,
                document_names=document_names,
                system_prompt=system_prompt,
                parameters=parameters,
                substitution_parameters=substitution_parameters,
                refresh_data=refresh_data,
                retrieve_chunks=retrieve_chunks,
            )
            logging.debug(f"Received response: {ica_response}")

            if retrieve_chunks:
                return ica_response
            else:
                return str(ica_response.get("response", "No response data."))
        except Exception as e:
            raise ICAClientError(f"Failed to execute prompt: {e}")

    # --------------------------------------------------------------------
    # create_prompt
    # --------------------------------------------------------------------
    def create_prompt(
        self,
        scope: str,
        prompt_title: str,
        model_id_or_name: str,
        prompt_description: str,
        prompt: str,
        prompt_response: Optional[str] = None,
        refresh_data: bool = False,
    ) -> list:
        """
        Create and save a new prompt to the database, optionally including an expected response.

        This method validates the presence of all required parameters and ensures that the model ID is resolved if only the model name is provided.
        It handles the creation of a new prompt in a specified scope with associated metadata and content.

        Args:
            scope (str): The scope of the prompt, options are 'mine', 'team', or 'both'.
            prompt_title (str): The title of the prompt.
            model_id_or_name (str): The model ID or the name of the model associated with the prompt.
            prompt_description (str): A description of what the prompt is about.
            prompt (str): The actual prompt text that will be executed.
            prompt_response (Optional[str]): The expected response for the prompt, useful for testing or documentation purposes.
            refresh_data (bool): If True, forces the resolution of the model ID from the model name each time the function is called.

        Returns:
            list: A list containing a dictionary with the API response indicating the success or failure of the creation.

        Raises:
            ValueError: If any required parameters are missing or if the model ID cannot be resolved.
            TypeError: If the response from the API is not a list as expected.
            RuntimeError: If the API returns an error message within the response.

        Examples:
            Create a prompt in your prompt library (scope = mine)
            >>> client = ICAClient()  # doctest: +SKIP
            >>> create_prompt_response = client.create_prompt(scope = "mine", prompt_title = "Title", model_id_or_name = "222", prompt = "What is k8s", prompt_description = "Define k8s")  # doctest: +SKIP
        """
        # Validate required parameters
        missing_params = [
            param
            for param, value in {
                "scope": scope,
                "prompt_title": prompt_title,
                "model_id_or_name": model_id_or_name,
                "prompt_description": prompt_description,
                "prompt": prompt,
            }.items()
            if not value
        ]

        if missing_params:
            error_message = f"Missing required parameters: {', '.join(missing_params)}"
            logging.error(error_message)
            raise ValueError(error_message)

        # Proceed with model_id_or_name validation and request construction
        model_id = self.get_model_id_by_name(model_id_or_name, refresh_data=refresh_data)
        if not model_id:
            raise ValueError("Model ID or name is invalid or could not be resolved.")

        # Construct the request URL and data payload, including 'promptResponse' if provided
        url = f"{self.settings.assistants_base_url}/createPrompt?scope={scope}"
        data = {
            "promptTitle": prompt_title,
            "description": prompt_description,
            "prompt": prompt,
            "model": model_id,
            "roles": ["General/NA"],  # TODO: make this dynamic, add tags too
        }

        # Include 'promptResponse' in the payload if it is provided
        if prompt_response is not None:
            data["promptResponse"] = prompt_response

        # Sending the request
        response = self.request_wrapper("POST", url, json=data, headers=self.get_headers())

        # Check if the response is a list
        if not isinstance(response, list):
            raise TypeError(f"Unexpected response type from API: Expected a list, received {type(response)}")

        # Check if there's an error in the response
        for item in response:
            if "error" in item:
                logging.error(f"Error from API when creating prompt: {item}")
                raise RuntimeError(f"API Error: {item}")
        return response

    # --------------------------------------------------------------------
    # NEW!
    # --------------------------------------------------------------------
    def get_model(self, model_id: int, refresh_data: bool = False) -> dict:
        """
        Retrieve model details dictionary from provided model_id, using cached data if available.

        This method checks if cached data is valid and uses it unless a refresh of the data is explicitly requested.
        If refreshing, it makes an HTTP GET request to retrieve model data.

        Args:
            model_id (int): A model id.
            refresh_data (bool): Forces the function to bypass the cache and read from the API.

        Returns:
            dict: A dict containing model details.

        Raises:
            ValueError: If the model_id input is not an int.
            TypeError: If the API does not return a list as expected.

        Examples:
            Get model details for a specific model ID:
            >>> client = ICAClient()
            >>> model = client.get_model(model_id=222, refresh_data = False)
            >>> print(model["model"]["name"])
            Mixtral 8x7b Instruct
        """
        if not isinstance(model_id, int):
            raise TypeError(
                f"Expected an int value for model_id: {model_id}, but got a different type: {type(model_id)}"
            )

        cache_file = f"model_{model_id}.json"
        if not refresh_data and self.is_cache_valid(cache_file):
            return self.read_cache(cache_file)

        url = f"{self.settings.assistants_base_url}/getModel?modelId={model_id}"
        data = self.request_wrapper("GET", url, headers=self.get_headers())

        if isinstance(data, dict):
            self.write_cache(cache_file, data)
            return data
        raise TypeError(f"Expected a dict from the API, but got a different type: {type(data)}")

    # --------------------------------------------------------------------
    # Token Management
    # TODO: go through the request_wrapper
    # --------------------------------------------------------------------
    def validate_extension_app_id(self, access_token: str, security_key: str, extension_app_id: str) -> dict:
        """
        Validate the provided x-extension-app-id with the server.

        This method uses the requests library to send a GET request to validate a security key and handles potential errors related to invalid keys.

        Args:
            access_token (str): Access token for authentication (x-access-token).
            security_key (str): Security key to be validated (x-security-key).
            extension_app_id (str): Extension app ID for authentication (x-extension-app-id).

        Returns:
            dict: A dictionary containing the response, if valid: {'extension_app_id': 'valid'}

        Examples:
            >>> from libica import ICAClient, Settings
            >>> client = ICAClient()
            >>> settings = Settings()
            >>> result = client.validate_extension_app_id(settings.assistants_access_token, settings.assistants_api_key, settings.assistants_app_id)
            >>> print(result)
            {'extension_app_id': 'valid'}

        Note: this method does not use the request_wrapper to make it easier for users to validate other keys
        """
        if not access_token or not security_key or not extension_app_id:
            raise ValueError("Access token, security key, and extension_app_id must not be empty.")

        url = f"{self.settings.assistants_base_url}/validateSecurityKey"
        headers = {
            "accept": "application/json",
            "x-access-token": access_token,
            "x-security-key": security_key,
            "x-extension-app-id": extension_app_id,
        }

        response = None
        try:
            response = requests.get(url, headers=headers, timeout=REQUESTS_TIMEOUT)
            response.raise_for_status()
            return {"extension_app_id": "valid"}  # If no exception, extension app ID is valid.
        except requests.exceptions.HTTPError:
            if response is not None:
                return response.json()  # Return JSON data if possible.
            return {"error": {"description": "HTTP error occurred, but no response was captured."}}
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        ):
            # Handle network-related errors that likely do not return a response.
            return {"error": {"description": "Failed to connect or timed out while attempting to validate."}}

    # TODO: migrate to requests_wrapper
    def validate_security_key(self, access_token: str, security_key: str) -> dict:
        """
        Validate the provided security key with the server.

        This method uses the requests library to send a GET request to validate a security key and handles potential errors related to invalid security keys.

        Args:
            access_token (str): Access token for authentication (x-access-token).
            security_key (str): Security key to be validated (x-security-key).

        Returns:1
            dict: A dictionary containing the response, if valid: {'security_key': 'valid'}

        Examples:
            >>> from libica import ICAClient, Settings
            >>> client = ICAClient()
            >>> settings = Settings()
            >>> result = client.validate_security_key(settings.assistants_access_token, settings.assistants_api_key)
            >>> print(result)
            {'security_key': 'valid'}

        Note: this method does not use the request_wrapper to make it easier for users to validate other keys.
        """
        if not access_token or not security_key:
            raise ValueError("Access token and security key must not be empty.")

        url = f"{self.settings.assistants_base_url}/validateSecurityKey"
        headers = {
            "accept": "application/json",
            "x-access-token": access_token,
            "x-security-key": security_key,
        }

        response = None
        try:
            response = requests.get(url, headers=headers, timeout=REQUESTS_TIMEOUT)
            response.raise_for_status()
            return {"security_key": "valid"}  # If no exception, security key is valid.
        except requests.exceptions.HTTPError as e:
            # Handle HTTP errors that may return a response.
            if response is not None:
                return response.json()  # Safely return JSON data if possible.
            return {"error": {"description": f"HTTP error occurred, but no response was captured: {e}"}}
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout,
            requests.exceptions.RequestException,
        ) as e:
            # Handle network-related errors that likely do not return a response.
            return {"error": {"description": str(e)}}

    def get_security_key(self, email_address: str, team_name: str) -> str:
        """
        Get IBM Consulting Assistants Security Key.

        This method uses the requests wrapper to send a GET request to retrieve a security key associated with an email and team name.

        Args:
            email_address (str): Email Address.
            team_name (str): Team Name.

        Returns:
            str: A str containing the response, empty string if there is no key.

        Raises:
            ValueError: If email_address, or team_name is empty.
            TypeError: If the API response is not a string as expected.
            ICAClientError: For HTTP errors or other request-related issues.

        Examples:
            >>> from libica import ICAClient, Settings
            >>> client = ICAClient()
            >>> settings = Settings()
            >>> security_key = client.create_security_key(email_address='crmihai1@ie.ibm.com', team_name='Assistants Education', expiry_date='2029-05-26T03:01:24.687Z')
            >>> security_key = client.get_security_key(email_address='crmihai1@ie.ibm.com', team_name='Assistants Education')
            >>> client.validate_security_key(settings.assistants_access_token, security_key)
            {'security_key': 'valid'}
        """
        if not email_address or not team_name:
            raise ValueError("access_token, email_address, and team_name must not be empty.")

        try:
            # Validate inputs using Pydantic model
            request = ica_model.GetSecurityKeyRequest(email_address=email_address, team_name=team_name)
        except ValidationError as e:
            raise ValueError(f"Input validation error: {e}")

        encoded_team_name = quote(request.team_name)  # Escape any spaces by URL encoding the team name
        encoded_email_address = quote(request.email_address)  # Escape any spaces by URL encoding the email

        url = f"{self.settings.assistants_base_url}/getSecurityKey?emailAddress={encoded_email_address}&teamName={encoded_team_name}"

        try:
            response_data = self.request_wrapper("GET", url, headers=self.get_headers())

            if not isinstance(response_data, str):
                raise TypeError(f"Expected a str from the API, but got a different type: {type(response_data)}")

            if response_data is not None:
                return str(response_data)
            return ""

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise ICAClientError(f"HTTP error: {e.response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            raise ICAClientError(f"Error during requests to {url}: {e}")

    class CreateSecurityKeyRequest(BaseModel):
        """
        A Pydantic model for validating input data for creating a security key.

        This class is used to validate that the necessary inputs for the `create_security_key` method
        meet the required format and type specifications. It ensures that the email address is valid,
        and that none of the required fields are missing.

        Attributes:
            email_address (EmailStr): A valid email address required for identifying the user.
                                        Uses Pydantic's EmailStr for validation to ensure the format is correct.
            team_name (str): The name of the team associated with the user and the security key, should not be empty.
            expiry_date (datetime): The date and time when the security key will expire.
        """

        email_address: EmailStr
        team_name: str
        expiry_date: datetime

    def create_security_key(self, email_address: str, team_name: str, expiry_date: str) -> str:
        """
        Create IBM Consulting Assistants Security Key.

        This method uses the requests library to send a POST request to create a security key associated with an email, team name, and expiry date.

        Args:
            email_address (str): Email Address.
            team_name (str): Team Name.
            expiry_date (str): Expiry Date in ISO 8601 format.

        Returns:
            str: A str containing the response, empty string if there is no key.

        Raises:
            ValueError: If email_address, team_name, or expiry_date is empty.
            TypeError: If the API response is not a string as expected.
            ICAClientError: For HTTP errors or other request-related issues.

        Examples:
            >>> from libica import ICAClient, Settings
            >>> client = ICAClient()
            >>> security_key = client.create_security_key(email_address='crmihai1@ie.ibm.com', team_name='Assistants Education', expiry_date='2029-05-26T03:01:24.687Z')
            >>> client.remove_security_key(email_address='crmihai1@ie.ibm.com', team_name='Assistants Education')
            {'result': ''}
        """
        if not email_address or not team_name or not expiry_date:
            raise ValueError("email_address, team_name, and expiry_date must not be empty.")

        try:
            # Validate inputs using Pydantic model
            request = self.CreateSecurityKeyRequest(
                email_address=email_address,
                team_name=team_name,
                expiry_date=datetime.fromisoformat(expiry_date),
            )
        except ValidationError as e:
            raise ValueError(f"Input validation error: {e}")

        url = f"{self.settings.assistants_base_url}/createSecurityKey"

        try:
            response_data = self.request_wrapper(
                "POST",
                url,
                headers=self.get_headers(),
                json={
                    "emailAddress": request.email_address,
                    "teamName": request.team_name,
                    "expiryDate": request.expiry_date.isoformat(),
                },
            )

            if not isinstance(response_data, str):
                raise TypeError(f"Expected a str from the API, but got a different type: {type(response_data)}")

            if response_data is not None:
                return str(response_data)
            return ""

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise ICAClientError(f"HTTP error: {e.response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            raise ICAClientError(f"Error during requests to {url}: {e}")

    def remove_security_key(self, email_address: str, team_name: str) -> dict:
        """
        Remove a security key associated with a specific email address and team name.

        This method sends a DELETE request to remove a security key and handles potential errors that may occur during the request. It logs the request and response data for debugging purposes.

        Args:
            email_address (str): The email address associated with the security key.
            team_name (str): The team name associated with the security key.

        Returns:
            dict: A dictionary with a message indicating the success or failure of the operation. The message is contained in a 'result' key.

        Raises:
            ValueError: If the email_address or team_name are empty.
            ICAClientError: For HTTP errors or other request-related issues, providing details of the specific error encountered.
            TypeError: If the response from the server is neither a str nor a dict as expected.

        Examples:
            >>> from libica import ICAClient, Settings
            >>> client = ICAClient()
            >>> settings = Settings()
            >>> security_key = client.create_security_key(email_address='crmihai1@ie.ibm.com', team_name='Assistants Education', expiry_date='2029-05-26T03:01:24.687Z')
            >>> client.remove_security_key(email_address='crmihai1@ie.ibm.com', team_name='Assistants Education')
            {'result': ''}
        """
        if not email_address or not team_name:
            raise ValueError("email_address and team_name must not be empty.")

        try:
            # Validate inputs using Pydantic model
            request = ica_model.RemoveSecurityKeyRequest(email_address=email_address, team_name=team_name)
        except ValidationError as e:
            raise ValueError(f"Input validation error: {e}")

        encoded_team_name = quote(request.team_name)  # Escape any spaces by URL encoding the team name
        encoded_email_address = quote(request.email_address)  # Escape any spaces by URL encoding the email

        url = f"{self.settings.assistants_base_url}/removeSecurityKey?emailAddress={encoded_email_address}&teamName={encoded_team_name}"

        try:
            response = self.request_wrapper("DELETE", url, headers=self.get_headers())

            if isinstance(response, dict):
                response_data = response

            elif isinstance(response, str):
                try:
                    response_data = json.loads(response)
                except ValueError:
                    response_data = {"result": response}
            else:
                raise TypeError(f"Expected a dict or a str from the API, but got a different type: {type(response)}")

            logging.debug(f"Remove security key response: {response_data}")
            return response_data

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise ICAClientError(f"HTTP error: {e.response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            raise ICAClientError(f"Error during requests to {url}: {e}")
