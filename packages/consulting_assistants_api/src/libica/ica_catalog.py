# -*- coding: utf-8 -*-
"""
LIBICA - IBM Consulting Assistants Extensions API - Python SDK.

Description: library supporting the IBM Consulting Assistants API v 4.5.

Authors: Mihai Criveti
"""

from __future__ import annotations

import json
import logging
from urllib.parse import quote

import requests
from libica import ica_model
from libica.ica_base import ICABase
from libica.ica_error import ICAClientError
from pydantic import ValidationError

# --------------------------------------------------------------------
# Initialize logging
# --------------------------------------------------------------------

log = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Classes
# --------------------------------------------------------------------


# --------------------------------------------------------------------
# Catalog Service Management: /apis/v1/catalog [Service Scope]
#
# get_catalog_user_roles GET /apis/v1/catalog/user-roles - Retrieve a list of user roles for a given catalog instance [Service Scope]
# get_catalog_user GET /apis/v1/catalog/user Retrieve list of catalog instances the user belongs to [Service Scope]
# get_catalog_teams GET /apis/v1/catalog/teams Retrieve list of team members for a given catalog instance [Service Scope]
# get_catalog_request_forms GET /apis/v1/catalog/requestforms Retrieve list of input properties for the last days [Service Scope]
# put_catalog_user_roles PUT /apis/v1/catalog/user-roles Update catalog user roles [Service Scope]
# --------------------------------------------------------------------


# --------------------------------------------------------------------
# get_catalog_user_roles GET /apis/v1/catalog/user-roles - Retrieve a list of user roles for a given catalog instance [Service Scope]
# --------------------------------------------------------------------


class ICACatalog(ICABase):
    """
    API Client to interact with IBM Consulting Assistants Extensions v4.5.

    This client provides methods to call API endpoints for managing models, tags, roles, assistants, collections, chat IDs, and executing prompts.
    It supports caching for models and tags to reduce network requests.

    Examples:
        >>> client = ICACatalog()
    """

    # TODO: Test Me
    def get_catalog_user_roles(self, user_email: str, team_name: str) -> list:
        """
        Retrieve a list of user roles for a given catalog instance.

        This method sends a GET request to retrieve a list of user roles.

        Args:
            user_email (str): The email address associated with the security key.
            team_name (str): The team name associated with the security key.

        Returns:
            dict: A dictionary with a message indicating the success or failure of the operation. The message is contained in a 'result' key.

        Raises:
            ValueError: If the email_address or team_name are empty.
            ICAClientError: For HTTP errors or other request-related issues, providing details of the specific error encountered.
            TypeError: If the response from the server is neither a str nor a dict as expected.

        Examples:
            >>> from libica import ICACatalog
            >>> catalog = ICACatalog()
            >>> user_roles = catalog.get_catalog_user_roles(user_email='crmihai1@ie.ibm.com', team_name='Assistants Education')
            >>> print(user_roles["name"])
            Mihai Criveti
        """
        if not user_email or not team_name:
            raise ValueError("user_email and team_name must not be empty.")

        try:
            # Validate inputs using Pydantic model
            request = ica_model.GetCatalogUserRolesRequest(user_email=user_email, team_name=team_name)
        except ValidationError as e:
            raise ValueError(f"Input validation error: {e}")

        encoded_team_name = quote(request.team_name)  # Escape any spaces by URL encoding the team name
        encoded_email_address = quote(request.user_email)  # Escape any spaces by URL encoding the email

        # TODO: change base url to /apis/v1 url = f"{self.settings.assistants_base_url}/removeSecurityKey?emailAddress={encoded_email_address}&teamName={encoded_team_name}"
        url = f"https://servicesessentials.ibm.com/apis/v1/catalog/user-roles?userEmail={encoded_email_address}&teamName={encoded_team_name}"
        logging.debug(f"Accessing URL: {url}")

        try:
            response = self.request_wrapper("GET", url, headers=self.get_headers())

            if isinstance(response, dict):
                response_data = response

            elif isinstance(response, str):
                try:
                    response_data = json.loads(response)
                except ValueError:
                    response_data = {"result": response}
            else:
                raise TypeError(
                    f"Expected a dict or a str from the user-role API, but got a different type: {type(response)}"
                )

            logging.debug(f"Get catalog user roles: {response_data}")
            return response_data

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            raise ICAClientError(f"HTTP error: {e.response.text}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")
            raise ICAClientError(f"Error during requests to {url}: {e}")
