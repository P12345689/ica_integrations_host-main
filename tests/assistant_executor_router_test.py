# -*- coding: utf-8 -*-
"""
Pytest for assistant_executor route.

Description: Tests assistant_executor route.

Authors: Iozu Sebastian
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_assistant_executor_route():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "3903", "prompt": "app to open car trunk with face"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant_executor/retrievers/assistant/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_executor_empty_prompt():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "3903", "prompt": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant_executor/retrievers/assistant/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_assistant_executor_empty_assistant():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "", "prompt": "app to open car trunk with face"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant_executor/retrievers/assistant/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_assistant_executor_wrong_assistant():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "1", "prompt": "app to open car trunk with face"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant_executor/retrievers/assistant/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_assistant_executor_no_input():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "", "prompt": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant_executor/retrievers/assistant/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 400
