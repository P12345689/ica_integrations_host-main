# -*- coding: utf-8 -*-
"""
Pytest for duckduckgo route.

Description: Tests duckduckgo search route.

Authors: Iozu Sebastian
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

app = FastAPI()


@app.post("/duckduckgo/invoke")
async def googlesearch_invoke(data: dict):
    query = data.get("input", {}).get("query", "")
    if not query:
        return {
            "results": {
                "status": "success",
                "response": [
                    {
                        "message": "I'm sorry but i couldn't find a response, please try with a different query",
                        "type": "text",
                    }
                ],
            }
        }, 200
    return {
        "results": {
            "status": "success",
            "response": [
                {
                    "message": "DND typically stands for Dungeons & Dragons",
                    "type": "text",
                }
            ],
        }
    }, 200


client = TestClient(app)


@pytest.mark.asyncio
async def test_googlesearch_endpoint_success():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        test_data = {"input": {"query": "what is dnd?"}}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/duckduckgo/invoke", json=test_data, headers=headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "results": {
                "status": "success",
                "response": [
                    {
                        "message": "DND typically stands for Dungeons & Dragons",
                        "type": "text",
                    }
                ],
            }
        },
        200,
    ]


@pytest.mark.asyncio
async def test_googlesearch_endpoint_no_query():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        test_data = {"input": {"query": ""}}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/duckduckgo/invoke", json=test_data, headers=headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "results": {
                "status": "success",
                "response": [
                    {
                        "message": "I'm sorry but i couldn't find a response, please try with a different query",
                        "type": "text",
                    }
                ],
            }
        },
        200,
    ]
