# -*- coding: utf-8 -*-
"""
Pytest for googlesearch route.

Description: Tests google search route.

Authors: Gytis Oziunas
"""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_googlesearch_endpoint_success():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"query": "What is DnD?"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/googlesearch/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_googlesearch_endpoint_no_query():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"query": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/googlesearch/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_googlesearch_endpoint_wrong_query():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"input": "1"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/googlesearch/invoke", json=payload, headers=headers)
    assert response.status_code == 200
