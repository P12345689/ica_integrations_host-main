# -*- coding: utf-8 -*-

from fastapi import FastAPI, Request


def add_custom_routes(app: FastAPI):
    @app.api_route("/health", methods=["GET", "POST", "PUT", "DELETE"])
    async def get_health(request: Request):
        # return ok
        return "OK"
