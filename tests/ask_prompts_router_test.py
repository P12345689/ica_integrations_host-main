# -*- coding: utf-8 -*-

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_prompts_route():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        # Test case 1: Valid input
        input_data = {
            "tags": ["tag1", "tag2"],
            "roles": ["role1", "role2"],
            "search_term": "search",
            "visibility": "PUBLIC",
            "user_email": "user@example.com",
            "prompt_id": "123",
            "refresh": True,
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/prompt/retrievers/get_prompts/invoke",
            json=input_data,
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_get_prompts_route_invalid_input():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        input_data = {
            "tags": "invalid",
            "roles": ["role1", "role2"],
            "search_term": "search",
            "visibility": "PUBLIC",
            "user_email": "user@example.com",
            "prompt_id": "123",
            "refresh": True,
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/prompt/retrievers/get_prompts/invoke",
            json=input_data,
            headers=headers,
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_get_prompts_route_empty_input():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        input_data = {}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/prompt/retrievers/get_prompts/invoke",
            json=input_data,
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["status"] == "success"
