# -*- coding: utf-8 -*-
"""
LIBICA - IBM Consulting Assistants Extensions API - Python SDK - Error Handlers.

Description: Error Handlers

Authors: Mihai Criveti
"""

from __future__ import annotations

import logging

# --------------------------------------------------------------------
# Initialize logging
# --------------------------------------------------------------------

log = logging.getLogger(__name__)


# --------------------------------------------------------------------
# Exception Classes
# --------------------------------------------------------------------
class ICAClientError(Exception):
    """Custom exception class for ICAClient errors.

    Args:
        message (str): The error message.

    Raises:
        ICAClientError: If an error occurs within ICAClient.

    Examples:
        >>> try:
        ...     raise ICAClientError("An error occurred.")
        ... except ICAClientError as e:
        ...     print(str(e))
        An error occurred.
    """

    def __init__(self, message):
        """Initialize the ICAClientError with a specific error message.

        This constructor method initializes a new instance of ICAClientError with the provided error message.

        Args:
            message (str): The error message to be displayed when the exception is raised.
        """
        super().__init__(message)
