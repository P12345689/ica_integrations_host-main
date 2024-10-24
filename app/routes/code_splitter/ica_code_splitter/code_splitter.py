# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Code splitting functions for the ica_code_splitter library.

This module contains the main code_splitter() function for splitting source code into chunks based on token limits and logical structures.
It uses the Tree-sitter library to parse the source code and identify logical structures such as functions, classes, and nested code blocks.
The code is then split into chunks, aiming to keep related code together within the token limit constraints.

The code_splitter() function takes the source code, file path, output directory, programming language, maximum tokens per chunk,
token estimation method, and a flag for code preprocessing as input. It returns a list of code chunks.

Usage:
    - Import the code_splitter() function from this module in other modules or scripts.
    - Use the code_splitter() function to split the source code into chunks based on the specified parameters.

Example:
    >>> from ica_code_splitter.code_splitter import code_splitter

    >>> code = '''
    def hello_world():
        print("Hello, World!")
    '''
    >>> filepath = 'example.py'
    >>> output_dir = 'output'
    >>> language = 'python'
    >>> max_tokens = 50
    >>> estimation_method = 'max'
    >>> preprocess = True

    >>> chunks = code_splitter(code, filepath, output_dir, language, max_tokens, estimation_method, preprocess)
    >>> print(chunks)
    ['def hello_world():\n    print("Hello, World!")']
