# -*- coding: utf-8 -*-
"""
Plotly chart generation tool for creating various types of charts and retrieving information about the Plotly integration.

This module provides tools that wrap the functionality from the main plotly router.
"""

from typing import Any, Dict, List

from langchain.agents import tool

# Import the generate_chart function from the main router
from app.routes.plotly.plotly_router import generate_chart


@tool
def create_plotly_chart(chart_type: str, data: Dict[str, List[Any]], title: str = "") -> str:
    """
    Tool for generating a Plotly chart from the provided data.

    Args:
        chart_type (str): The type of chart to generate (e.g., 'bar', 'pie', 'line').
        data (Dict[str, List[Any]]): The data for the chart.
        title (str, optional): The title of the chart.

    Returns:
        str: The URL of the generated HTML file.

    Example:
        >>> result = create_plotly_chart("bar", {"x": ["A", "B", "C"], "y": [1, 2, 3]}, "Sample Chart")
        >>> assert "http" in result and ".html" in result
    """
    return generate_chart(chart_type, data, title)


@tool
def get_plotly_info() -> str:
    """
    Tool for getting information about the Plotly integration.

    Returns:
        str: Information about the Plotly integration.

    Example:
        >>> info = get_plotly_info()
        >>> assert "Plotly" in info
        >>> assert "generate interactive charts" in info
    """
    return (
        "The Plotly integration provides functionality to generate various types of interactive charts "
        "using Plotly. It can create HTML files containing interactive bar charts, pie charts, line charts, "
        "and more based on provided data or natural language descriptions."
    )


@tool
def plotly_chart_type_helper(chart_type: str) -> str:
    """
    Tool for providing information about different Plotly chart types and their data requirements.

    Args:
        chart_type (str): The type of chart (e.g., "bar", "pie", "line").

    Returns:
        str: Information about the specified chart type and its data requirements.

    Example:
        >>> result = plotly_chart_type_helper("bar")
        >>> assert "bar chart" in result.lower()
        >>> assert "x" in result and "y" in result
    """
    info = {
        "bar": "Bar charts require 'x' (categories) and 'y' (values) data. Example: {'x': ['A', 'B', 'C'], 'y': [1, 2, 3]}",
        "pie": "Pie charts require 'labels' and 'values' data. Example: {'labels': ['A', 'B', 'C'], 'values': [30, 40, 30]}",
        "line": "Line charts require 'x' (typically time or ordered categories) and 'y' (values) data. Example: {'x': [1, 2, 3, 4], 'y': [10, 15, 13, 17]}",
        "scatter": "Scatter plots require 'x' and 'y' data for each point. Example: {'x': [1, 2, 3, 4], 'y': [10, 15, 13, 17]}",
        "histogram": "Histogram plots require only 'x', however a list of frequencies can be passed in 'y'. Example: {'x': ['A', 'B', 'C'], 'y': [1, 2, 3]} or {'x': ['A', 'B', 'B', 'C', 'C', 'C'], 'y': []}",
    }
    return info.get(
        chart_type.lower(),
        "Chart type not recognized. Available types: bar, pie, line, scatter, histogram",
    )
