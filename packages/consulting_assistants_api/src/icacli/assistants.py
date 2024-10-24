#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
icacli - interactive IBM Consulting Assistants SDK tool, built on libica.

Description: IBM Consulting Assistants Extensions API - Python SDK

Authors: Mihai Criveti

Usage: icacli --help
Supports: export ASSISTANTS_DEBUG=1
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import signal
import sys
from getpass import getpass
from importlib.metadata import version
from pathlib import Path
from shutil import copyfile
from typing import Any, Dict, Optional, Sequence, Union

import argcomplete
from icacli.interactive_prompt import interactive_prompt_flow
from libica.ica_client import ICAClient
from libica.ica_settings import Settings
from rich import print as rich_print
from tabulate import tabulate

# --------------------------------------------------------------------
# Initialize logging
# --------------------------------------------------------------------

log = logging.getLogger(__name__)

# --------------------------------------------------------------------
# CONSTANTS
# --------------------------------------------------------------------

default_columns = {
    "get_models": ["id", "name"],
    "get_tags": None,
    "get_roles": None,
    "get_prompts": ["promptId", "prompt"],
    "get_assistants": ["id", "title"],  # description...
    "get_collections": [
        "_id",
        "collectionName",
        "visibility",
        "status",
        "createdAt",
        "updatedAt",
        "documentNames",
        "teamId",
        "userEmail",
        "userName",
        "tags",
        "roles",
    ],
}

# Configure logging based on settings
settings = Settings()

if settings.assistants_debug:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


logging.debug(f"Settings: {settings}")


# Check settings
def check_settings(settings_object: object) -> None:
    """
    Check if the required settings parameters are present and non-empty.

    Args:
        settings (object): The settings object which should contain the required parameters.

    Raises:
        SystemExit: If any required parameter is missing or empty.

    Examples:
        Check that all required settings are present and non-empty.
        >>> class Settings:
        ...     assistants_base_url = "http://localhost"
        ...     assistants_app_id = "123"
        ...     assistants_api_key = "abc"
        ...     assistants_access_token = "xyz"
        ...
        >>> check_settings(Settings) # No output means all required settings are present and non-empty.

        Raises a SystemExit if any of the required settings are empty or not present.
        >>> class Settings:
        ...     assistants_base_url = "http://localhost"
        ...     assistants_app_id = ""
        ...     assistants_api_key = "abc"
        ...     assistants_access_token = "xyz"
        ...
        >>> try:
        ...     print('doctest testing')
        ...     check_settings(Settings) # Raises SystemExit because `assistants_app_id` is empty.
        ... except SystemExit:
        ...     pass
        ... # doctest: +ELLIPSIS +NORMALIZE_WHITESPACE
        doctest ...
    """
    required_params = [
        "assistants_base_url",
        "assistants_app_id",
        "assistants_api_key",
        "assistants_access_token",
    ]

    # Check for both presence and non-emptiness of each parameter
    missing_or_empty_params = [param for param in required_params if not getattr(settings_object, param, None)]
    if missing_or_empty_params:
        for param in missing_or_empty_params:
            safe_print(
                f"[red]Error: {param.upper()} is not defined or is empty. You should export this as an environment variable or run --setup-config."
            )
        sys.exit(
            f"Exiting due to missing or empty configuration parameters. Run `icacli setup-config` or manually edit {settings.assistants_config_file_location}"
        )


def load_current_config(config_path: Path) -> Dict[str, str]:
    """
    Load the current configuration from the specified path, ignoring comments.

    Returns a dictionary with the configuration values, ensuring no surrounding quotes or comments.

    Args:
        config_path (Path): The path to the configuration file.

    Returns:
        Dict[str, str]: A dictionary containing the configuration values.

    Examples:
        Suppose we have a config file ('test/sample-ica-config-malformed.env') with the following content:
        ASSISTANTS_BASE_URL=https://servicesessentials.ibm.com/apis/v1/sidekick-ai
        ASSISTANTS_APP_ID=xxx
        ASSISTANTS_API_KEY=yyy
        ASSISTANTS_ACCESS_TOKEN=zzz
        ASSISTANTS_CACHE_DURATION_HOURS=24
        ASSISTANTS_DEFAULT_FORMAT=table
        ASSISTANTS_TABLEFMT=simple
        ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME='Llama2 70B Chat'
        ASSISTANTS_RETRY_ATTEMPTS=3
        ASSISTANTS_RETRY_BASE_DELAY=0.75
        ASSISTANTS_RETRY_MAX_DELAY=60
        ASSISTANTS_DEBUG=0
        ASSISTANTS_ENABLE_RICH_PRINT=1
        malformed line

        >>> load_current_config(Path('test/sample-ica-config-malformed.env'))
        {'ASSISTANTS_BASE_URL': 'https://servicesessentials.ibm.com/apis/v1/sidekick-ai', 'ASSISTANTS_APP_ID': 'xxx', 'ASSISTANTS_API_KEY': 'yyy', 'ASSISTANTS_ACCESS_TOKEN': 'zzz', 'ASSISTANTS_CACHE_DURATION_HOURS': '24', 'ASSISTANTS_DEFAULT_FORMAT': 'table', 'ASSISTANTS_TABLEFMT': 'simple', 'ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME': 'Llama2 70B Chat', 'ASSISTANTS_RETRY_ATTEMPTS': '3', 'ASSISTANTS_RETRY_BASE_DELAY': '0.75', 'ASSISTANTS_RETRY_MAX_DELAY': '60', 'ASSISTANTS_DEBUG': '0', 'ASSISTANTS_ENABLE_RICH_PRINT': '1'}

    Note:
        The function assumes that the configuration file has lines in the format 'key=value'.
        Lines that do not follow this format are skipped and a message is printed.
    """
    current_config = {}
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as file:
            for line in file:
                # Ignore comments: split the line at the first '#' and take the first part
                line = line.split("#", 1)[0].strip()
                if "=" not in line:
                    continue  # Skip lines without '='
                try:
                    key, value = line.split("=", 1)
                    # Further clean value: strip spaces and surrounding single or double quotes
                    value = value.strip().strip("'\"")
                    current_config[key] = value
                except ValueError:
                    # Optionally log an error or warning about a malformed line
                    safe_print(f"[orange]Skipping malformed line in config: {line}")
    return current_config


