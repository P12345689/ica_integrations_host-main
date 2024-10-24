# -*- coding: utf-8 -*-
"""
LLM Route returns curl formatted output of received parameters.
"""

__author__ = "Adrian POpa"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-01-14"
__email__ = "adrian.popa@ro.ibm.com"
__status__ = "Alpha"
__description__ = "Implements a crewAI dynamic agent that defines the agents from JSON using as tools ICA integrations reffered by name"

import logging
import os

if os.getenv("DEBUG") == "1":
    logging.getLogger().setLevel(logging.DEBUG)
