# -*- coding: utf-8 -*-
"""
mvs_zos_logo Route

This module provides functionality for Generate MVS and z/OS login screens.
"""

__author__ = "Name of the author"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-07-10"
__email__ = "example@email.com"
__status__ = "Alpha"
__description__ = "Generate MVS and z/OS login screens"

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