# Create config file
def setup_config(output: Optional[str] = None) -> None:
    """
    Set up the configuration file for the application.

    If a configuration file already exists, a backup is created.
    Existing configuration values are loaded and potentially overwritten with new values.

    Args:
        output (Optional[str], optional): The path where to create the configuration file.
            Uses settings.assistants_config_file_location.
            If not assigned, it defaults to "~/.config/icacli/.ica.env". Defaults to None.

    Examples:
        >>> setup_config(Path('test/new-config.env')) # doctest: +SKIP

    Note:
        The function makes a backup of the existing configuration file before overwriting it with new values.
        This is an interactive function, which requires user input from the terminal.
        This is tested by the expect based unit test in `test/test_setup_config.py`
    """
    if output:
        config_path = Path(output)
    else:
        config_path = Path(
            settings.assistants_config_file_location
            if settings.assistants_config_file_location
            else "~/.config/icacli/.ica.env"
        )
    logging.debug(f"config_path is: {config_path}")
    backup_path = config_path.with_suffix(".env.bak")

    config_exists = config_path.exists()

    if config_exists:
        # Make a backup of the existing config file
        copyfile(config_path, backup_path)
        safe_print(f"[green]Backup created at:[/green] {backup_path}")

    current_config = load_current_config(config_path)

    # Configuration options with descriptions and optional defaults
    config_options = {
        "ASSISTANTS_DEBUG": (
            "Enable DEBUG mode.",
            0,
            False,
        ),
        "ASSISTANTS_ENABLE_RICH_PRINT": (
            "Enable color rich printing in CLI output.",
            1,
            False,
        ),
        "ASSISTANTS_CACHE_DIRECTORY": (
            "Assistants cache directory, used to cache models, tags, assistants, prompts and collections.",
            "~/.config/icacli/cache",
            False,
        ),
        "ASSISTANTS_BASE_URL": (
            "Base URL for the Assistants API.",
            "https://servicesessentials.ibm.com/apis/v1/sidekick-ai",
            False,
        ),
        "ASSISTANTS_APP_ID": (
            "Application ID for accessing the Assistants API.",
            None,
            True,
        ),  # True indicates sensitive info
        "ASSISTANTS_API_KEY": (
            "API key for authenticating with the Assistants API.",
            None,
            True,
        ),
        "ASSISTANTS_ACCESS_TOKEN": (
            "Access token for using the Assistants API.",
            None,
            True,
        ),
        "ASSISTANTS_CACHE_DURATION_HOURS": (
            "Default cache duration in hours.",
            "24",
            False,
        ),
        "ASSISTANTS_DEFAULT_FORMAT": (
            "Default table output format (json, table).",
            "table",
            False,
        ),
        "ASSISTANTS_TABLEFMT": (
            "Default table format type when using table format (github, simple, tsv, html, fancy_grid, grid).",
            "grid",
            False,
        ),
        "ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME": (
            "Default model id or name. Ex: 'Llama2 70B Chat' or 'Mixtral 8x7b Instruct'",
            "Llama2 70B Chat",
            False,
        ),
        "ASSISTANTS_RETRY_ATTEMPTS": (
            "Number of retry attempts for API calls.",
            "3",
            False,
        ),
        "ASSISTANTS_RETRY_BASE_DELAY": (
            "Base delay in seconds for exponential backoff in retries mechanism.",
            "0.5",
            False,
        ),
        "ASSISTANTS_RETRY_MAX_DELAY": (
            "Maximum delay in seconds for exponential backoff in retries mechanism.",
            "60.0",
            False,
        ),
    }

    # Process config_options for setup_config interactive prompt
    for option, (description, default, sensitive) in config_options.items():
        current_value = current_config.get(option, "")
        if sensitive and current_value:
            prompt = f"{option} {description} (current value hidden, press Enter to keep): "
            value = getpass(prompt=prompt)
        else:
            prompt = f"{option} {description} ({'Optional' if default is not None else 'Required'}, current: '{current_value if current_value else 'None'}'): "
            value = input(prompt)

        # Only update if a new value is provided
        if value.strip():
            current_config[option] = value.strip()
        elif not current_value and default is not None:
            # Assign default if no current value and default is specified
            current_config[option] = str(default)

    confirmation = input(
        f"Are you sure you want to update the configuration file {config_path}? Type 'yes' to confirm: "
    )
    if confirmation.lower() == "yes":
        if not config_exists:
            config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w", encoding="utf-8") as config_file:
            for option, value in current_config.items():
                config_file.write(f"{option}={value}\n")
        safe_print(f"[green]Configuration has been updated: {config_path}")
    else:
        safe_print("[yellow]Configuration update canceled.")


# Function to configure signal and error handling
def setup_broken_pipe_handling():
    """
    Configure signal and error handling for the program by ignoring the SIGPIPE signal.

    This prevents BrokenPipeErrors during program execution.

    Examples:
        >>> setup_broken_pipe_handling() # No output means the setup was successful.

    Note:
        This function modifies the global signal handling configuration of the program,
        which can affect other parts of the program as well.
    """
    # Ignore SIGPIPE signal to prevent BrokenPipeErrors during program execution
    try:
        signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    except AttributeError:
        pass  # not supported on Windows


