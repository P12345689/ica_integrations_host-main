# -*- coding: utf-8 -*-
"""
Pytest for ask_assistant route.

Description: Tests ask_assistant route.

Authors: Iozu Sebastian
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_ask_assistant_empty_data():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"tags": [""], "refresh": True}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant/retrievers/get_assistants/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ask_assistant_get_tag():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"tags": ["unified"], "refresh": True}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant/retrievers/get_assistants/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ask_assistant_get_role():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"roles": ["Software Developer"], "refresh": True}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant/retrievers/get_assistants/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ask_assistant_get_keyword():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"search_term": "Python", "refresh": True}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant/retrievers/get_assistants/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ask_assistant_get_id():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"assistant_id": "3909", "refresh": True}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/assistant/retrievers/get_assistants/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ask_assistant_llm():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "Which assistants can help me generate Python code?",
            "tags": ["Developer", "Code Generation"],
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/experience/assistant/ask_assistant/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_ask_assistant_llm_by_id():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "What are the capabilities of the assistant with ID 3903?",
            "assistant_id": "3903",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/experience/assistant/ask_assistant/invoke", json=payload, headers=headers)
    assert response.status_code == 200
