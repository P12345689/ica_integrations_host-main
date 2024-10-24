# -*- coding: utf-8 -*-
"""
Pytest for nvidia route.

Description: Tests nvidia route.

Authors: Iozu Sebastian
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_nvidia_neva():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "What is in this image?",
            "image_url": "https://bellard.org/bpg/2small.png",
            "model": "",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/nvidia/neva22b/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nvidia_neva_broken_image():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "What is in this image?",
            "image_url": "https://.org/bpg/2small.png",
            "model": "",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/nvidia/neva22b/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nvidia_llm():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "What is 1+1?",
            "image_url": "",
            "model": "llama3-chatqa-1.5-70b",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/nvidia/llm/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nvidia_llm_empty():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"query": "", "image_url": "", "model": ""}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/nvidia/llm/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nvidia_image_stabledif():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "Generate an image of a penguin in a suit",
            "image_url": "",
            "model": "stable-diffusion-3-medium",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/nvidia/image/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nvidia_image_sdxl():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "Generate an image of a penguin in a suit",
            "image_url": "",
            "model": "sdxl-turbo",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/nvidia/image/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nvidia_image_stable_xl():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "Generate an image of a penguin in a suit",
            "image_url": "",
            "model": "stable-diffusion-xl",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/nvidia/image/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nvidia_image_sdxl_lightning():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "Generate an image of a penguin in a suit",
            "image_url": "",
            "model": "sdxl-lightning",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/nvidia/image/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_nvidia_image_no_model():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "Generate an image of a penguin in a suit",
            "image_url": "",
            "model": "",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/nvidia/image/invoke", json=payload, headers=headers)
    assert response.status_code == 200
