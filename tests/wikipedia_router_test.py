# -*- coding: utf-8 -*-
"""
Pytest for wikipedia route.

Description: Tests Wikipedia route.

Authors: Andrei Colhon
"""

from unittest import mock
from unittest.mock import AsyncMock, patch
from wsgiref import headers

from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient

from app.server import app

client = TestClient(app)

from app.routes.wikipedia.wikipedia_router import (
    ResultsType,
    WikipediaSearchInput,
    search_wikipedia,
)


@pytest.mark.asyncio
async def test_search_wikipedia_summary():
    test_data = WikipediaSearchInput(
        search_string="Python programming", results_type=ResultsType.summary, llm="base"
    )

    search_result = await search_wikipedia(test_data)

    assert search_result.get("summary") != ""
    assert search_result.get("content") == ""
    assert search_result.get("article_url") != ""
    assert search_result.get("image_url") != ""


@pytest.mark.asyncio
async def test_search_wikipedia_full():
    test_data = WikipediaSearchInput(
        search_string="Python programming", results_type=ResultsType.full, llm="base"
    )

    search_result = await search_wikipedia(test_data)

    assert search_result.get("summary") == ""
    assert search_result.get("content") != ""
    assert search_result.get("article_url") != ""
    assert search_result.get("image_url") != ""


@pytest.mark.asyncio
async def test_search_wikipedia_disambiguation():
    test_data = WikipediaSearchInput(
        search_string="python", results_type=ResultsType.full, llm="base"
    )

    search_result = await search_wikipedia(test_data)

    assert search_result.get("summary") != ""
    assert search_result.get("content") == ""
    assert search_result.get("article_url") == ""
    assert search_result.get("image_url") == ""


@pytest.mark.asyncio
async def test_wikipedia_invoke():
    test_data = {
        "search_string": "python",
        "results_type": "summary",
        "llm": "base",
    }

    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    response = client.post(
        "/system/wikipedia/retrievers/search/invoke", json=test_data, headers=headers
    )

    assert response.status_code == 200
    assert "success" in response.text
    assert "message" in response.text


@pytest.mark.asyncio
async def test_wikipedia_invoke_bad_request():
    test_data = {
        "bad_input": "python programming",
        "llm": "base",
    }

    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    response = client.post(
        "/system/wikipedia/retrievers/search/invoke", json=test_data, headers=headers
    )

    assert response.status_code == 400
