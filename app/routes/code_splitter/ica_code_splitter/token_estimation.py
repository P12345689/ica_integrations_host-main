# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Token estimation functions for the ica_code_splitter library.

This module contains functions for estimating the number of tokens in a given text and counting tokens in files.
The token estimation is based on different methods such as average, words, characters, maximum, or minimum.

The main functions in this module are:

- estimate_tokens(text, method): Estimates the number of tokens in the given text based on the specified method.
- count_tokens(filepaths, estimation_method): Counts the estimated tokens in the specified files.

Usage:
    - Import the necessary functions from this module in other modules of the ica_code_splitter library.
    - Use the estimate_tokens() function to estimate the number of tokens in a given text.
    - Use the count_tokens() function to count the estimated tokens in specified files.

Example:
    >>> from ica_code_splitter.token_estimation import estimate_tokens, count_tokens

    >>> text = "This is a sample text."
    >>> token_count = estimate_tokens(text, method="max")
    >>> print(f"Estimated tokens: {token_count}")

    >>> filepaths = ["file1.py", "file2.py"]
    >>> token_counts = count_tokens(filepaths, estimation_method="max")
    >>> print(f"Token counts: {token_counts}")
"""

import logging
from typing import Dict, List

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Token Estimation
# --------------------------------------------------------------------
def estimate_tokens(text: str, method: str = "max") -> int:
    """
    Estimate the number of tokens in the given text based on the specified method.

    The function provides five estimation methods:
    1. 'average': Calculates the average of the word-based and character-based token estimates.
                  - Word-based estimate: Divides the word count by 0.75 and rounds to the nearest integer.
                  - Character-based estimate: Divides the character count by 4.0 and rounds to the nearest integer.
                  - The final estimate is the average of the word-based and character-based estimates.
    2. 'words': Uses the word-based token estimate.
                - Word-based estimate: Divides the word count by 0.75 and rounds to the nearest integer.
    3. 'chars': Uses the character-based token estimate.
                - Character-based estimate: Divides the character count by 4.0 and rounds to the nearest integer.
    4. 'max': Takes the maximum of the word-based and character-based token estimates.
    5. 'min': Takes the minimum of the word-based and character-based token estimates.

    Args:
        text (str): The text to estimate tokens for.
        method (str, optional): The method to use for token estimation. Options are 'average', 'words', 'chars', 'max', 'min'. Default is 'max'.

    Returns:
        int: The estimated number of tokens.

    Raises:
        ValueError: If an invalid estimation method is provided.

    Example:
        >>> text = "This is a sample text."
        >>> estimate_tokens(text, method="average")
        5
        >>> estimate_tokens(text, method="words")
        6
        >>> estimate_tokens(text, method="chars")
        5
        >>> estimate_tokens(text, method="max")
        6
        >>> estimate_tokens(text, method="min")
        5
    """
    words = text.split()
    word_count = len(words)
    char_count = len(text)
    tokens_count_word_est = int(word_count / 0.75)
    tokens_count_char_est = int(char_count / 4.0)

    methods = {
        "average": lambda wc, cc: (wc + cc) // 2,
        "words": lambda wc, _: wc,
        "chars": lambda _, cc: cc,
        "max": lambda wc, cc: max(wc, cc),
        "min": lambda wc, cc: min(wc, cc),
    }

    if method not in methods:
        logger.error(f"Invalid token estimation method: {method}")
        raise ValueError("Invalid method. Use 'average', 'words', 'chars', 'max', or 'min'.")

    return methods[method](tokens_count_word_est, tokens_count_char_est)


def count_tokens(filepaths: List[str], estimation_method: str) -> Dict[str, int]:
    """
    Count the estimated tokens in the specified files.

    Args:
        filepaths (List[str]): List of file paths to count tokens for.
        estimation_method (str): The method to estimate the number of tokens. Options are 'average', 'words', 'chars', 'max', 'min'.

    Returns:
        Dict[str, int]: A dictionary mapping file paths to their estimated token counts.
    """
    token_counts = {}
    for filepath in filepaths:
        try:
            with open(filepath, "r") as file:
                code = file.read()
                token_count = estimate_tokens(code, method=estimation_method)
                token_counts[filepath] = token_count
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
            token_counts[filepath] = None
        except Exception as e:
            logger.error(f"Error counting tokens for file {filepath}: {str(e)}")
            token_counts[filepath] = None
    return token_counts
