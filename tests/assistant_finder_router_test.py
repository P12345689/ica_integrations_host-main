# -*- coding: utf-8 -*-
"""
Pytest for assistant_finder route.

Description: Tests assistant_finder route.

Authors: Iozu Sebastian
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_assistant_finder_route():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"description": "I need help with data analysis",
                   "tags": "SDLC Assistants",
                   "roles": "Software Developer"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_finder/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_finder_empty_description():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"description": "",
                   "tags": "SDLC Assistants",
                   "roles": "Software Developer"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_finder/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_finder_empty_tags():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"description": "I need help with data analysis",
                   "tags": "",
                   "roles": "Software Developer"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_finder/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_finder_empty_tags_and_roles():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"description": "I need help with data analysis",
                   "tags": "",
                   "roles": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_finder/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_finder_empty_roles():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"description": "I need help with data analysis",
                   "tags": "SDLC Assistants",
                   "roles": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_finder/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_assistant_finder_no_input():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"description": "",
                   "tags": "",
                   "roles": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/assistant_finder/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200
