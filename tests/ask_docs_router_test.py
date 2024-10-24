# -*- coding: utf-8 -*-

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_get_ask_docs_route():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        # Test case 1: Valid input
        input_data = {
            "collection_ids": ["66142f5a2dd4fae8aa4d5781"],
            "document_names": ["Sidekick AI API Documentation - Early Adopters 4.5.pdf"],
            "query": "What is the API endpoint used to retrieve document collections?",
            "refresh": False
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/experience/docs/ask_docs/invoke",
            json=input_data,
            headers=headers,
        )
        assert response.status_code == 200
        assert response.json()["status"] == "success"


@pytest.mark.asyncio
async def test_get_ask_docs_route_invalid_input():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        input_data = {
            "collection_ids": ["randomID"],
            "document_names": ["Sidekick AI API Documentation - Early Adopters 4.5.pdf"],
            "query": "What is the API endpoint used to retrieve document collections?",
            "refresh": False
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/experience/docs/ask_docs/invoke",
            json=input_data,
            headers=headers,
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_ask_docs_route_empty_input():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        input_data = {}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/experience/docs/ask_docs/invoke",
            json=input_data,
            headers=headers,
        )
        assert response.status_code == 422
