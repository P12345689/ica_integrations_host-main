# -*- coding: utf-8 -*-
"""
cv_builder Route

This module provides functionality for CV Builder integration.
"""

__author__ = "Freddy Hernandez Rojas"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-07-16"
__email__ = "frhernan@cr.ibm.com"
__status__ = "Alpha"
__description__ = "CV Builder integration"

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
