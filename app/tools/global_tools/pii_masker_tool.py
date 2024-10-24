# -*- coding: utf-8 -*-
"""
PII masking tool for use with LangChain agents.

This module provides a tool that uses the PII masking functionality from the main router.
"""

from typing import Dict, List, Optional

from langchain.agents import tool

# Import the necessary functions and types from the main router
from app.routes.pii_masker.pii_masker_router import MaskType, PIIType, process_pii


@tool
def pii_masker_tool(
    text: str,
    mask_type: str = "mask",
    pii_types: List[str] = ["credit_card"],
    custom_regex: Optional[Dict[str, str]] = None,
    encryption_key: Optional[str] = None,
) -> str:
    """
    Tool for masking PII in the given text.

    Args:
        text (str): The input text containing PII.
        mask_type (str): The type of masking to apply ("delete", "mask", or "fake").
        pii_types (List[str]): Types of PII to mask (e.g., ["credit_card", "name", "email"]).
        custom_regex (Optional[str]): Custom regex pattern for PII detection.

    Returns:
        str: The text with masked PII.
    """
    try:
        mask_type_enum = MaskType(mask_type)
        pii_types_enum = [PIIType(pii_type) for pii_type in pii_types]
        return process_pii(text, mask_type_enum, pii_types_enum, custom_regex, encryption_key)
    except ValueError as e:
        return f"Error: {str(e)}"
