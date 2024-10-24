# -*- coding: utf-8 -*-
"""
graphql_mapper_function Route

This module provides functionality for integration provides a rag solution for ingesting graphql schemas. Users can input a rest response and the matching mapper function is created.
"""

__author__ = "Oluwole Obamakin"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-07-10"
__email__ = "Oluwole.Obamakin@ibm.com"
__status__ = "Alpha"
__description__ = "integration provides a rag solution for ingesting graphql schemas. Users can input a rest response and the matching mapper function is created"

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
