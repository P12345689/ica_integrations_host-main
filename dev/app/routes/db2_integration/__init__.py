# -*- coding: utf-8 -*-
"""
db2_integration Route

This module provides functionality for Connect and fetch data from an IBM DB2 Warehouse.
"""

__author__ = "Andre Gheilerman"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-09-12"
__email__ = "andre.gheilerman@ibm.com"
__status__ = "Alpha"
__description__ = "Connect and fetch data from an IBM DB2 Warehouse"

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
