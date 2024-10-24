# -*- coding: utf-8 -*-
"""
Pytest for plotly route.

Description: Tests plotly route.

Authors: Iozu Sebastian
"""

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
async def test_plotly_system_empty_data():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "chart_type": "bar",
            "data": {"x": [], "y": []},
            "title": "Sample Bar Chart",
            "format": "HTML",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/plotly/generate_chart/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plotly_system_bar():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "chart_type": "bar",
            "data": {"x": ["A", "B", "C", "D"], "y": [1, 4, 2, 3]},
            "title": "Sample Bar Chart",
            "format": "HTML",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/plotly/generate_chart/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plotly_system_line():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "chart_type": "line",
            "data": {"x": ["A", "B", "C", "D"], "y": [1, 4, 2, 3]},
            "title": "Sample Line Chart",
            "format": "HTML",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/plotly/generate_chart/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plotly_system_pie():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "chart_type": "pie",
            "data": {"x": ["A", "B", "C", "D"], "y": [1, 4, 2, 3]},
            "title": "Sample Pie Chart",
            "format": "HTML",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/plotly/generate_chart/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plotly_system_scatter():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "chart_type": "scatter",
            "data": {"x": ["A", "B", "C", "D"], "y": [1, 4, 2, 3]},
            "title": "Sample Scatter Chart",
            "format": "HTML",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/plotly/generate_chart/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plotly_system_histogram():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "chart_type": "histogram",
            "data": {"x": ["A", "A", "A", "B", "B", "C", "D", "D"], "y": []},
            "title": "Sample Histogram Chart",
            "format": "HTML",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/plotly/generate_chart/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plotly_system_histogram_with_frequency():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "chart_type": "histogram",
            "data": {"x": ["A", "B", "C", "D"], "y": [1, 4, 2, 3]},
            "title": "Sample Histogram Chart",
            "format": "HTML",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/plotly/generate_chart/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plotly_llm():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {
            "query": "Create a pie chart showing the distribution of fruits: 30% apples, 25% bananas, 20% oranges, "
            "and 25% grapes",
            "format": "HTML",
        }
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/experience/plotly/generate_chart/invoke", json=payload, headers=headers)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_plotly_llm_empty_input():
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        payload = {"query": "", "format": "HTML"}
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/experience/plotly/generate_chart/invoke", json=payload, headers=headers)
    assert response.status_code == 422
