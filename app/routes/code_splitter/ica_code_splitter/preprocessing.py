# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Preprocessing functions for the ica_code_splitter library.

This module contains functions for preprocessing code, such as removing comments and extra newlines/spaces.
The preprocessing is performed using regular expressions to clean up the code before further processing.

The main function in this module is:

- preprocess_code(code): Preprocesses the code by removing comments and extra newlines/spaces.

Usage:
    - Import the preprocess_code() function from this module in other modules of the ica_code_splitter library.
    - Use the preprocess_code() function to preprocess the code before splitting it into chunks.

Example:
    >>> from ica_code_splitter.preprocessing import preprocess_code

    >>> code = '''
    ... # This is a comment
    ... def hello_world():
    ...    print("Hello, World!")
    ... '''
    >>> preprocessed_code = preprocess_code(code, language="python")
    >>> print(preprocessed_code)
"""

import logging
import re

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Pre-processing
# --------------------------------------------------------------------
def preprocess_code(code: str, language: str) -> str:
    """
    Preprocess the code by removing comments and extra newlines/spaces using regular expressions.

    Args:
        code (str): The source code to preprocess.
        language (str): The programming language of the source code.

    Returns:
        str: The preprocessed code with comments and extra newlines/spaces removed.
    """
    if language in ["python"]:
        # Remove single-line comments
        code = re.sub(r"#.*", "", code)
    elif language in [
        "java",
        "javascript",
        "c",
        "cpp",
        "csharp",
        "php",
        "swift",
        "go",
        "rust",
        "kotlin",
        "scala",
    ]:
        # Remove single-line comments
        code = re.sub(r"(?<!:)//.*", "", code)
        # Remove inline comments
        code = re.sub(r"/\*.*?\*/", "", code)
        # Remove multi-line comments
        code = re.sub(r"/\*[\s\S]*?\*/", "", code)
    elif language in ["ruby", "perl"]:
        # Remove single-line comments
        code = re.sub(r"#.*", "", code)
        # Remove multi-line comments
        code = re.sub(r"=begin[\s\S]*?=end", "", code)
    elif language in ["lua"]:
        # Remove single-line comments
        code = re.sub(r"--.*", "", code)
        # Remove multi-line comments
        code = re.sub(r"--\[\[[\s\S]*?\]\]", "", code)
    elif language in ["sql"]:
        # Remove single-line comments
        code = re.sub(r"--.*", "", code)
        # Remove inline comments
        code = re.sub(r"/\*.*?\*/", "", code)
        # Remove multi-line comments
        code = re.sub(r"/\*[\s\S]*?\*/", "", code)
    elif language in ["html", "xml"]:
        # Remove comments
        code = re.sub(r"<!--[\s\S]*?-->", "", code)
    elif language in ["css"]:
        # Remove comments
        code = re.sub(r"/\*[\s\S]*?\*/", "", code)

    # Remove extra newlines and spaces at the end of lines
    code = re.sub(r"(?<=\n)\s+$", "", code, flags=re.MULTILINE)
    # Remove consecutive empty lines
    code = re.sub(r"\n{2,}", "\n", code)

    return code.strip()
