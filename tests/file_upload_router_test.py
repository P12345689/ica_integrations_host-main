# -*- coding: utf-8 -*-
"""
Pytest for file_upload route.

Description: Tests file_upload route.

Authors: Iozu Sebastian
"""

from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)
file_name = ""


@pytest.mark.asyncio
async def test_file_upload_get_url():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        input_data = {
            "team_id": "team123",
            "user_email": "user@example.com"
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/file_upload/retrievers/get_upload_url/invoke",
            json=input_data,
            headers=headers,
        )
        assert response.status_code == 200
        assert "/file_upload_ui" in response.json()["response"][0]["message"]


@pytest.mark.asyncio
async def test_file_upload_upload():
    global file_name
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        input_data = {
            "team_id": "team123",
            "user_email": "user@example.com",
            "key": "4f0f3db1e03cd0046918d748622160f687db2dfc9d8047d4a73eb2e8c38e6efa",
            "file_path": "README.md"
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/system/file_upload/upload",
            json=input_data,
            headers=headers,
        )
        tmp_file = response.json()["file_name"]
        file_path = Path(
            f"public/userfiles/4f0f3db1e03cd0046918d748622160f687db2dfc9d8047d4a73eb2e8c38e6efa/{tmp_file}")
        assert response.status_code == 200
        assert file_path.exists()
        file_name = tmp_file


@pytest.mark.asyncio
async def test_file_upload_list_files():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.get(
            "/system/file_upload/list?key=4f0f3db1e03cd0046918d748622160f687db2dfc9d8047d4a73eb2e8c38e6efa&team_id=team123&user_email=user@example.com",
            headers=headers,
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_file_upload_download_file():
    global file_name
    if not file_name:
        pytest.skip("Skipping test because file_name is empty")

    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.get(
            f"/system/file_upload/download/{file_name}?key=4f0f3db1e03cd0046918d748622160f687db2dfc9d8047d4a73eb2e8c38e6efa&team_id=team123&user_email=user@example.com",
            headers=headers,
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_file_upload_ask_files():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        input_data = {
            "team_id": "team123",
            "user_email": "user@example.com",
            "query": "What files do I have?"
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            f"/experience/file_upload/ask_about_files/invoke",
            json=input_data,
            headers=headers,
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_file_upload_delete_file():
    global file_name
    if not file_name:
        pytest.skip("Skipping test because file_name is empty")

    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.delete(
            f"/system/file_upload/delete/{file_name}?key=4f0f3db1e03cd0046918d748622160f687db2dfc9d8047d4a73eb2e8c38e6efa&team_id=team123&user_email=user@example.com",
            headers=headers,
        )
        file_path = Path(
            f"public/userfiles/4f0f3db1e03cd0046918d748622160f687db2dfc9d8047d4a73eb2e8c38e6efa/{file_name}")
        assert response.status_code == 200
        assert not file_path.exists()
        file_name = ""