"""

import logging
import os
from typing import List, Optional

from tree_sitter_languages import get_parser

from .preprocessing import preprocess_code
from .token_estimation import estimate_tokens
from .utils import extract_signature, get_language_comment, load_language_mappings

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Code Splitter
# --------------------------------------------------------------------
def code_splitter(
    code: str,
    filepath: str,
    output_dir: str,
    language_str: Optional[str],
    max_tokens: int,
    estimation_method: str,
    preprocess: bool,
) -> (List[str], List[str]):
    """
    Split the provided source code into chunks based on a maximum token limit and logical structures.

    This function uses the Tree-sitter library to parse the source code and identify logical structures
    such as functions, classes, and nested code blocks. It then splits the code into chunks, aiming to
    keep related code together within the token limit constraints.

    Args:
        code (str): The source code to be split.
        filepath (str): The path to the source code file.
        output_dir (str): The output directory for the generated chunks and headers file.
        language_str (Optional[str]): The programming language of the source code. If not provided, the language is detected based on the file extension.
        max_tokens (int): The maximum number of tokens allowed per chunk.
        estimation_method (str): The method to estimate the number of tokens. Options are 'average', 'words', 'chars', 'max', 'min'.
        preprocess (bool): Whether to preprocess the code to remove comments and extra newlines/spaces.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing a list of code chunks, where each chunk is a string containing a portion of the source code, and a list of headers extracted from the code.

    Raises:
        ValueError: If the programming language is not specified and cannot be detected from the file extension.
    """
    LANGUAGE_MAPPING = load_language_mappings()
    log.info(f"LANGUAGE_MAPPING: {LANGUAGE_MAPPING}")

    if not language_str:
        file_extension = os.path.splitext(filepath)[1]
        language_str = LANGUAGE_MAPPING.get(file_extension)
        if not language_str:
            raise ValueError(f"Language not specified and cannot be detected from file extension: {file_extension}")
        log.debug(f"Detected language: {language_str} for file extension: {file_extension}")

    if preprocess:
        log.info("Preprocessing code...")
        code = preprocess_code(code, language=language_str)

    log.info(f"Getting parser for {language_str}...")
    try:
        parser = get_parser(language_str)
        log.info(f"Parser obtained for {language_str}")
    except Exception as e:
        log.error(f"Error getting parser for {language_str}: {str(e)}")
        raise

    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node
    lines = code.split("\n")

    log.info("Estimating tokens...")
    total_token_count = estimate_tokens(code, method=estimation_method)
    log.info(f"Total tokens in the file: {filepath}: {total_token_count}")

    split_lines = [0]  # Start with the first line
    current_token_count = estimate_tokens("\n".join(lines[: root_node.end_point[0] + 1]), method=estimation_method)
    current_chunk_nodes = []  # Keep track of the nodes in the current chunk
    headers = []  # Store function, class, and method headers

    def visit(node, level=0):
        """
        Recursively visit nodes of the parsed Abstract Syntax Tree (AST) and split the code into chunks.

        This function traverses the AST depth-first and keeps track of the token count for each chunk.
        It creates new chunks when the token count exceeds the specified limit, aiming to keep related
        code together within the token limit constraints.

        Args:
            node (tree_sitter.Node): The current node being visited in the AST.
            level (int, optional): The depth level of the current node in the AST. Defaults to 0.

        The function uses the following variables from the outer scope:
            - `current_token_count` (int): The running count of tokens in the current chunk.
            - `current_chunk_nodes` (List[tree_sitter.Node]): The list of nodes in the current chunk.
            - `split_lines` (List[int]): The list of line numbers where chunks should be split.
            - `lines` (List[str]): The list of individual lines of code from the source code.
            - `max_tokens` (int): The maximum number of tokens allowed per chunk.
            - `estimation_method` (str): The method used to estimate the number of tokens.
            - `headers` (List[str]): The list of function, class, and method headers.

        The function updates `current_token_count`, `current_chunk_nodes`, `split_lines`, and `headers` as it
        traverses the AST. It splits the code into new chunks when the token count exceeds `max_tokens`,
        considering the following cases:
            - If the first node itself exceeds the token limit, it is split into smaller chunks.
            - If the current node is at the top level (level 0) or is a significant structural boundary
            (function, class, or method definition), a new chunk is started.
            - For deeply nested structures, the token count is allowed to exceed the limit until a
            significant boundary is reached.

        The function recursively calls itself on the children of the current node to traverse the entire AST.
        """
        nonlocal current_token_count, current_chunk_nodes, headers
        start_line = node.start_point[0]
        end_line = node.end_point[0]

        if node.type in [
            "function_definition",
            "class_definition",
            "method_declaration",
        ]:
            while start_line > 0 and lines[start_line - 1].strip().startswith("//"):
                start_line -= 1
            header = "\n".join(lines[start_line : end_line + 1])
            signature = extract_signature(header)
            headers.append(signature)

        node_text = "\n".join(lines[start_line : end_line + 1])
        node_token_count = estimate_tokens(node_text, method=estimation_method)

        log.debug(f"Visiting {node.type} from line {start_line} to {end_line}, estimated tokens: {node_token_count}, current chunk tokens: {current_token_count}")

        if level == 0 and node_token_count > max_tokens:
            # If the first node itself exceeds the token limit, split it into smaller chunks
            split_lines.extend(range(start_line, end_line + 1, max_tokens))
            current_token_count = 0
            current_chunk_nodes = []
        elif current_token_count + node_token_count > max_tokens:
            log.debug(f"Exceeded token limit at node {node.type}, line {start_line}. Starting new chunk.")
            if level == 0 or node.type in [
                "function_definition",
                "class_definition",
                "method_declaration",
            ]:
                # This ensures that we only start new chunks at significant structural boundaries
                split_lines.append(start_line)
                current_token_count = node_token_count
                current_chunk_nodes = [node]
            else:
                # Allow the current token count to exceed in deeply nested structures until a significant boundary is reached
                current_token_count += node_token_count
                current_chunk_nodes.append(node)
        else:
            current_token_count += node_token_count
            current_chunk_nodes.append(node)

        for child in node.children:
            if child.type not in ["comment", "line_comment", "block_comment"]:
                visit(child, level + 1)

    visit(root_node)
    split_lines.append(len(lines))  # Always add the last line as the ending point for the last chunk

    # Avoid having an empty file
    # Remove the first split line if it's 0 and the second split line exists
    if len(split_lines) > 1 and split_lines[0] == 0:
        split_lines.pop(0)

    # Merge smaller chunks into larger ones while respecting the token limit
    merged_split_lines = [split_lines[0]]
    current_chunk_token_count = 0
    for i in range(1, len(split_lines)):
        start_line = split_lines[i - 1]
        end_line = split_lines[i]
        chunk_text = "\n".join(lines[start_line:end_line])
        chunk_token_count = estimate_tokens(chunk_text, method=estimation_method)
        if current_chunk_token_count + chunk_token_count <= max_tokens:
            current_chunk_token_count += chunk_token_count
        else:
            merged_split_lines.append(split_lines[i - 1])
            current_chunk_token_count = chunk_token_count
    merged_split_lines.append(split_lines[-1])

    chunks = []
    chunk_number = 1
    for i in range(len(merged_split_lines) - 1):
        start_line = merged_split_lines[i]
        end_line = merged_split_lines[i + 1]
        chunk = "\n".join(lines[start_line:end_line])
        if chunk.strip():  # Skip empty chunks to avoid having empty resulting files
            total_chunks = len(merged_split_lines) - 1
            input_file = os.path.basename(filepath)
            comment_syntax = get_language_comment(language_str)
            chunk_info = f"{comment_syntax} {input_file} chunk {chunk_number}/{total_chunks}"
            chunk = f"{chunk_info}\n{chunk}"
            chunks.append(chunk)
            chunk_number += 1

    # Handle the case when the first chunk is empty
    if len(chunks) > 0 and not chunks[0].strip():
        chunks = chunks[1:]

    # Write the headers file
    headers_filename = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(filepath))[0]}_headers.txt")
    with open(headers_filename, "w") as headers_file:
        headers_file.write("\n".join(headers))

    return chunks, headers