def safe_print(*args, **kwargs) -> None:
    """
    Attempt to print arguments safely using rich print, catching BrokenPipeError and MarkupError.

    If `assistants_enable_rich_print` is False, it falls back to the standard print function.

    This function was created to catch tags such as [/INST] in LLM prompts,
    which would cause the rich_print to trigger an error.

    Args:
        *args: Variable length argument list to be printed.
        **kwargs: Arbitrary keyword arguments to be passed to the print function.

    Examples:
        >>> safe_print('Hello, world!')
        Hello, world!

        # Assuming `assistants_enable_rich_print` is True and `rich_print` can print in color
        >>> print('doctest'); safe_print('[red]Hello, world![/red]')  # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
        doctest ...

        >>> safe_print('[/red]Hello, world![/red]') # Incorrect tags cause the function to revert back to using a regular print
        [/red]Hello, world![/red]

    Note:
        This function modifies the global stdout and stderr streams in case of a BrokenPipeError,
        which can affect other parts of the program as well.
    """
    if not settings.assistants_enable_rich_print:
        try:
            print(*args, **kwargs)
        except BrokenPipeError:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            os._exit(0)
        return
    try:
        rich_print(*args, **kwargs)
    except BrokenPipeError:
        # Directly exit to avoid broken pipe error messages
        # Restore stdout/stderr to original state to clean up properly
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        os._exit(0)
    except Exception:
        try:
            print(*args, **kwargs)
        except BrokenPipeError:
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__
            os._exit(0)


def parse_row_limit(row_limit_str: str) -> slice:
    """
    Parse a row limit string and returns a slice object representing the limit.

    This function is used by `icacli --rows` to return specific rows.

    Args:
        row_limit_str (str): A string representing a maximum number of rows ('10') or a row range ('5,10').

    Returns:
        slice: A slice object representing the row limit or range.

    Examples:
        >>> parse_row_limit('10')
        slice(None, 10, None)

        >>> parse_row_limit('5,10')
        slice(4, 10, None)

    Note:
        The function assumes that the input is either a single integer or two integers separated by a comma.
        If the input does not meet these criteria, the function will raise a ValueError.
        The user input is assumed to be 1-indexed, so the function subtracts 1 from the start index.
    """
    if "," in row_limit_str:
        start, end = row_limit_str.split(",", 1)
        return slice(int(start) - 1, int(end))  # -1 because user input is 1-indexed
    return slice(int(row_limit_str))


def handle_execute_prompt_response(response: Dict, retrieve_chunks: bool) -> None:
    """
    Handle and print the response for the execute_prompt command.

    Args:
        response (dict): The response dictionary from the execute_prompt API call.
        retrieve_chunks (bool): Whether to retrieve and display chunks.

    Examples:
        >>> handle_execute_prompt_response({"response": "test"})
        test
        >>> try:
        ...     handle_execute_prompt_response({'error': 'handle_execute_prompt_response doctest'}) # Prints "handle_execute_prompt_response doctest" in red and exits the program.
        ... except SystemExit:
        ...     print("handle_execute_prompt_response doctest")
        handle_execute_prompt_response doctest
        # Test chunks
        >>> handle_execute_prompt_response({"response": "test", "responseChunks": [{"chunk": "test chunk"}]}, True)
        test
        Chunks:
        - test chunk

        >>> handle_execute_prompt_response({"response": "test"}, False)

    Note:
        The function assumes that the response dictionary has either an 'error' key or a 'response' key.
        If the 'error' key is present, the function prints the error message and exits the program.
        If the 'response' key is present, the function prints the response message after stripping any leading or trailing whitespace.
    """
    if "error" in response:
        safe_print(f"[red]Error: {response['error']}", file=sys.stderr)
        sys.exit(1)
    else:
        # Print the response
        print(response["response"].strip())

        # Print chunks if requested and available
        if retrieve_chunks and "responseChunks" in response:
            print("Chunks:")
            for chunk in response["responseChunks"]:
                print(f"- {chunk['chunk']}")


def handle_execute_prompt_async_response(response: Dict[str, str]) -> None:
    """
    Handle and print the response for the execute_prompt_async command.

    Args:
        response (str): The response from the execute_prompt API call.

    Examples:
        >>> handle_execute_prompt_async_response('123')
        123

        >>> try:
        ...     handle_execute_prompt_async_response(None)
        ... except SystemExit:
        ...     print("handle_execute_prompt_async_response doctest")
        handle_execute_prompt_async_response doctest
    """
    if response is None:
        safe_print(
            "[red]Error receiving transactionId from execute_prompt_async",
            file=sys.stderr,
        )
        sys.exit(1)
    print(response)


def handle_create_prompt_response(response: Dict[str, str]) -> None:
    """
    Handle and print the response for the create_prompt command.

    Args:
        response (Dict[str, str]): The response dictionary from the create_prompt API call.

    Examples:
        >>> try:
        ...     handle_create_prompt_response({'error': 'handle_create_prompt_response doctest'}) # Prints "handle_create_prompt_response doctest" in red and exits the program.
        ... except SystemExit:
        ...     print("handle_create_prompt_response doctest")
        handle_create_prompt_response doctest

        >>> handle_create_prompt_response({'response': 'Prompt created successfully.'})
        {
            "response": "Prompt created successfully."
        }

    Note:
        The function assumes that the response dictionary has either an 'error' key or a 'response' key.
        If the 'error' key is present, the function prints the error message and exits the program.
        If the 'response' key is present, the function prints the entire response dictionary in JSON format.
    """
    if "error" in response:
        safe_print(f"[red]Error: {response['error']}", file=sys.stderr)
        sys.exit(1)
    else:
        # Print the response in JSON format for success
        logging.debug("Prompt creation successful. Response:")
        print(json.dumps(response, indent=4))


