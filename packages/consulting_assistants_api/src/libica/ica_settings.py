# -*- coding: utf-8 -*-
"""
LIBICA - IBM Consulting Assistants Extensions API - Python SDK.

Description: Contains settings specific to ICA (configurations and constants)

Authors: Mihai Criveti

Usage examples (with doctest):

# Load libica and initialize a settings object
>>> from libica import Settings
>>> settings = Settings()
"""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Literal, Optional

from pydantic import (DirectoryPath, Field, FilePath, ValidationInfo,
                      field_validator, model_validator)
from pydantic_settings import BaseSettings, SettingsConfigDict

# --------------------------------------------------------------------
# Initialize logging
# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------
# Constants
# --------------------------------------------------------------------

DEFAULT_CONFIG_FILE_LOCATION = "~/.config/icacli/.ica.env"  # Configuration file
DEFAULT_CACHE_DIRECTORY = "~/.config/icacli/cache"  # Cache directory
REQUESTS_TIMEOUT = 200  # Timeout used for requests library


# --------------------------------------------------------------------
# Settings
# --------------------------------------------------------------------
class Settings(BaseSettings):
    """
    Settings class to manage all the environment variables.

    Attributes:
        assistants_debug (Optional[bool]): Enable debug mode. Default is False.
        assistants_enable_rich_print (Optional[bool]): Enable rich print mode. Default is False.
        assistants_config_file_location (Optional[FilePath]): Path to config file. Default is ~/.config/icacli/.ica.env
        assistants_cache_directory (Optional[DirectoryPath]): Path to cache directory. Directory will be created if it does not exist. Default is the ~/.config/icacli/cache directory.
        assistants_base_url (str): Base URL for the assistant.
        assistants_app_id (str): App ID for the assistant.
        assistants_api_key (str): API key for the assistant.
        assistants_access_token (str): Access token for the assistant.
        assistants_cache_duration_hours (int): Cache duration in hours. Default is 24.
        assistants_default_model_id_or_name (str): Default model ID or name. Default is "Llama2 70B Chat".
        assistants_default_format (Literal["json", "table"]): Default format. Default is "table".
        assistants_retry_attempts (int): Number of retry attempts. Default is 3.
        assistants_retry_base_delay (float): Base delay for retry attempts in seconds. Default is 0.5.
        assistants_retry_max_delay (float): Maximum delay for retry attempts in seconds. Default is 60.0.
        assistants_tablefmt (Literal[...]): Table format. Options include python-tabulate supported types: plain, simple, github, fancy_grid, jira, html, ..., tsv. Default is "simple".
    """

    assistants_debug: Optional[bool] = Field(
        default=False,
        description="Enable debug mode for more verbose output.",
        examples=[0, 1],
    )
    assistants_enable_rich_print: Optional[bool] = Field(
        default=False,
        description="Enable rich print mode to enhance the display of outputs.",
        examples=[0, 1],
    )
    assistants_config_file_location: Optional[FilePath] = Field(
        default=Path("~/.config/icacli/.ica.env"),
        description="Path to the configuration file.",
        examples=[Path("/path/to/config.env")],
    )
    assistants_cache_directory: Optional[DirectoryPath] = Field(
        default=Path("~/.config/icacli/cache"),
        description="Path to the cache directory. The directory will be created if it does not exist.",
        examples=[Path("/path/to/cache")],
    )
    assistants_base_url: str = Field(
        default=...,
        description="Base URL for the assistant API.",
        examples=["https://servicesessentials.ibm.com/apis/v1/sidekick-ai"],
    )
    assistants_app_id: str = Field(
        default=...,
        description="Application ID for the assistant API. This field is mandatory.",
        examples=["your_app_id"],
    )
    assistants_api_key: str = Field(
        default=...,
        description="API key for the assistant. This field is mandatory.",
        examples=["your_api_key"],
    )
    assistants_access_token: str = Field(
        default=...,
        description="Access token for authenticated API calls. This field is mandatory.",
        examples=["your_access_token"],
    )
    assistants_cache_duration_hours: int = Field(
        default=24,
        description="Duration in hours for which the cache is valid.",
        examples=[0, 1, 24, 72],
    )
    assistants_default_model_id_or_name: str = Field(
        default="Llama2 70B Chat",
        description="Default model ID or name to use for the assistant.",
        examples=["Llama3.1 70b Instruct"],
    )
    assistants_default_format: Literal["json", "table"] = Field(
        default="table",
        description="Default format for displaying results.",
        examples=["json", "table"],
    )
    assistants_retry_attempts: int = Field(
        default=3,
        description="Number of retry attempts in case of API call failures.",
        examples=[3],
    )
    assistants_retry_base_delay: float = Field(
        default=1.5,
        description="Base delay in seconds for retry attempts, used in exponential backoff.",
        examples=[10.0],
    )
    assistants_retry_max_delay: float = Field(
        default=60.0,
        description="Maximum delay in seconds for retry attempts, used in exponential backoff.",
        examples=[120.0],
    )
    assistants_tablefmt: Literal[
        "plain",
        "simple",
        "github",
        "grid",
        "simple_grid",
        "rounded_grid",
        "heavy_grid",
        "mixed_grid",
        "double_grid",
        "fancy_grid",
        "outline",
        "simple_outline",
        "rounded_outline",
        "heavy_outline",
        "mixed_outline",
        "double_outline",
        "fancy_outline",
        "pipe",
        "orgtbl",
        "asciidoc",
        "jira",
        "presto",
        "pretty",
        "psql",
        "rst",
        "mediawiki",
        "moinmoin",
        "youtrack",
        "html",
        "unsafehtml",
        "latex",
        "latex_raw",
        "latex_booktabs",
        "latex_longtable",
        "textile",
        "tsv",
    ] = Field(
        default="simple",
        description="Table format for displaying results. Supported types from python-tabulate.",
        examples=["fancy_grid", "simple", "github", "tsv", "html"],
    )

    @model_validator(mode="before")
    def expand_paths(cls, values):  # pylint: disable=no-self-argument
        """
        Expand user paths and ensures necessary directories and files exist before model validation.

        This method is designed to be used as a pre-validation hook in Pydantic models.
        It modifies the 'values' dictionary in-place to expand user directories and create necessary directories and configuration files if they do not already exist.
        The method ensures that paths in the configuration for 'assistants_config_file_location' and 'assistants_cache_directory'
        are expanded to absolute paths and that these locations are properly initialized on the filesystem.

        Parameters:
            cls (type): The class on which the method is being called.
            values (dict): The dictionary of values being processed by the Pydantic model.

        Returns:
            dict: The modified dictionary with expanded paths and ensured file and directory existence.

        Example usage:
            When used in a Pydantic model, this method is triggered automatically as part of the validation process, preparing the environment for other operations that depend on these configurations.

        Decorators:
            @model_validator(mode="before"): Specifies that this validator should be run before other validation steps in Pydantic.

        Note:
            This function is dependent on the 'os' module for filesystem operations and should be used in environments where file access is permissible.
            When used with podman or OpenShift, ensure that the container is able to write to the provided `assistants_cache_directory`.
        """
        values["assistants_config_file_location"] = os.path.expanduser(
            values.get("assistants_config_file_location", DEFAULT_CONFIG_FILE_LOCATION)
        )
        values["assistants_cache_directory"] = os.path.expanduser(
            values.get("assistants_cache_directory", DEFAULT_CACHE_DIRECTORY)
        )

        # create cache directory if it doesn't exist
        os.makedirs(values["assistants_cache_directory"], exist_ok=True)

        # create config file if it doesn't exist
        if not os.path.isfile(values["assistants_config_file_location"]):
            with open(values["assistants_config_file_location"], "w", encoding="utf-8") as file:
                file.write("")  # Writing an empty string just to instantiate the file

        return values

    model_config = SettingsConfigDict(
        env_file=os.getenv("ASSISTANTS_CONFIG_FILE_LOCATION", DEFAULT_CONFIG_FILE_LOCATION),
        env_file_encoding="utf-8",
    )

    # Validator using Pydantic V2, strips quotes.
    @field_validator("*", mode="before")
    def strip_quotes(cls, v: str, info: ValidationInfo) -> str:  # pylint: disable=no-self-argument, unused-argument
        """
        Strip quotes. This method serves as a pre-validation field modifier for Pydantic models.

        It is applied to all string fields to remove both single and double quotes that may encase the field value.
        This preprocessing ensures that string data is sanitized and uniform before any further validation rules or business logic is applied.

        Args:
            cls (type): The class on which the method is being called.
            v (str): The string value of the field to be processed.
            info (ValidationInfo): An object providing metadata about the field being validated, such as the field name.

        Returns:
            str: The string without quotes at the beginning and end.

        Example usage:
            Used as part of a field validation process in a Pydantic model, this method automatically strips quotes from incoming string data fields.

        Examples:
            >>> from libica import Settings
            >>> Settings.strip_quotes('"Hello, World!"', info='')
            'Hello, World!'
            >>> Settings.strip_quotes("'Hello, World!'", info='')
            'Hello, World!'
            >>> Settings.strip_quotes('No quotes here', info='')
            'No quotes here'

        Decorators:
            @field_validator("*", mode="before"): Indicates this validator should be applied to all fields before other validation steps executed as one of the initial validations.

        Note:
            This method only affects string fields. If the provided value is not a string, it will be returned unchanged.
        """
        if isinstance(v, str):
            v = v.strip()
            if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                return v[1:-1]
        return v
