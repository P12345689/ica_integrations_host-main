# -*- coding: utf-8 -*-
"""
summarizer Route

This module provides functionality for Summarize text using LangChain refine, map_reduce or stuff methods. Supports long context, and multiple options (bullets or paragraphs), short/medium/long summary output, plain text or markdown, business or casual, or translation use cases via the additional instruction..
"""

__author__ = "Mihai Criveti"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-07-18"
__email__ = "crmihai1@ie.ibm.com"
__status__ = "Alpha"
__description__ = "Summarize text using LangChain refine, map_reduce or stuff methods. Supports long context, and multiple options (bullets or paragraphs), short/medium/long summary output, plain text or markdown, business or casual, or translation use cases via the additional instruction."

import logging
import os
import sys

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s: %(name)s:%(funcName)s(%(lineno)d) -- %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    stream=sys.stderr,
    level=logging.INFO,
)

if os.getenv("DEBUG") == "1":
    logging.getLogger().setLevel(logging.DEBUG)
