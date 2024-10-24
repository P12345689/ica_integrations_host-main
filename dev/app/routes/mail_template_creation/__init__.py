# -*- coding: utf-8 -*-
"""
mail_template_creation Route

This module provides functionality for Integration for email generation based on template.
"""

__author__ = "Freddy Hernandez Rojas"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-07-24"
__email__ = "frhernan@cr.ibm.com"
__status__ = "Alpha"
__description__ = "Integration for email generation based on template"

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
