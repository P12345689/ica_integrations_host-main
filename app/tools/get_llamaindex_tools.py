# -*- coding: utf-8 -*-
"""
Authors: Chris Hay, Mihai Criveti
Description: Tool Management Module to dynamically import tools

This module provides functionalities for dynamically importing and creating tools
from JSON definitions. It includes functions for importing functions or methods,
creating tools from definitions, and retrieving tool definitions.

Example:
    >>> tools = get_tools(['tool1', 'tool2'])
    >>> len(tools)
    2
    >>> tools[0].name
    'tool1'
"""

import importlib
import json
import logging
import os
from typing import Callable, List, Optional
from llama_index.core.tools.function_tool import FunctionTool

from app.tools.global_tools.integration_tool import create_integration_tool


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Set up color logging
class ColorFormatter(logging.Formatter):
    green = "\x1b[32;20m"
    blue = "\x1b[34;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: blue + format_str + reset,
        logging.INFO: green + format_str + reset,
        logging.WARNING: yellow + format_str + reset,
        logging.ERROR: red + format_str + reset,
        logging.CRITICAL: bold_red + format_str + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Add color formatter to logger
color_handler = logging.StreamHandler()
color_handler.setFormatter(ColorFormatter())
logger.addHandler(color_handler)

# Global variable to store tool definitions
_LLAMA_INDEX_TOOL_DEFINITIONS: Optional[List[FunctionTool]] = None

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "default_value")
GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "default_value")