def handle_get_transaction_response(response):
    """
    Handle and print the response for the get_transaction_response command.

    Args:
        response (Dict[str, str]): The response dictionary from the get_transaction_response API call.

    Examples:
        >>> try:
        ...     handle_get_transaction_response({'error': 'handle_get_transaction_response doctest'}) # Prints "handle_get_transaction_response doctest" in red and exits the program.
        ... except SystemExit:
        ...     print("handle_get_transaction_response doctest")
        handle_get_transaction_response doctest

        >>> handle_get_transaction_response({'response': 'Transaction details.'})# Prints "Transaction details.".
        Transaction details.

    Note:
        The function assumes that the response dictionary has either an 'error' key or a 'response' key.
        If the 'error' key is present, the function prints the error message and exits the program.
        If the 'response' key is present, the function prints the response message after stripping any leading or trailing whitespace.
    """
    if "error" in response:
        safe_print(f"[red]Error: {response['error']}", file=sys.stderr)
        sys.exit(1)
    else:
        print(response["response"].strip())


def execute_api_command(client: "ICAClient", func_name: str, **kwargs: Any) -> None:
    """
    Execute an Assistant extensions API command with the given arguments and print the result.

    Args:
        client (ICAClient): The API client instance.
        func_name (str): The name of the ICAClient method to call.
        **kwargs: Arbitrary keyword arguments to pass to the API method.
            These can include:
                - 'format': The output format. If not provided, defaults to `settings.assistants_default_format`.
                - 'columns': Custom columns for the output. If not provided, defaults to None.
                - 'rows': The number of rows to limit the output to. If not provided, defaults to None.
                - 'retrieve_chunks': Whether to retrieve and display chunks. If not provided, defaults to False.

    Examples:
        >>> client = ICAClient()
        >>> execute_api_command(client, 'get_models', format='json') # doctest: +ELLIPSIS
        [...]

    Note:
        The function assumes that 'func_name' is a valid method of 'client'.
        If it is not, the function will raise an AttributeError.
        The function also assumes that the method can be called with the provided keyword arguments.
        If it cannot, the function will raise a TypeError.
    """
    output_format = kwargs.pop("format", settings.assistants_default_format)
    custom_columns = kwargs.pop("columns", None)
    row_limit_str = kwargs.pop("rows", None)
    retrieve_chunks = kwargs.pop("retrieve_chunks", False)

    # Parse 'parameters' JSON string to dictionary if present
    if "parameters" in kwargs and kwargs["parameters"]:
        try:
            kwargs["parameters"] = json.loads(kwargs["parameters"])
        except json.JSONDecodeError:
            logging.error("Failed to parse parameters as JSON.")
            safe_print("[red]Error: Failed to parse 'parameters' as JSON. Ensure it is correctly formatted.")
            sys.exit(1)

    try:
        api_method = getattr(client, func_name)
        response = api_method(**kwargs)

        # Custom handling for specific functions like execute_prompt
        if func_name in [
            "execute_prompt",
            "execute_prompt_async",
            "create_prompt",
            "get_transaction_response",
        ]:
            special_handlers = {
                "execute_prompt": handle_execute_prompt_response,
                "execute_prompt_async": handle_execute_prompt_async_response,
                "create_prompt": handle_create_prompt_response,
                "get_transaction_response": handle_get_transaction_response,
            }
            special_handlers[func_name](response, retrieve_chunks)
            return  # Exit after special handling to avoid the general response printing logic

        # Handle general case for commands output
        if isinstance(response, str):
            safe_print(response)
        elif output_format == "json":
            print(json.dumps(response, indent=4))
        elif output_format == "table":
            columns = None
            if custom_columns == "*":
                if func_name == "get_collections":
                    if (
                        "collections" in response
                        and isinstance(response["collections"], list)
                        and response["collections"]
                    ):
                        columns = sorted({k for item in response["collections"] for k in item.keys()})
                elif func_name in ["get_tags", "get_roles"]:
                    # No dynamic columns to determine; handled separately below
                    pass
                else:
                    if isinstance(response, list) and all(isinstance(item, dict) for item in response):
                        columns = sorted({k for item in response for k in item.keys()})
                    elif isinstance(response, dict):
                        columns = sorted(response.keys())
                    else:
                        columns = ["value"]
                        response = [{"value": response}]  # Ensure response is list of dicts for tabulation
            else:
                columns = custom_columns.split(",") if custom_columns else default_columns.get(func_name, [])

            # Handling row limits
            if row_limit_str:
                row_limit = parse_row_limit(row_limit_str)
                if isinstance(response, list):
                    response = response[row_limit]
                elif func_name == "get_collections" and "collections" in response:
                    response["collections"] = response["collections"][row_limit]

            # Handle get_tabs and get_roles
            if func_name in ["get_tags", "get_roles"]:
                items = response if isinstance(response, list) else []
                column_name = "Tag" if func_name == "get_tags" else "Role"
                table_data = [[item] for item in items]
                safe_print(
                    tabulate(
                        table_data,
                        headers=[column_name],
                        tablefmt=settings.assistants_tablefmt,
                    )
                )
            else:
                # Prepare table data for all other commands
                table_data = []

                # Validate: Check if no columns are returned
                if columns is None:
                    columns = ["Column"]

                # Validate: Check if response has any data
                if response is None:
                    safe_print("[red]Error: No data available to display.")
                else:
                    if isinstance(response, dict) and func_name == "get_collections":
                        collections = response.get(
                            "collections", []
                        )  # pyright error: Cannot access attribute "get" for class "list[dict[str, Any | list[Unknown]]]"
                        table_data = [[collection.get(col, "") for col in columns] for collection in collections]
                    elif isinstance(response, list) and all(isinstance(item, dict) for item in response):
                        table_data = [[item.get(col, "") for col in columns] for item in response]
                    elif isinstance(response, dict):
                        table_data = [[response.get(col, "") for col in columns]]
                    else:
                        table_data = [[item.get(col, "") for col in columns] for item in response]

                safe_print(
                    tabulate(
                        table_data,
                        headers=columns,
                        tablefmt=settings.assistants_tablefmt,
                    )
                )
    except Exception as exception:
        logging.error(f"Error executing {func_name}: {exception}")
        safe_print(f"[red]Error: {exception}")
        sys.exit(1)


