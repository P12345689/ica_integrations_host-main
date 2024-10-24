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
async def test_python_executor_execute():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "code": "def custom_sum(numbers):\n    return sum(numbers)\nnumbers = [1, 2, 3, 4, 5]\nresult = custom_sum(numbers)\nprint(result)"
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/python_executor/execute_code/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_python_executor_empty_code():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "code": ""
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/python_executor/execute_code/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_python_executor_wrong_code():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "code": "def custom_sum(numbers):\n    return WRONG VARIABLE NAME\nnumbers = [1, 2, 3, 4, 5]\nresult = custom_sum(numbers)\nprint(result)"
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/python_executor/execute_code/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_python_executor_generate():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"query": "Calculate the factorial of 5"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/experience/python_executor/generate_and_execute/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_python_executor_generate_no_query():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"query": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/experience/python_executor/generate_and_execute/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_python_executor_generate_wrong_query():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"query": "aaa"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/experience/python_executor/generate_and_execute/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200
