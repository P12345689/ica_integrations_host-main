# -*- coding: utf-8 -*-
"""
autogen_newsletter Route.

This module provides functionality for Detailed description of your integration.
"""

__author__ = "Stan Furrer"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-18-10"
__email__ = "stan.furrer@ibm.com"
__status__ = "Alpha"
__description__ = "Provides newsletter functionality by using a multi-agent setup"

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
