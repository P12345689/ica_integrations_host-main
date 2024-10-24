# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Chart generation tool for creating various types of charts and retrieving information about the Chart integration.

This module provides tools that wrap the functionality from the main chart router.
"""

import json

from langchain.agents import tool

# Import the generate_chart function from the main router
from app.routes.chart.chart_router import generate_chart


@tool
def create_chart(input_json: str) -> str:
    """
    Tool for generating a chart from the provided JSON data.

    Args:
        input_json (str): JSON string containing the chart type, data, and optionally a title.

    Returns:
        str: The URL of the generated PNG file.

    Example:
        >>> result = create_chart('{"chart_type": "bar", "data": {"x": ["A", "B", "C"], "y": [1, 2, 3]}, "title": "Sample Chart"}')
        >>> assert "http" in result and ".png" in result
    """
    try:
        params = json.loads(input_json)
    except json.JSONDecodeError:
        return "Error: Invalid JSON input. Please provide a valid JSON string."

    chart_type = params.get("chart_type")
    data = params.get("data")
    title = params.get("title", "")
    return generate_chart(chart_type, data, title)


@tool
def get_chart_info() -> str:
    """
    Tool for getting information about the Chart integration.

    Returns:
        str: Information about the Chart integration.

    Example:
        >>> info = get_chart_info()
        >>> assert "Chart" in info
        >>> assert "generate charts" in info
    """
    return (
        "The Chart integration provides functionality to generate various types of charts "
        "using matplotlib. It can create PNG images of bar charts, pie charts, line charts, "
        "and more based on provided data or natural language descriptions."
    )


@tool
def chart_type_helper(input_json: str) -> str:
    """
    Tool for providing information about different chart types and their data requirements from JSON input.

    Args:
        input_json (str): JSON string containing the chart type.

    Returns:
        str: Information about the specified chart type and its data requirements.

    Example:
        >>> result = chart_type_helper('{"chart_type": "bar"}')
        >>> assert "bar chart" in result.lower()
        >>> assert "x" in result and "y" in result
    """
    try:
        params = json.loads(input_json)
    except json.JSONDecodeError:
        return "Error: Invalid JSON input. Please provide a valid JSON string."

    chart_type = params.get("chart_type")
    info = {
        "bar": "Bar charts require 'x' (categories) and 'y' (values) data. Example: {'x': ['A', 'B', 'C'], 'y': [1, 2, 3]}",
        "pie": "Pie charts require 'labels' and 'values' data. Example: {'labels': ['A', 'B', 'C'], 'values': [30, 40, 30]}",
        "line": "Line charts require 'x' (typically time or ordered categories) and 'y' (values) data. Example: {'x': [1, 2, 3, 4], 'y': [10, 15, 13, 17]}",
        "scatter": "Scatter plots require 'x' and 'y' data for each point. Example: {'x': [1, 2, 3, 4], 'y': [10, 15, 13, 17]}",
        "histogram": "Histograms require a single list of values. Example: {'values': [1, 2, 2, 3, 3, 3, 4, 4, 5]}",
    }

    return info.get(
        chart_type.lower(),
        "Chart type not recognized. Available types: bar, pie, line, scatter, histogram.",
    )
