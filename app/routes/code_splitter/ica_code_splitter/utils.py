# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Utility functions for the ica_code_splitter library.

This module contains utility functions used by other modules in the ica_code_splitter library.
These functions include:

- load_language_mappings(): Loads language mappings from a JSON file to map file extensions to programming languages.
- get_language_comment(language): Gets the language-specific comment syntax based on the programming language.
- extract_signature(header): Extracts the function, class, or method signature from the header.

Usage:
    - Import the necessary functions from this module in other modules of the ica_code_splitter library.
    - Use the functions as needed to perform common tasks such as loading language mappings, getting comment syntaxes, and extracting signatures.

Example:
    >>> from ica_code_splitter.utils import load_language_mappings, get_language_comment, extract_signature

    >>> language_mappings = load_language_mappings()
    >>> comment_syntax = get_language_comment('python')
    >>> signature = extract_signature('def hello_world(name: str) -> None:')
"""

import json
import logging
import os
import re
from typing import Dict

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Utility Functions
# --------------------------------------------------------------------
def load_language_mappings() -> Dict[str, str]:
    """
    Load language mappings from a JSON file to map file extensions to programming languages.

    Returns:
        Dict[str, str]: A dictionary mapping file extensions to programming languages.

    Raises:
        FileNotFoundError: If the language configuration file is not found.
        json.JSONDecodeError: If there is an error decoding the JSON file.
    """

    # Get the directory of the current file (utils.py)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the language_config.json file
    config_path = os.path.join(current_dir, "..", "language_config.json")

    try:
        with open(config_path, "r") as file:
            return {v: k for k, v in json.load(file).items()}
    except FileNotFoundError as e:
        logger.error(f"Language configuration file not found: {e}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding the language configuration file: {e}")
        raise


def get_language_comment(language: str) -> str:
    """
    Get the language-specific comment syntax based on the programming language.

    Args:
        language (str): The programming language.

    Returns:
        str: The language-specific comment syntax.
    """
    comment_syntax = {
        "python": "#",
        "javascript": "//",
        "java": "//",
        "c": "//",
        "cpp": "//",
        "csharp": "//",
        "ruby": "#",
        "php": "//",
        "swift": "//",
        "go": "//",
        "rust": "//",
        "kotlin": "//",
        "scala": "//",
        "lua": "--",
        "perl": "#",
        "r": "#",
        "sql": "--",
    }
    return comment_syntax.get(language, "//")  # Use '//' as the default comment syntax if not found


def extract_signature(header: str) -> str:
    """
    Extract the function, class, or method signature from the header.

    Args:
        header (str): The header containing the function, class, or method definition.

    Returns:
        str: The extracted signature without the body or comments.
    """
    signature = re.sub(r"\{.*\}", "", header, flags=re.DOTALL)  # Remove the body
    signature = re.sub(r"\/\/.*", "", signature)  # Remove single-line comments
    signature = re.sub(r"\/\*[\s\S]*?\*\/", "", signature)  # Remove multi-line comments
    return signature.strip()
