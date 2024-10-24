# -*- coding: utf-8 -*-
import json
import logging
from typing import Any, Callable, Coroutine, Dict
from uuid import uuid4

from fastapi import Request

# set the logger
log = logging.getLogger(__name__)


async def get_request_data(request: Request):
    # get the data
    try:
        data = await request.json()
    except json.JSONDecodeError:
        data = await request.form()

    # return the data
    return data


async def api_wrapper(func: Callable[..., Coroutine], request: Request, *args, **kwargs):
    try:
        # debug
        log.debug(f"Received {request.method} request")

        # create an invocation id
        invocation_id = str(uuid4())

        # Parse JSON data from the request
        data = await get_request_data(request)

        # Call the provided coroutine function with the data and additional arguments
        result = await func(data, *args, **kwargs)
    except Exception as e:
        log.error(f"Unexpected error: {e}")
        return {"status": "error", "message": str(e)}

    # return the result
    response = {
        "status": "success",
        "invocationId": invocation_id,
        "response": result,
    }

    return response


def debug_message(message: str) -> Dict[str, Any]:
    """
    Returns a dictionary with a formatted message for displaying error information on the client UI.

    Args:
        message (str): The error message to be displayed.

    Returns:
        Dict[str, Any]: A dictionary containing the error message.
    """
    log.info(f"Returning error message to client: {message}")
    return {
        "status": "error",
        "response": [
            {
                "message": f"Error: {message}",
                "type": "text",
            }
        ],
    }
