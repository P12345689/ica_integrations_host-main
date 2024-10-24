#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Author: Mihai Criveti
Description: Token estimation CLI tool for estimating tokens in files and calculating costs.

This CLI tool allows you to estimate the number of tokens in one or more files using different estimation methods,
including the OpenAI tiktoken library. It supports globbing, recursive file search, verbose output, and file extension filtering.
It also calculates the estimated cost based on the token count and displays a table with costs for all supported pricing models.

Usage:
    python token_estimation_cli.py <file_path_1> <file_path_2> ... [--method METHOD] [--recursive] [--verbose] [--extensions EXTENSIONS]

    - <file_path_1>, <file_path_2>, ...: Paths to the files or directories for token estimation. Supports globbing.
    - --method METHOD: (Optional) The method to use for token estimation. Options are 'average', 'words', 'chars', 'max', 'min', 'tiktoken'. Default is 'max'.
    - --recursive, -r: (Optional) Perform recursive file search in directories.
    - --verbose, -v: (Optional) Enable verbose output.
    - --extensions EXTENSIONS: (Optional) Comma-separated list of file extensions to include. Default is 'py,java,c,sql'.

Example:
    python token_estimation_cli.py "*.py" "src/" --method tiktoken --recursive --verbose --extensions py,js,txt

Dependencies:
    - rich: For enhanced output formatting with tables and colors.
    - tiktoken: For the 'tiktoken' estimation method (optional).

Installation:
    pip install rich tiktoken
"""

import argparse
import glob
import logging
import os
from typing import Dict, List

from rich.console import Console
from rich.table import Table

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

try:
    import tiktoken
except ImportError:
    logger.warning(
        "OpenAI tiktoken library not found. Install it using 'pip install tiktoken' for the 'tiktoken' method."
    )
    tiktoken = None

# Pricing models (per 1 million tokens)
PRICING_MODELS = {
    "llama-3-70b-instruct (watsonx.ai)": 1.80,
    "GPT-4 (blended, assumes input/output)": 37.50,
    "Claude 2": 12.00,
}

# File extensions to skip
SKIP_EXTENSIONS = [".git", ".bak"]

# Default file extensions to include
DEFAULT_EXTENSIONS = ["py", "java", "c", "sql"]


# --------------------------------------------------------------------
# Token Estimation
# --------------------------------------------------------------------
def estimate_tokens(text: str, method: str = "max") -> int:
    """
    Estimate the number of tokens in the given text based on the specified method.

    The function provides six estimation methods:
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
    6. 'tiktoken': Uses the OpenAI tiktoken library to count the tokens.
                   - Requires the tiktoken library to be installed.

    Args:
        text (str): The text to estimate tokens for.
        method (str, optional): The method to use for token estimation. Options are 'average', 'words', 'chars', 'max', 'min', 'tiktoken'. Default is 'max'.

    Returns:
        int: The estimated number of tokens.

    Raises:
        ValueError: If an invalid estimation method is provided or the tiktoken library is not installed for the 'tiktoken' method.

    Examples:
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
        "tiktoken": lambda text, _: len(tiktoken.get_encoding("cl100k_base").encode(text)) if tiktoken else None,
    }

    if method not in methods:
        logger.error(f"Invalid token estimation method: {method}")
        raise ValueError("Invalid method. Use 'average', 'words', 'chars', 'max', 'min', or 'tiktoken'.")

    if method == "tiktoken" and tiktoken is None:
        logger.error(
            "OpenAI tiktoken library not found. Install it using 'pip install tiktoken' for the 'tiktoken' method."
        )
        raise ValueError(
            "OpenAI tiktoken library not found. Install it using 'pip install tiktoken' for the 'tiktoken' method."
        )

    return (
        methods[method](text, None)
        if method == "tiktoken"
        else methods[method](tokens_count_word_est, tokens_count_char_est)
    )


def count_tokens(filepaths: List[str], estimation_method: str, verbose: bool = False) -> Dict[str, int]:
    """
    Count the estimated tokens in the specified files.

    Args:
        filepaths (List[str]): List of file paths to count tokens for.
        estimation_method (str): The method to estimate the number of tokens. Options are 'average', 'words', 'chars', 'max', 'min', 'tiktoken'.
        verbose (bool, optional): Enable verbose output. Default is False.

    Returns:
        Dict[str, int]: A dictionary mapping file paths to their estimated token counts.

    Examples:
        >>> filepaths = ["file1.py", "file2.py"]
        >>> count_tokens(filepaths, estimation_method="max")
        {'file1.py': 100, 'file2.py': 200}
    """
    token_counts = {}
    for filepath in filepaths:
        try:
            with open(filepath, "r") as file:
                code = file.read()
                token_count = estimate_tokens(code, method=estimation_method)
                token_counts[filepath] = token_count
                if verbose:
                    logger.info(f"File: {filepath}, Estimated Tokens: {token_count}")
        except FileNotFoundError:
            logger.error(f"File not found: {filepath}")
        except Exception as e:
            logger.error(f"Error counting tokens for file {filepath}: {str(e)}")
    return token_counts


