# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Creates charts using matplotlib, returning a PNG

This module provides routes for chart generation, including a system route
for generating a PNG from chart data, and an experience route that
uses an LLM to interpret a natural language request and create a chart.
"""

import os
from typing import List, Tuple

LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

DEFAULT_MODEL_PROMPT_PAIRS: List[Tuple[str, str]] = [
    (
        os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct"),
        "prompt.jinja",
    ),
    ("Llama3 8B Instruct", "prompt.jinja"),
    ("Mixtral Large", "prompt.jinja"),
]

# Set default model and max threads from environment variables
DEFAULT_MODEL = os.getenv(
    "ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct"
)
DEFAULT_MAX_THREADS = int(os.getenv("DEFAULT_MAX_THREADS", 4))
MAX_RETRIES: int = 4

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME = os.getenv(
    "SERVER_NAME", "http://127.0.0.1:8080"
)  # Default URL as fallback

# Template directory
TEMPLATE_DIR: str = "app/routes/chart/templates"

# Public directory for XLSX files
PUBLIC_DIR: str = "public/chart"
