# -*- coding: utf-8 -*-
"""
Pytest for plantUML route.

Description: Tests plantUML route.

Authors: Iozu Sebastian
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_plantuml_route():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "description": "@startuml\nAlice -> Bob: Hello Bob, how are you?\nBob --> Alice: I am fine, thanks!\n@enduml"
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/plantuml/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plantuml_empty_description():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"description": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/plantuml/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_plantuml_wrong_description():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "description": "Bob --> Alice: I am fine, thanks!\n@enduml"
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/plantuml/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plantuml_system_call():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "description": "@startuml\nAlice -> Bob: Hello Bob, how are you?\nBob --> Alice: I am fine, thanks!\n@enduml"
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/plantuml/transformers/syntax_to_image/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plantuml_empty_system_call():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "description": ""
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/plantuml/transformers/syntax_to_image/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_plantuml_wrong_description_system_call():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "description": "Bob --> Alice: I am fine, thanks!\n@enduml"
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/plantuml/transformers/syntax_to_image/invoke",
            json=payload,
            headers=headers,
        )
    assert response.status_code == 200
