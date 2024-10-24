# -*- coding: utf-8 -*-
import logging

from fastapi import FastAPI, Request

from app.utilities.request_utilities import api_wrapper

# tools
from .tools.website_tools import is_healthy_async, is_website_up_async

# set the logger
log = logging.getLogger(__name__)


def add_custom_routes(app: FastAPI):
    @app.get("/system/website/retrievers/check_website_up/invoke")
    @app.post("/system/website/retrievers/check_website_up/invoke")
    async def check_website_up(request: Request):
        async def check_website_up_response(data):
            # set the format
            url = data["url"]

            # get the text between markers
            website_up = await is_website_up_async(url)

            # return the messages
            return [
                {
                    "message": f"The url: {url} is {'UP' if website_up else 'DOWN'}",
                    "type": "text",
                },
                {"is_website_up": website_up, "type": "text"},
            ]

        # execute health check
        return await api_wrapper(check_website_up_response, request)

    @app.post("/system/website/retrievers/check_website_health/invoke")
    async def check_website_health(request: Request):
        async def check_website_health_response(data):
            # set the format
            url = data["url"]

            # get the text between markers
            healthy = await is_healthy_async(url)

            # return the messages
            return [
                {
                    "message": f"The health endpoint for: {url} is {'HEALTHY' if healthy else 'NOT HEALTHY'}",
                    "type": "text",
                },
                {"healthy": healthy, "type": "text"},
            ]

        # execute health check
        return await api_wrapper(check_website_health_response, request)