# Sets the default flag for model_id_or_name only when other flags are not set
class EnsureDefaultModelID(argparse.Action):
    """
    Custom argparse action that sets the default flag for `model_id_or_name` only when other related flags are not set.

    This action sets the value of `model_id_or_name` based on the command line input. If neither `assistant_id` nor `collection_id`
    is provided, it assigns a default value from settings, specifically `settings.assistants_default_model_id_or_name`.

    The action ensures that defaults are applied sensibly when dependencies between command line arguments exist.

    Examples:
        >>> parser = argparse.ArgumentParser()
        >>> parser.add_argument('--model', action=EnsureDefaultModelID)  # doctest: +ELLIPSIS
        EnsureDefaultModelID...
        >>> parser.add_argument('--assistant_id', action='store')  # doctest: +ELLIPSIS
        _StoreAction...
        >>> parser.add_argument('--collection_id', action='store')  # doctest: +ELLIPSIS
        _StoreAction...
        >>> args = parser.parse_args(['--model', 'my_model'])
        >>> args.model
        'my_model'
    """

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Optional[str] = None,
    ) -> None:
        """
        Set the command-line argument value, and apply a default if other related flags are not set.

        Args:
            parser (argparse.ArgumentParser): The parser that this action belongs to.
            namespace (argparse.Namespace): The namespace where parsed values are stored.
            values (Union[str, Sequence[Any], None]): The values associated with the command-line argument.
            option_string (Optional[str]): The option string that triggered this action (e.g., '--model').
        """
        # Set the provided value to the namespace at the destination key.
        setattr(namespace, self.dest, values)
        # If no values are provided for assistant_id and collection_id, and if they have not been set in the namespace, apply the default value.
        if not hasattr(namespace, "assistant_id") and not hasattr(namespace, "collection_id"):
            setattr(
                namespace,
                self.dest,
                values if values is not None else settings.assistants_default_model_id_or_name,
            )


class CustomFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """
    Custom argparse formatter.

    Combines displaying argument defaults with preserving the formatting of the description and epilog for help messages.

    Examples:
        >>> parser = argparse.ArgumentParser(formatter_class=CustomFormatter)
        >>> parser.add_argument('--model', default='default_model') # doctest: +ELLIPSIS
        _StoreAction...
        >>> parser.print_help()  # doctest: +ELLIPSIS
        usage:...

    Note:
        Using ELLIPSIS because the output of `print_help`
        includes the script name, which can vary depending on the environment.
    """

    def _fill_text(self, text: str, width: int, indent: str) -> str:
        """Handle text formatting to preserve raw texts for description and epilog."""
        return "".join(indent + line for line in text.splitlines(keepends=True))

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """
        Initialize the CustomFormatter.

        This method allows the class to accept any arguments and keyword arguments that the parent class supports.
        """
        super().__init__(*args, **kwargs)


