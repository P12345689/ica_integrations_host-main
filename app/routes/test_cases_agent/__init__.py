# -*- coding: utf-8 -*-
"""
test_cases_agent Route

This module provides functionality for Generate manual test cases based on user story and generates an excel with all the details of the test cases.
"""

__author__ = "Shrishti"
__copyright__ = "IBM"
__license__ = "IBM"
__version__ = "0.1.0"
__date__ = "2024-08-27"
__email__ = "shrishti.shrishti@ibm.com"
__status__ = "Alpha"
__description__ = "Generate manual test cases based on user story and generates an excel with all the details of the test cases"

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
