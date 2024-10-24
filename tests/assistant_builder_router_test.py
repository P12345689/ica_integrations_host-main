# -*- coding: utf-8 -*-
"""
Pytest for assistant_builder route.

Description: Tests assistant_builder route.

Authors: Iozu Sebastian
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_assistant_builder_route():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"input": "Assistant to write user stories"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_builder/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_builder_empty_data():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"input": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_builder/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_builder_no_input():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"input": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_builder/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200
