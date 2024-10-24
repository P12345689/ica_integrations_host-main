# -*- coding: utf-8 -*-
import asyncio
import logging

import httpx
from langchain.agents import tool

# import nest_asyncio

# this is necessary for async wrapping
# nest_asyncio.apply()

# set the logger
log = logging.getLogger(__name__)


# this is considered a system level api
@tool
def is_website_up(url: str) -> bool:
    """This tool will check if the website is up and running for the passed in url.  It will only check if it returns a 200 response"""

    # call the async version
    loop = asyncio.get_event_loop()

    # call it
    return loop.run_until_complete(is_website_up_async(url))


# this is considered a system level api
async def is_website_up_async(url: str) -> bool:
    """This tool will check if the website is up and running for the passed in url.  It will only check if it returns a 200 response"""

    # prefix with https if no prefix provided
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.head(url)

            # check for a successful status code (2xx or 3xx)
            return 200 <= response.status_code < 400
    except httpx.RequestError as e:
        log.debug(e)
        return False


@tool
def is_healthy(url: str) -> bool:
    """This tool will check the health endpoint of the given url.  It will check if the health endpoint returns OK"""

    # call the async version
    loop = asyncio.get_event_loop()

    # call it
    return loop.run_until_complete(is_healthy_async(url))


async def is_healthy_async(url: str) -> bool:
    """This tool will check the health endpoint of the given url.  It will check if the health endpoint returns OK"""
    # prefix with https if no prefix provided
    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url)

            # check for a successful status code (2xx or 3xx) and ok
            return 200 <= response.status_code < 400 and response.text.strip().lower().__contains__("ok")
    except httpx.RequestError as e:
        log.debug(e)
        return False
