# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Creates charts using matplotlib, returning a PNG

This module provides routes for chart generation, including a system route
for generating a PNG from chart data, and an experience route that
uses an LLM to interpret a natural language request and create a chart.
"""

from typing import Dict, List, Any
from pydantic import BaseModel, Field
from typing import Optional


class CSVInputModel(BaseModel):
    """Model to validate input data for chart generation from CSV."""

    chart_type: str = Field(
        ..., description="Type of chart (e.g., 'bar', 'pie', 'line')"
    )
    csv_data: str = Field(..., description="CSV data as a string")
    sheet_name: str = Field(
        default="Sheet1", description="Name of the sheet in the XLSX file"
    )
    title: str = Field(default="", description="Title of the chart")

# class DataModel(BaseModel):
#     x: Optional[List[Any]] = Field(None, description="X-values for the chart")
#     y: Optional[List[Any]] = Field(None, description="Y-values for the chart")
#     values: Optional[List[Any]] = Field(None, description="Values for the pie chart")
#     labels: Optional[List[Any]] = Field(None, description="Labels for the pie chart")
#     x_label: Optional[str] = Field(None, description="Label for the X-axis")
#     y_label: Optional[str] = Field(None, description="Label for the Y-axis")

class ChartInputModel(BaseModel):
    """Model to validate input data for chart generation."""

    chart_type: str = Field(
        ..., description="Type of chart (e.g., 'bar', 'pie', 'line')"
    )
    data: Dict[str, List[Any]] = Field(..., description="Data for the chart")
    title: str = Field(default="", description="Title of the chart")
    x_label: Optional[str] = Field(None, description="Label for the X-axis")
    y_label: Optional[str] = Field(None, description="Label for the Y-axis")



class ExperienceInputModel(BaseModel):
    """Model to validate input data for the experience route."""

    query: str = Field(..., description="The input query describing the desired chart")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str  # noqa: N815
    response: List[ResponseMessageModel]