def get_files(
    paths: List[str],
    recursive: bool = False,
    extensions: List[str] = DEFAULT_EXTENSIONS,
) -> List[str]:
    """
    Get the list of files based on the provided paths, supporting globbing and recursive search.

    Args:
        paths (List[str]): List of paths to files or directories.
        recursive (bool, optional): Perform recursive file search in directories. Default is False.
        extensions (List[str], optional): List of file extensions to include. Default is DEFAULT_EXTENSIONS.

    Returns:
        List[str]: List of file paths.

    Examples:
        >>> paths = ["src/", "*.py"]
        >>> get_files(paths, recursive=True)
        ['src/file1.py', 'src/file2.py', 'file3.py']
    """
    files = []
    for path in paths:
        if os.path.isfile(path):
            _, ext = os.path.splitext(path)
            if ext[1:] in extensions:
                files.append(path)
        elif os.path.isdir(path):
            if recursive:
                for root, _, filenames in os.walk(path):
                    for filename in filenames:
                        _, ext = os.path.splitext(filename)
                        if ext[1:] in extensions and ext not in SKIP_EXTENSIONS:
                            files.append(os.path.join(root, filename))
            else:
                for ext in extensions:
                    files.extend(glob.glob(os.path.join(path, f"*.{ext}")))
        else:
            for ext in extensions:
                files.extend(glob.glob(f"{path}.{ext}"))
    return files


def calculate_costs(total_tokens: int) -> Dict[str, float]:
    """
    Calculate the estimated costs for all supported pricing models based on the total tokens.

    Args:
        total_tokens (int): The total number of tokens.

    Returns:
        Dict[str, float]: A dictionary mapping pricing models to their estimated costs.

    Examples:
        >>> calculate_costs(1000000)
        {'llama-3-70b-instruct (watsonx.ai)': 1.8, 'GPT-4 (blended, assumes input/output)': 37.5, 'Claude 2': 12.0}
    """
    costs = {}
    for model, price_per_million_tokens in PRICING_MODELS.items():
        cost = (total_tokens / 1_000_000) * price_per_million_tokens
        costs[model] = cost
    return costs


def main():
    parser = argparse.ArgumentParser(description="Token Estimation CLI Tool")
    parser.add_argument(
        "paths",
        nargs="+",
        help="Paths to the files or directories for token estimation (supports globbing)",
    )
    parser.add_argument("--method", default="max", help="Token estimation method (default: max)")
    parser.add_argument(
        "--recursive",
        "-r",
        action="store_true",
        help="Perform recursive file search in directories",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--extensions",
        default=",".join(DEFAULT_EXTENSIONS),
        help=f"Comma-separated list of file extensions to include (default: {','.join(DEFAULT_EXTENSIONS)})",
    )
    args = parser.parse_args()

    extensions = args.extensions.split(",")
    files = get_files(args.paths, args.recursive, extensions)
    token_counts = count_tokens(files, args.method, args.verbose)
    total_tokens = sum(count for count in token_counts.values() if count is not None)
    total_tokens_with_multiplier = total_tokens * 3
    costs = calculate_costs(total_tokens_with_multiplier)

    console = Console()

    console.print("[bold blue]Token Estimation Results:[/bold blue]")
    console.print("=" * 50)
    console.print("[bold]Pricing Models (per 1 million tokens):[/bold]")
    pricing_table = Table(show_header=True, header_style="bold magenta")
    pricing_table.add_column("Model")
    pricing_table.add_column("Price")
    for model, price in PRICING_MODELS.items():
        pricing_table.add_row(model, f"${price:.2f}")
    console.print(pricing_table)

    console.print("=" * 50)
    console.print("[bold]File Token Counts:[/bold]")
    file_table = Table(show_header=True, header_style="bold cyan")
    file_table.add_column("File")
    file_table.add_column("Tokens", justify="right")
    for filepath, count in token_counts.items():
        if count is not None:
            file_table.add_row(filepath, str(count))
        elif args.verbose:
            file_table.add_row(filepath, "Error")
    console.print(file_table)

    console.print("=" * 50)
    console.print(f"[bold green]Total Tokens:[/bold green] {total_tokens}")
    console.print(f"[bold green]Total Tokens (with 3x multiplier):[/bold green] {total_tokens_with_multiplier}")

    console.print("=" * 50)
    console.print("[bold]Estimated Costs:[/bold]")
    cost_table = Table(show_header=True, header_style="bold yellow")
    cost_table.add_column("Model")
    cost_table.add_column("Cost", justify="right")
    for model, cost in costs.items():
        cost_table.add_row(model, f"${cost:.2f}")
    console.print(cost_table)
    console.print("=" * 50)


if __name__ == "__main__":
    main()