def setup_parser():
    """Return argparse parser."""
    parser = argparse.ArgumentParser(
        description="IBM Consulting Assistants - API CLI Tool: A command-line interface for interacting with the extensions API.",
        epilog=f"""EXAMPLE:
icacli setup-config # Creates or edits {settings.assistants_config_file_location}
icacli get-models --columns="id,name" --rows=5,10
icacli prompt --prompt "What is OpenShift" --model_id_or_name="Mixtral 8x7b Instruct"

AUTOCOMPLETE: activate-global-python-argcomplete --user; eval "$(register-python-argcomplete icacli)"
AUTHORS: Mihai Criveti <crmihai1@ie.ibm.com>
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Add the --format argument globally
    parser.add_argument(
        "--format",
        choices=["table", "json"],
        default=settings.assistants_default_format,
        help="Output format (default: %(default)s).",
    )

    subparsers = parser.add_subparsers(help="commands", dest="command")

    # Dynamically create subparsers based on ICAClient methods
    commands = {
        "get_models": {
            "description": "Retrieve a list of available models, allowing for specification of columns and control over pagination.",
            "options": {
                "refresh_data": {
                    "action": "store_true",
                    "help": "Force re-reading data from the API, bypassing the cache.",
                },
                "columns": {
                    "type": str,
                    "help": "Comma-separated list of columns to display.",
                },
                "rows": {
                    "type": str,
                    "help": "Maximum number of rows or row range to display (e.g., '10' or '5,10').",
                },
            },
        },
        "get_tags": {
            "description": "Fetch a list of tags used within the system. Allows for pagination.",
            "options": {
                "refresh_data": {
                    "action": "store_true",
                    "help": "Bypass cached data and directly fetch the latest data from the API.",
                },
                "rows": {
                    "type": str,
                    "help": "Specify the maximum number of rows to return or a range of rows (e.g., '10' or '5,10').",
                },
            },
        },
        "get_roles": {
            "description": "List all roles available, with options to control output volume through pagination.",
            "options": {
                "refresh_data": {
                    "action": "store_true",
                    "help": "Ignore cache to ensure the data is fetched live from the API.",
                },
                "rows": {
                    "type": str,
                    "help": "Limit the output to a specified number of rows or a row range (e.g., '10' or '5,10').",
                },
            },
        },
        "get_prompts": {
            "description": "Retrieve stored prompts, optionally filtered by tags and roles, with pagination support.",
            "options": {
                "tags": {
                    "nargs": "*",
                    "help": "Filter prompts by specifying one or more tags.",
                },
                "roles": {
                    "nargs": "*",
                    "help": "Filter prompts by specifying one or more roles.",
                },
                "refresh_data": {
                    "action": "store_true",
                    "help": "Force a fresh fetch of prompts from the API, bypassing any cached data.",
                },
                "columns": {
                    "type": str,
                    "help": "Specify columns to display in a comma-separated list (e.g., 'promptId,prompt').",
                },
                "rows": {
                    "type": str,
                    "help": "Control the number of prompts displayed with a maximum count or range (e.g., '10' or '5,10').",
                },
            },
        },
        "get_assistants": {
            "description": "Fetch a list of assistants, with options to filter by tags and roles and to control the output format and volume.",
            "options": {
                "tags": {
                    "nargs": "*",
                    "help": "Filter assistants by tags. Multiple tags can be specified.",
                },
                "roles": {
                    "nargs": "*",
                    "help": "Filter assistants based on roles. Multiple roles can be specified.",
                },
                "refresh_data": {
                    "action": "store_true",
                    "help": "Ensure the latest data is retrieved by bypassing cache.",
                },
                "columns": {
                    "type": str,
                    "help": "Columns to include in the output, specified in a comma-separated list.",
                },
                "rows": {
                    "type": str,
                    "help": "Set a limit on the number of rows to show, or specify a range (e.g., '10' or '5,10').",
                },
            },
        },
        "get_collections": {
            "description": "List collections in the system, including details such as IDs, names, and status, with pagination options.",
            "options": {
                "refresh_data": {
                    "action": "store_true",
                    "help": "Access the latest collection data directly from the API, skipping cache.",
                },
                "columns": {
                    "type": str,
                    "help": "Choose specific columns for the output. Specify them in a comma-separated list.",
                },
                "rows": {
                    "type": str,
                    "help": "Define the output's row limit or range (e.g., '10' or '5,10').",
                },
            },
        },
        "create_chat_id": {
            "description": "Creates a new chat session ID that can be used to manage and persist context across multiple interactions.",
            "options": {
                "model_id_or_name": {
                    "required": False,
                    "help": "Specify the model ID or name for the chat session.",
                },
                "assistant_id": {
                    "required": False,
                    "help": "Specify the assistant ID to use.",
                },
                "collection_id": {
                    "required": False,
                    "help": "Specify the collection ID for the session.",
                },
                "refresh_data": {
                    "action": "store_true",
                    "help": "Force re-reading data from the API, bypassing the cache.",
                },
            },
        },
        "remove_chat_id": {
            "description": "Deletes a specific chat session ID, clearing any stored context or history associated with it.",
            "options": {"chat_id": {"required": True, "help": "Specify the chat ID to delete."}},
        },
        "execute_prompt": {
            "description": "Executes a given prompt against a specified chat session, model, assistant, or collection.",
            "options": {
                "prompt": {"required": True, "help": "The prompt text to execute."},
                "chat_id": {
                    "required": True,
                    "help": "Specify the chat ID for context.",
                },
                "model_id_or_name": {
                    "required": False,
                    "help": "Specify the model ID or name.",
                },
                "assistant_id": {
                    "required": False,
                    "help": "Specify the assistant ID.",
                },
                "collection_id": {
                    "required": False,
                    "help": "Specify the collection ID.",
                },
                "system_prompt": {
                    "required": False,
                    "help": "Specify a system prompt if applicable.",
                },
                "parameters": {
                    "required": False,
                    "help": 'A JSON string of parameters to pass to the model. Example: \'{"parameter1": "value1", "parameter2": 2}\'',
                },
                "substitution_parameters": {
                    "required": False,
                    "help": 'A JSON string of substitution parameters to pass to the model. Example: \'{"parameter1": "value1", "parameter2": 2}\'',
                },
                "refresh_data": {
                    "action": "store_true",
                    "help": "Force re-reading data from the API, bypassing the cache.",
                },
            },
        },
        "execute_prompt_async": {
            "description": "Executes a prompt asynchronously, allowing for operations that might take longer to complete.",
            "options": {
                "prompt": {"required": True, "help": "The prompt text to execute."},
                "chat_id": {
                    "required": True,
                    "help": "Specify the chat ID for context.",
                },
                "model_id_or_name": {
                    "required": False,
                    "help": "Specify the model ID or name.",
                },
                "assistant_id": {
                    "required": False,
                    "help": "Specify the assistant ID.",
                },
                "collection_id": {
                    "required": False,
                    "help": "Specify the collection ID.",
                },
                "system_prompt": {
                    "required": False,
                    "help": "Specify a system prompt if applicable.",
                },
                "parameters": {
                    "required": False,
                    "help": 'A JSON string of parameters to pass to the model. Example: \'{"parameter1": "value1", "parameter2": 2}\'',
                },
                "substitution_parameters": {
                    "required": False,
                    "help": 'A JSON string of substitution parameters to pass to the model. Example: \'{"parameter1": "value1", "parameter2": 2}\'',
                },
                "refresh_data": {
                    "action": "store_true",
                    "help": "Force re-reading data from the API, bypassing the cache.",
                },
            },
        },
        "get_transaction_response": {
            "description": "Retrieves the response for a previously executed asynchronous prompt by its transaction ID.",
            "options": {
                "transaction_id": {
                    "required": True,
                    "help": "The transaction ID to retrieve the response for.",
                }
            },
        },
        "create_prompt": {
            "description": "Allows for the creation of a new prompt, specifying its scope, title, description, and optional response.",
            "options": {
                "scope": {"required": True, "help": "Specify the scope of the prompt."},
                "prompt_title": {"required": True, "help": "Title for the prompt."},
                "model_id_or_name": {
                    "required": True,
                    "help": "Specify the model ID or name.",
                },
                "prompt_description": {
                    "required": True,
                    "help": "Description of the prompt.",
                },
                "prompt": {"required": True, "help": "The text of the prompt."},
                "prompt_response": {
                    "required": False,
                    "help": "The expected response for the prompt.",
                },
                "refresh_data": {
                    "action": "store_true",
                    "help": "Force re-reading data from the API, bypassing the cache.",
                },
            },
        },
    }

    # Parse the list of commands, displaying the help
    for cmd, details in commands.items():
        cmd_description = details.get("description", f"{cmd} command.")  # Fallback description
        cmd_options = details.get("options", {})

        cmd_parser = subparsers.add_parser(
            cmd.replace("_", "-"),
            help=cmd_description,  # This brief help appears in the list of all commands
            description=cmd_description,  # This detailed description is shown in the --help for the command
            formatter_class=CustomFormatter,
        )

        if not isinstance(cmd_options, dict):
            raise TypeError(f"Expected cmd_options: {cmd_options} to be a dictionary, instead got: {type(cmd_options)}")

        for param, config in cmd_options.items():
            cmd_parser.add_argument(f"--{param}", **config)

        cmd_parser.set_defaults(func=execute_api_command, func_name=cmd)

    # Prompt parser for the prompt command. This uses prompt_flow to execute everything in one go
    prompt_parser = subparsers.add_parser(
        "prompt",
        help="Execute a prompt with automatic chat ID management.",
        formatter_class=CustomFormatter,
    )
    prompt_parser.add_argument("--assistant-id", required=False, help="The assistant ID to use.")
    prompt_parser.add_argument("--collection-id", required=False, help="The assistant ID to use.")
    # --model_id_or_name needs to be defined after the --asistantiid and --collection-id
    prompt_parser.add_argument(
        "--model_id_or_name",
        required=False,
        default=settings.assistants_default_model_id_or_name,
        help="The model ID or model name to use.",
    )
    prompt_parser.add_argument(
        "--prompt",
        nargs="?",
        type=str,
        default=None,
        help="The prompt to execute. If not provided, will read from stdin.",
    )
    prompt_parser.add_argument(
        "--prompt-file",
        required=False,
        type=str,
        help="Path to a file containing the prompt text. This option is mutually exclusive with --prompt.",
    )
    prompt_parser.add_argument("--system-prompt", required=False, help="The system prompt to use.", default="")
    prompt_parser.add_argument(
        "--system-prompt-file",
        required=False,
        type=str,
        help="Path to a file containing the system prompt text. This option is mutually exclusive with --system-prompt.",
    )
    prompt_parser.add_argument(
        "--parameters",
        required=False,
        help='A JSON string of parameters to pass to the model. Example: \'{"parameter1": "value1", "parameter2": 2}\'',
    )
    prompt_parser.add_argument(
        "--substitution_parameters",
        required=False,
        help='A JSON string of substitution parameters to pass to the model. Example: \'{"parameter1": "value1", "parameter2": 2}\'',
    )
    prompt_parser.add_argument(
        "--document-names",
        required=False,
        help='A list of documents to search. Example: ["document1", "document2"]',
    )
    prompt_parser.add_argument(
        "--refresh_data",
        action="store_true",
        help="Force re-reading data from the API, bypassing the cache.",
    )

    # Add setup-config as its own subcommand
    setup_config_parser = subparsers.add_parser(
        "setup-config",
        help="Setup or update the configuration file.",
        formatter_class=CustomFormatter,
    )
    setup_config_parser.add_argument(
        "--output",
        type=str,
        help=f"Output file path for the configuration. Default is {settings.assistants_config_file_location}",
    )
    setup_config_parser.set_defaults(func=setup_config)

    # Version

    # Interactive prompt parser for the interactive command
    interactive_parser = subparsers.add_parser(
        "interactive",
        help="Enter an interactive REPL for executing prompts.",
        formatter_class=CustomFormatter,
    )
    interactive_parser.add_argument("--assistant-id", required=False, help="The assistant ID to use.")
    interactive_parser.add_argument("--collection-id", required=False, help="The collection ID to use.")
    interactive_parser.add_argument(
        "--model_id_or_name",
        required=False,
        default=settings.assistants_default_model_id_or_name,
        help="The model ID or model name to use.",
    )
    interactive_parser.add_argument("--system-prompt", required=False, help="The system prompt to use.", default="")
    interactive_parser.add_argument(
        "--parameters",
        required=False,
        help='A JSON string of parameters to pass to the model. Example: \'{"parameter1": "value1", "parameter2": 2}\'',
    )
    interactive_parser.add_argument(
        "--substitution_parameters",
        required=False,
        help='A JSON string of substitution parameters to pass to the model. Example: \'{"parameter1": "value1", "parameter2": 2}\'',
    )
    interactive_parser.add_argument(
        "--refresh_data",
        action="store_true",
        help="Force re-reading data from the API, bypassing the cache.",
    )

    # Version flag
    libica_version = version("libica")
    icacli_version = f"""icacli {libica_version} using libica {libica_version}
IBM Consulting Assistants Extension API - Python cli and library
"""
    parser.add_argument("-v", "--version", action="version", version=icacli_version)

    # Parse arguments from the command line
    argcomplete.autocomplete(parser)  # setup autocomplete using argcomplete
    args = parser.parse_args()

    # Check if required settings are present unless running setup-config
    if "command" in args and getattr(args, "command", None) != "setup-config":
        check_settings(settings)

    # Set the defaults to only set a default model when collection-id or assistant-id are not set.
    if "command" in args and getattr(args, "command", None) == "prompt":
        assistant_id_present = getattr(args, "assistant_id", None) is not None
        collection_id_present = getattr(args, "collection_id", None) is not None

        if not assistant_id_present and not collection_id_present:
            # If neither assistant-id nor collection-id was provided, check model_id_or_name
            if getattr(args, "model_id_or_name", None) is None:
                args.model_id_or_name = settings.assistants_default_model_id_or_name
        else:
            # If assistant-id or collection-id was provided, unset model_id_or_name to ensure exclusivity
            args.model_id_or_name = None

    # Special handling for 'setup-config' command
    if getattr(args, "command", None) == "setup-config":
        setup_config(output=args.output)
        return None  # Exit after handling setup-config to prevent further processing

    # Check for and handle the 'prompt' command to do everything in one go
    if args.command:
        client = ICAClient()
        # Process interactive command
        if args.command == "interactive":
            interactive_prompt_flow(client, args)
            return None  # Exit after handling interactive to prevent further processing

        # Process prompt command. Ensure only one context is set for the 'prompt' command
        if args.command == "prompt" and (args.model_id_or_name or args.assistant_id or args.collection_id):
            prompt = args.prompt
            system_prompt = args.system_prompt
            if args.system_prompt_file:
                try:
                    with open(args.system_prompt_file, "r", encoding="utf-8") as file:
                        system_prompt = file.read().strip()
                except FileNotFoundError:
                    print(
                        f"[red]Error: The file specified in --system-prompt-file does not exist: {args.system_prompt_file}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
            if args.prompt_file:
                try:
                    with open(args.prompt_file, "r", encoding="utf-8") as file:
                        prompt = file.read().strip()
                except FileNotFoundError:
                    print(
                        f"[red]Error: The file specified in --prompt-file does not exist: {args.prompt_file}",
                        file=sys.stderr,
                    )
                    sys.exit(1)
            elif prompt is None:
                # If no prompt is provided as an argument, try to read from stdin
                if not sys.stdin.isatty():
                    prompt = sys.stdin.read().strip()
                else:
                    print(
                        "[red]Error: No prompt provided via --prompt or --prompt-file, and stdin is empty.",
                        file=sys.stderr,
                    )
                    sys.exit(1)
            # Special handling for the 'prompt' subcommand
            # Wrap the call to prompt_flow in a try-except block to catch exceptions
            try:
                # Parameters
                if hasattr(args, "parameters") and args.parameters:
                    try:
                        parameters_dict = json.loads(args.parameters)
                    except json.JSONDecodeError:
                        print("[red]Error: Failed to parse 'parameters' as JSON. Ensure it is correctly formatted.")
                        sys.exit(1)
                else:
                    parameters_dict = None
                # Substitution parameters
                if hasattr(args, "substitution_parameters") and args.substitution_parameters:
                    try:
                        substitution_parameters_dict = json.loads(args.substitution_parameters)
                    except json.JSONDecodeError:
                        print(
                            "[red]Error: Failed to parse 'substitution_parameters' as JSON. Ensure it is correctly formatted."
                        )
                        sys.exit(1)
                else:
                    substitution_parameters_dict = None
                # Documents list
                if hasattr(args, "document_names") and args.document_names:
                    try:
                        document_names_list = json.loads(args.document_names)
                    except json.JSONDecodeError:
                        print("[red]Error: Failed to parse 'document_names' as JSON. Ensure it is correctly formatted.")
                        sys.exit(1)
                else:
                    document_names_list = None
                prompt_output = client.prompt_flow(
                    system_prompt=system_prompt,
                    model_id_or_name=args.model_id_or_name,
                    assistant_id=args.assistant_id,
                    collection_id=args.collection_id,
                    document_names=document_names_list,
                    prompt=prompt,
                    parameters=parameters_dict,
                    substitution_parameters=substitution_parameters_dict,
                )
                # Currently the API adds an extra space to the left of the output, this should be addressed by the API
                safe_print(str(prompt_output).strip())
            except Exception as exception:
                print(f"[red]Failed to execute prompt: {exception}", file=sys.stderr)
                sys.exit(1)
        else:
            # Handle other commands as before
            kwargs = {k: v for k, v in vars(args).items() if k not in ["func", "func_name", "command"]}
            execute_api_command(client, args.func_name, **kwargs)
    else:
        parser.print_help()
    return parser


def main():
    """
    Define main entry point function for the IBM Consulting Assistants - API CLI Tool.

    This function defines the command-line interface for interacting with the extensions API. It sets up commands
    and corresponding arguments using argparse, then executes the appropriate function based on the provided
    command-line arguments. It also contains special handling for 'setup-config', 'prompt', and 'interactive'
    commands. In case of the 'prompt' command, it also reads prompts from either the command line, a file, or stdin.

    This tool provides a variety of commands for interacting with the extensions API, including retrieving model
    lists, getting tags, getting roles, retrieving prompts, fetching assistants, listing collections, creating
    chat sessions, deleting chat sessions, executing prompts, creating prompts, and more.
    """
    setup_parser()


if __name__ == "__main__":
    setup_broken_pipe_handling()
    try:
        main()
    except BrokenPipeError:
        # Directly exit to avoid broken pipe error messages, even if exception occurs outside safe_print
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        os._exit(0)
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        sys.exit(1)
