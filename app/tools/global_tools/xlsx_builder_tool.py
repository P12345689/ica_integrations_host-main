# -*- coding: utf-8 -*-
"""
XLSX builder tool for creating XLSX files and retrieving information about the XLSX builder integration.

This module provides tools that wrap the functionality from the main xlsx_builder router.
"""

from langchain.agents import tool

# Import the generate_xlsx function from the main router
from app.routes.xlsx_builder.xlsx_builder_router import generate_xlsx


@tool
def create_xlsx_from_csv(csv_data: str, sheet_name: str = "Sheet1") -> str:
    """
    Tool for generating an XLSX file from CSV data.

    Args:
        csv_data (str): The CSV data as a string.
        sheet_name (str, optional): The name of the sheet in the XLSX file. Defaults to "Sheet1".

    Returns:
        str: The URL of the generated XLSX file.

    Example:
        >>> result = create_xlsx_from_csv("Name,Age\nJohn,30\nJane,25", "Employee Data")
        >>> assert "http" in result and ".xlsx" in result
    """
    return generate_xlsx(csv_data, sheet_name)


@tool
def get_xlsx_builder_info() -> str:
    """
    Tool for getting information about the XLSX builder integration.

    Returns:
        str: Information about the XLSX builder integration.

    Example:
        >>> info = get_xlsx_builder_info()
        >>> assert "XLSX" in info
        >>> assert "generate spreadsheets" in info
    """
    return (
        "The XLSX builder integration provides functionality to generate XLSX files "
        "from CSV data or natural language descriptions. It can create spreadsheets "
        "with multiple columns and rows based on the provided input."
    )


@tool
def xlsx_format_helper() -> str:
    """
    Tool for providing information about XLSX file format and capabilities.

    Returns:
        str: Information about XLSX file format and capabilities.

    Example:
        >>> result = xlsx_format_helper()
        >>> assert "XLSX" in result
        >>> assert "Microsoft Excel" in result
    """
    return (
        "XLSX is a file format used by Microsoft Excel for spreadsheets. "
        "It supports multiple sheets, formulas, charts, and various data types. "
        "XLSX files can be opened by Excel and many other spreadsheet applications. "
        "They are useful for organizing, analyzing, and visualizing data in a tabular format."
    )
