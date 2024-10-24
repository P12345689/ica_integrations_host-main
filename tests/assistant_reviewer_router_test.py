# -*- coding: utf-8 -*-
"""
Pytest for assistant_reviewer route.

Description: Tests assistant_reviewer route.

Authors: Iozu Sebastian
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_assistant_reviewer_route():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "3903", "assistant_input": "test input", "assistant_output": "test output"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_reviewer/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_finder_empty_assistant():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "", "assistant_input": "test input", "assistant_output": "test output"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_reviewer/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_assistant_finder_empty_input():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "3903", "assistant_input": "", "assistant_output": "test output"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_reviewer/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_finder_empty_output():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "3903", "assistant_input": "test input", "assistant_output": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_reviewer/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_finder_empty_input_output():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "3903", "assistant_input": "", "assistant_output": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_reviewer/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200