def import_function(
    function_path: str,
    method_name: Optional[str] = None,
    init_args: Optional[dict] = None,
) -> Callable:
    """
    Dynamically import a function or method from a string path.

    Args:
        function_path (str): The dot-separated path to the function or class.
        method_name (Optional[str]): The name of the method if importing from a class.

    Returns:
        Callable: The imported function or method.

    Raises:
        ValueError: If the function path is invalid or the attribute is not callable.
        ModuleNotFoundError: If the specified module cannot be found.
        AttributeError: If the specified attribute cannot be found in the module.

    Example:
        >>> import_function('math.sqrt')
        <built-in function sqrt>
        >>> import_function('collections.Counter', 'update')
        <bound method Counter.update of Counter()>
    """
    try:
        parts = function_path.split(".")

        if len(parts) < 2:
            raise ValueError("Invalid function path")

        module_name = ".".join(parts[:-1])
        class_or_func_name = parts[-1]

        logger.debug(f"Importing module: {module_name} and class/function: {class_or_func_name}")

        module = importlib.import_module(module_name)
        attr = getattr(module, class_or_func_name)

        if callable(attr) and method_name is None:
            logger.debug(f"Successfully imported function: {function_path}")
            return attr

        if method_name:
            if init_args:
                class_instance = attr(**init_args)
            else:
                class_instance = attr()
            method = getattr(class_instance, method_name)
            logger.debug(f"Successfully imported method: {function_path}.{method_name}")
            return method

        raise ValueError("Provided path is not callable or method name is missing")

    except ModuleNotFoundError as e:
        logger.error(f"ModuleNotFoundError: Failed to import module: {module_name}. Error: {e}")
        raise
    except AttributeError as e:
        logger.error(f"AttributeError: Failed to find class/function: {class_or_func_name} or method: {method_name} in module: {module_name}. Error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise


def create_tools_from_definitions(tool_definitions: List[dict], context: Optional[dict] = None) -> List[FunctionTool]:
    """
    Create tools from definitions.

    Args:
        tool_definitions (List[dict]): A list of dictionaries containing tool definitions.

    Returns:
        List[Tool]: A list of created Tool objects.

    Example:
        >>> defs = [{'name': 'test_tool', 'function': 'math.sqrt', 'description': 'Test tool'}]
        >>> tools = create_tools_from_definitions(defs)
        >>> len(tools)
        1
        >>> tools[0].name
        'test_tool'
    """
    tools = []

    for tool_def in tool_definitions:
        logger.debug(f"Creating tool: {tool_def['name']}")
        # if "integration_defintion" in tool_def:
        #     tool = create_integration_tool(
        #         tool_def["name"],
        #         tool_def["integration_defintion"],
        #         tool_def["description"],
        #         context,
        #     )
        #     tools.append(tool)
        #     continue

        init_args = {}
        if "method" in tool_def:
            if "GoogleSearchAPIWrapper" in tool_def["function"]:
                init_args = {
                    "google_api_key": GOOGLE_API_KEY,
                    "google_cse_id": GOOGLE_CSE_ID,
                }
            func = import_function(
                tool_def["function"],
                method_name=tool_def["method"],
                init_args=init_args,
            )
        else:
            if "GoogleSearchAPIWrapper" in tool_def["function"]:
                init_args = {
                    "google_api_key": GOOGLE_API_KEY,
                    "google_cse_id": GOOGLE_CSE_ID,
                }
            func = import_function(tool_def["function"], init_args=init_args)

        #tool = Tool(name=tool_def["name"], func=func, description=tool_def["description"])
        #metadata = {"name": tool_def["name"], "description":tool_def["description"]}
        #tool = FunctionTool.from_defaults(name=tool_def["name"], description=tool_def["description"], fn=func, tool_metadata=metadata)
        tool = FunctionTool.from_defaults(
            name=tool_def["name"],
            description=tool_def["description"],
            fn=func
        )

        if hasattr(tool, "name"):
            print(f"Tool name: {tool.name}")
        else:
            print("Error: Tool name is missing")
        

        tools.append(tool)
        logger.debug(f"Created tool: {tool.metadata}")

    if GOOGLE_API_KEY == "default_value":
        logger.error("Google API KEY was not provided. Integrations that use Google services will not work.")
    if GOOGLE_CSE_ID == "default_value":
        logger.error("Google CSE ID was not provided. Integrations that use Google services will not work.")

    return tools


def get_tool_definitions(context: Optional[dict] = None) -> List[FunctionTool]:
    """
    Get or load tool definitions from a JSON file.

    Returns:
        List[Tool]: A list of Tool objects.

    Note:
        This function caches the tool definitions after the first load.

    Example:
        >>> tools = get_tool_definitions()
        >>> isinstance(tools, list)
        True
        >>> all(isinstance(tool, Tool) for tool in tools)
        True
    """
    global _LLAMA_INDEX_TOOL_DEFINITIONS

    if (_LLAMA_INDEX_TOOL_DEFINITIONS is None) or (context is not None):
        logger.debug("Loading tool definitions from JSON file")
        script_dir = os.path.dirname(__file__)
        json_file_path = os.path.join(script_dir, "global_tools.json")

        with open(json_file_path, "r") as f:
            json_data = json.load(f)
            _LLAMA_INDEX_TOOL_DEFINITIONS = create_tools_from_definitions(json_data, context)

        logger.info(f"Loaded {len(_LLAMA_INDEX_TOOL_DEFINITIONS)} tools:")
        for tool in _LLAMA_INDEX_TOOL_DEFINITIONS:
            logger.info(f"  - {tool.metadata}")

    print(_LLAMA_INDEX_TOOL_DEFINITIONS)

    return _LLAMA_INDEX_TOOL_DEFINITIONS


def get_tools(tool_names: Optional[List[str]] = None, context: Optional[dict] = None) -> List[FunctionTool]:
    """
    Returns a list of tools. If tool_names is provided, returns only the tools with the specified names.
    Otherwise, returns all tools.

    Args:
        tool_names (Optional[List[str]]): A list of tool names to retrieve.

    Returns:
        List[Tool]: A list of Tool objects.

    Example:
        >>> all_tools = get_tools()
        >>> len(all_tools) > 0
        True
        >>> specific_tools = get_tools(['tool1', 'tool2'])
        >>> all(tool.name in ['tool1', 'tool2'] for tool in specific_tools)
        True
    """
    tools = get_tool_definitions(context)

    if tool_names is None:
        logger.debug("Returning all tools")
        return tools
    else:
        logger.debug(f"Returning specific tools: {tool_names}")
        return [tool for tool in tools if tool.metadata.name in tool_names]


# Load tools when the module is imported
get_tool_definitions()

if __name__ == "__main__":
    import doctest

    doctest.testmod()
