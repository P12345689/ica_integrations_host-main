#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti, M S Rahul Saj
Description: Command-line interface for the ica_code_splitter library.

This script provides a command-line interface for splitting source code into chunks based on token limits
or counting tokens in files using the ica_code_splitter library.

This library uses the Tree-sitter library to parse the source code and identify logical structures such as
functions, classes, and nested code blocks. It then splits the code into chunks, aiming to keep related
code together within the token limit constraints.

Usage:
    python cli.py <filepath> [--output_dir <output_directory>] [--language <language>] [--max_tokens <max_tokens>]
                             [--estimation_method <method>] [--preprocess] [--verbose]

    python cli.py --count_tokens <file1> <file2> ... [--estimation_method <method>]

Arguments:
    filepath (str): Path to the source code file to be split.
    --output_dir (str, optional): Output directory for the generated chunks and headers file. Default is the current directory.
    --language (str, optional): Programming language of the source code. If not provided, the language is detected based on the file extension.
    --max_tokens (int, optional): Maximum number of tokens allowed per chunk. Default is 3000.
    --estimation_method (str, optional): Method to estimate the number of tokens. Options are 'average', 'words', 'chars', 'max', 'min'. Default is 'max'.
    --preprocess (flag, optional): Enables code preprocessing to remove comments and extra newlines/spaces using the AST parser.
    --verbose (flag, optional): Enables detailed debug logging.
    --count_tokens (flag): Counts the estimated tokens in the specified files.

Examples:
    python cli.py example.py --output_dir chunks --language python --max_tokens 500 --estimation_method max --preprocess --verbose
    python cli.py --count_tokens file1.py file2.py --estimation_method max


---
Description: Command-line interface for the genai code_splitter library.

This script provides a command-line interface for splitting source code into chunks based on token limits
or counting tokens in files using the genai ica_code_splitter library.

Usage:
    python cli.py <filepath> -s <code_splitter> -u <usecase_id> 


Arguments:
    filepath (str): Path to the source code file to be split.
    --splitter (str): Type of the splitter to use, available options are genai_code_splitter and ica_code_splitter.
    --usecase-id (str): Use case id to choose language parser and other attributes such as max_token_size, etc.
    

Examples:python cli.py example.java -s genai_code_splitter -u Java_to_Business_Rule 
    

"""

import argparse
import glob
import logging
import os
import asyncio

from ica_code_splitter.code_splitter import code_splitter
from ica_code_splitter.token_estimation import count_tokens, estimate_tokens
from genai_code_splitter.splitter.jobs import create_jobs

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Main
# --------------------------------------------------------------------
def main() -> None:
    """
    The main function that parses command-line arguments and splits the source code into chunks.
    """

    parser = argparse.ArgumentParser(description="Split code into chunks based on token limits or count tokens in files.")
    parser.add_argument("filepath", nargs="?", help="Path to the source code file.")
    parser.add_argument(
        "-o",
        "--output_dir",
        default=".",
        help="Output directory for the generated chunks and headers file.",
    )
    parser.add_argument("-l", "--language", help="Programming language of the source code.")
    parser.add_argument(
        "-m",
        "--max_tokens",
        type=int,
        default=3000,
        help="Maximum number of tokens per chunk.",
    )
    parser.add_argument(
        "-e",
        "--estimation_method",
        choices=["average", "words", "chars", "max", "min"],
        default="max",
        help="Method to estimate tokens.",
    )
    parser.add_argument(
        "-p",
        "--preprocess",
        action="store_true",
        help="Enable code preprocessing to remove comments and extra newlines/spaces using regular expressions.",
    )
    parser.add_argument(
        "-c",
        "--count_tokens",
        nargs="*",
        help="Count tokens in the specified file(s). Supports globbing.",
    )
    parser.add_argument(
        "-s",
        "--splitter",
        choices=["genai_code_splitter", "ica_code_splitter"],
        help="Type of request (default: unit_test)",
    )
 
    parser.add_argument(
        "-u",
        "--usecase_id",
        choices=["SpringBoot_to_Quarkus", "Java_X_to_Java_Y_Conversion", "Java_to_Business_Rule"],
        help="Use case ID to choose for GenAI Code Splitter",
    )
   
    
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging.")
    args = parser.parse_args()

    # Verbose Flag
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled.")

        # Create the output directory if it does not exist
    os.makedirs(args.output_dir, exist_ok=True)

        # Count tokens flag
    if args.count_tokens:
        filepaths = []
        for path in args.count_tokens:
            if "*" in path:
                filepaths.extend(glob.glob(path))
            else:
                filepaths.append(path)
        token_counts = count_tokens(filepaths, args.estimation_method)
        for filepath, count in token_counts.items():
            if count is not None:
                print(f"{filepath}: Estimated tokens: {count}")
            else:
                print(f"{filepath}: Failed to count tokens")
        return

    try:
        with open(args.filepath, "r") as file:
            code = file.read()
    except FileNotFoundError:
        logger.error(f"File not found: {args.filepath}")
        print(f"Error: The file {args.filepath} does not exist.")
        return
    
    if splitter:= args.splitter:
        if splitter == "genai_code_splitter":
            chunks, *_ = asyncio.run(create_jobs(
                code,
                args.usecase_id,
                "ica",
                "chunk_only"
            ))
            print(f"Chunks are as follows: \n\n{chunks}")
        return




    if not args.filepath:
        parser.error("the following arguments are required: filepath")



    # code_splitter
    try:
        chunks, headers = code_splitter(
            code,
            args.filepath,
            args.output_dir,
            args.language,
            args.max_tokens,
            args.estimation_method,
            args.preprocess,
        )
    except ValueError as e:
        logger.error(f"Error splitting code: {e}")
        print(f"Error: {e}")
        return

    # write chunks
    file_extension = os.path.splitext(args.filepath)[1]
    for i, chunk in enumerate(chunks, 1):
        chunk_filename = os.path.join(
            args.output_dir,
            f"{os.path.splitext(os.path.basename(args.filepath))[0]}_chunk_{i}{file_extension}",
        )
        with open(chunk_filename, "w") as output_file:
            output_file.write(chunk)
        chunk_token_count = estimate_tokens(chunk, method=args.estimation_method)
        print(f"# CHUNK {i}: Saved to {chunk_filename} - Estimated tokens: {chunk_token_count}")
        logger.info(f"Chunk {i} written to file {chunk_filename}")

    logger.info(f"Total chunks: {len(chunks)}")


if __name__ == "__main__":
    main()
