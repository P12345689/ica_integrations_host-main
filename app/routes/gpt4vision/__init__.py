# -*- coding: utf-8 -*-
"""
GPT4Vision Integration
"""

__author__ = "Chris Hay"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-01-14"
__email__ = "chris.hay@uk.ibm.com"
__status__ = "Alpha"
__description__ = "GPT4Vision Integration"

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
