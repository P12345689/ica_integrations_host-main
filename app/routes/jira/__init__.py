# -*- coding: utf-8 -*-
"""
jira Route

This module provides functionality for Integrates with Jira.
"""

__author__ = "Mihai Criveti"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-08-02"
__email__ = "crmihai1@ie.ibm.com"
__status__ = "Alpha"
__description__ = "Integrates with Jira"

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