# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Package initialization file for the ica_code_splitter library.

This file serves as the entry point for the ica_code_splitter package. It imports the main functions
and classes from the respective modules and defines the __all__ variable, which specifies the public API
of the package.

The __all__ variable lists the names that should be imported when using the `from ica_code_splitter import *`
statement. It includes the following functions:

- code_splitter from the code_splitter module
- preprocess_code from the preprocessing module
- estimate_tokens and count_tokens from the token_estimation module
- load_language_mappings, get_language_comment, and extract_signature from the utils module

Usage:
    - Import the package or specific functions from the package in your Python scripts or modules.
    - Use the imported functions and classes as needed for code splitting and token estimation tasks.

Example:
    >>> from ica_code_splitter import code_splitter, preprocess_code

    >>> code = '''
    ... def hello_world():
    ...    print("Hello, World!")
    ... '''
    >>> preprocessed_code = preprocess_code(code, language="python")
    >>> chunks = code_splitter(preprocessed_code, filepath, output_dir, language, max_tokens, estimation_method, preprocess=False)
"""

import logging

from .code_splitter import code_splitter
from .preprocessing import preprocess_code
from .token_estimation import count_tokens, estimate_tokens
from .utils import extract_signature, get_language_comment, load_language_mappings

__all__ = [
    "code_splitter",
    "preprocess_code",
    "estimate_tokens",
    "count_tokens",
    "load_language_mappings",
    "get_language_comment",
    "extract_signature",
]

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)
logger.debug("Initialized the ica_code_splitter package.")
