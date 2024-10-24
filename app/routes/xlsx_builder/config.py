# -*- coding: utf-8 -*-
"""
Author: Mihai Criveti
Description: Creates XLSX files from CSV data or from a natural language prompt

This module provides routes for XLSX generation, including a system route
for generating an XLSX from CSV data, and an experience route that
uses an LLM to interpret a natural language request and create an XLSX file.
"""

import os
from typing import List, Tuple

# Set up logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# Set default models, prompt templates, and max threads from environment variables
DEFAULT_MODEL_PROMPT_PAIRS: List[Tuple[str, str]] = [
    ("OpenAI GPT4o", "prompt_1.jinja"),
    (
        os.getenv("ASSISTANTS_DEFAULT_MODEL_ID_OR_NAME", "Llama3.1 70b Instruct"),
        "prompt_2.jinja",
    ),
    ("Llama3 8B Instruct", "prompt_2.jinja"),
    ("Mixtral Large", "prompt_2.jinja"),
]
DEFAULT_MAX_THREADS: int = int(os.getenv("DEFAULT_MAX_THREADS", "4"))
MAX_RETRIES: int = 4

# Load the server URL from an environment variable (localhost or remote)
SERVER_NAME: str = os.getenv("SERVER_NAME", "http://127.0.0.1:8080")

# Template directory
TEMPLATE_DIR: str = "app/routes/xlsx_builder/templates"

# Public directory for XLSX files
PUBLIC_DIR: str = "public/xlsx_builder"
