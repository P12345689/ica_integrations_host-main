# -*- coding: utf-8 -*-
"""
{{ cookiecutter.module_name }} Route

This module provides functionality for {{ cookiecutter.description }}.
"""

__author__ = "{{ cookiecutter.author }}"
__copyright__ = "{{ cookiecutter.copyright }}"
__license__ = "{{ cookiecutter.license }}"
__version__ = "{{ cookiecutter.version }}"
__date__ = "{{ cookiecutter.date }}"
__email__ = "{{ cookiecutter.email }}"
__status__ = "{{ cookiecutter.status }}"
__description__ = "{{ cookiecutter.description }}"

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
