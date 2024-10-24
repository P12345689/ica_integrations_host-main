# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Creates XLSX files from CSV data or from a natural language prompt

This module provides routes for XLSX generation, including a system route
for generating an XLSX from CSV data, and an experience route that
uses an LLM to interpret a natural language request and create an XLSX file.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class CSVInputModel(BaseModel):
    """Model to validate input data for XLSX generation from CSV."""

    csv_data: Dict[str, str] = Field(..., description="Dictionary of CSV data strings keyed by sheet name")
    file_name: Optional[str] = Field(default=None, description="Optional file_name for the excel to be generated")


class ExperienceInputModel(BaseModel):
    """Model to validate input data for the experience route."""

    query: str = Field(..., description="The input query describing the desired XLSX content")


class ResponseMessageModel(BaseModel):
    """Model to validate the response message."""

    message: str
    type: str = "text"


class OutputModel(BaseModel):
    """Model to structure the output response."""

    status: str = Field(default="success")
    invocationId: str
    response: List[ResponseMessageModel]
