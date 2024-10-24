# -*- coding: utf-8 -*-
"""
MVS/z/OS Logo Generator tool.

This module provides tools that use the logo generation functionality from the main router.
"""

from langchain.agents import tool

# Import the necessary functions from the main router
from ..mvs_zos_logo_router import LogoInputModel, generate_logo_assembly


@tool
def generate_mvs_zos_logo(logo_text: str, start_line: int = 7, start_column: int = 15) -> str:
    """
    Tool for generating MVS/z/OS logo assembly code.

    Args:
        logo_text (str): The text-based logo to convert.
        start_line (int, optional): The starting line number for the logo. Defaults to 7.
        start_column (int, optional): The starting column number for the logo. Defaults to 15.

    Returns:
        str: The generated assembly language code.

    Example:
        >>> result = generate_mvs_zos_logo("MVS\\nLOGO")
        >>> assert isinstance(result, str)
        >>> assert "$SBA   (7,15)" in result
        >>> assert "DC     C'MVS'" in result
    """
    input_data = LogoInputModel(logo_text=logo_text, start_line=start_line, start_column=start_column)
    return generate_logo_assembly(input_data.logo_text, input_data.start_line, input_data.start_column)


@tool
def format_mvs_zos_logo(text: str, max_width: int = 40) -> str:
    """
    Tool for formatting text into a simple ASCII art logo suitable for MVS/z/OS.

    Args:
        text (str): The text to format into a logo.
        max_width (int, optional): The maximum width of the logo. Defaults to 40.

    Returns:
        str: The formatted ASCII art logo.

    Example:
        >>> result = format_mvs_zos_logo("MVS LOGO")
        >>> assert isinstance(result, str)
        >>> assert len(result.split('\\n')) <= 6
        >>> assert all(len(line) <= 40 for line in result.split('\\n'))
    """
    lines = []
    words = text.split()
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 > max_width:
            lines.append(current_line)
            current_line = word
        else:
            current_line += " " + word if current_line else word

    if current_line:
        lines.append(current_line)

    # Center each line
    formatted_lines = [line.center(max_width) for line in lines]

    # Add decorative borders
    border = "+" + "-" * (max_width - 2) + "+"
    formatted_logo = [border] + ["|" + line + "|" for line in formatted_lines] + [border]

    return "\n".join(formatted_logo[:6])  # Limit to 6 lines
