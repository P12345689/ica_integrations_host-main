# -*- coding: utf-8 -*-
"""
plotly Route

This module provides functionality for Generate charts using Plotly, returning an interactive HTML.
"""

__author__ = "Mihai Criveti"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-06-24"
__email__ = "crmihai1@ie.ibm.com"
__status__ = "Alpha"
__description__ = "Generate charts using Plotly, returning an interactive HTML"

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
