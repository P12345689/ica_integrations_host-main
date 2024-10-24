# -*- coding: utf-8 -*-
"""
userstory_excel_mapper Route

This integration provides functionality for generating user stories from the given requirements.
Input: Requirement list
Output: An excel file with the User story details for all the reqirements
This excel can be used to bulk import the user stories to JIRA.

"""

__author__ = "Charan Kumar Samudrala"
__copyright__ = "IBM"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2024-07-26"
__email__ = "csamudra@in.ibm.com"
__status__ = "Alpha"
__description__ = "Generates user stories for the given requirements and also generates an excel with all the details"

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
