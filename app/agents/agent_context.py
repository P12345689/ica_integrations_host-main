# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti, Chris Hay
Description: Utility module for context parsing and formatting

This module provides utilities for parsing stringified JSON context into
context items and formatting it.
"""
import os
import json
import logging
import re
from typing import List, Optional
from pydantic import BaseModel, ValidationError
from llama_index.core.llms import ChatMessage

# Setup logging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

# set clean context
CLEAN_CONTEXT = os.getenv("CLEAN_CONTEXT", "True").lower() == "true"

class ContextItem(BaseModel):
    """Model for a single context item."""

    content: str
    type: str


def unescape_string(s: str) -> str:
    """
    Unescape a string that may contain various levels of escaping,
    while preserving regular characters.

    Args:
        s (str): The escaped string.

    Returns:
        str: The unescaped string.
    """
    pattern = r'\\(\\\\|["\\/bfnrt]|u[0-9a-fA-F]{4})'

    def unescape_match(match: re.Match) -> str:
        escaped = match.group(1)
        if escaped == "\\":
            return "\\"
        if escaped in '"\\/bfnrt':
            return json.loads(f'"{match.group(0)}"')
        if escaped.startswith("u"):
            return chr(int(escaped[1:], 16))
        return match.group(0)

    return re.sub(pattern, unescape_match, s)


def parse_context(context_str: Optional[str]) -> List[ContextItem]:
    """
    Parses the stringified JSON context into a list of ContextItem objects.

    Args:
        context_str (Optional[str]): The JSON string of context items.

    Returns:
        List[ContextItem]: A list of ContextItem objects.

    Raises:
        ValueError: If the context JSON is invalid or if context items are in an invalid format.
    """
    if not context_str:
        log.debug("Empty context string provided.")
        return []

    try:
        context_data = json.loads(context_str)
        log.debug("Context JSON parsed successfully.")

        if CLEAN_CONTEXT:
            cleaned_context_data = []
            for item in context_data:
                cleaned_item = {
                    "content": unescape_string(item["content"]),
                    "type": item["type"],
                }
                cleaned_context_data.append(cleaned_item)
                log.debug(f"Context item cleaned: {cleaned_item}")
        else:
            cleaned_context_data = context_data
            log.debug("Context cleaning not enabled.")

        context_items = [ContextItem(**item) for item in cleaned_context_data]
        log.debug(f"Context items validated successfully: {context_items}")
        return context_items

    except json.JSONDecodeError as e:
        log.error(f"Error parsing context JSON: {e}")
        raise ValueError("Invalid context JSON") from e
    except ValidationError as e:
        log.error(f"Error validating context items: {e}")
        raise ValueError("Invalid context item format") from e

def format_context(context_items: List[ContextItem]) -> str:
    """
    Formats the context items into a string for the prompt.

    Args:
        context_items (List[ContextItem]): A list of ContextItem objects.

    Returns:
        str: A formatted string representing the context items.
    """
    formatted_context = "\n".join([f"{item.type}: {item.content}" for item in context_items])
    log.debug(f"Formatted context: {formatted_context}")
    return formatted_context

def format_llamaindex_chat_message(context_items: List[ContextItem]) -> List[ChatMessage]:
    """
    Convert a list of ContextItem objects into a list of ChatMessage objects.

    Args:
        context_items (List[ContextItem]): A list of ContextItem objects.

    Returns:
        List[ChatMessage]: A list of ChatMessage objects.
    """
    return [ChatMessage(role=item.type, content=item.content) for item in context_items]
