# -*- coding: utf-8 -*-
"""
Pytest for mermaid route.

Description: Tests mermaid route.

Authors: Andrei Colhon
"""

from unittest import mock
from unittest.mock import AsyncMock, patch
from wsgiref import headers

from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, HTTPError

from app.routes.mermaid.mermaid_router import MermaidRequest
from app.routes.mermaid.mermaid_router import (
    convert_mermaid_text_to_syntax,
    generate_mermaid_image,
)

from app.server import app

client = TestClient(app)


@pytest.mark.asyncio
@patch("app.routes.mermaid.mermaid_router.LLMChain.run")
async def test_convert_mermaid_text_to_syntax(mock_llm_chain):
    # Mock response from LLM
    mock_llm_chain.return_value = "graph TB\nA-->B"

    # Define input data
    mermaid_request = MermaidRequest(
        query="A simple mindmap", chart_type="mindmap", style="default", direction="TB"
    )

    # Call the function
    response = await convert_mermaid_text_to_syntax(mermaid_request)

    # Assert the response
    assert response == "graph TB\nA-->B"


@pytest.mark.asyncio
@patch("app.tools.global_tools.mermaid_tool.syntax_to_image")
async def test_generate_mermaid_image(mock_syntax_to_img):
    mock_syntax_to_img.return_value = "test_url.com"

    mermaid_syntax = "graph TB\nA-->B"

    url = await generate_mermaid_image(mermaid_syntax)

    assert "http://localhost:8080/public/images/mermaid" in url


@pytest.mark.asyncio
@patch("app.routes.mermaid.mermaid_router.convert_mermaid_text_to_syntax")
@patch("app.routes.mermaid.mermaid_router.generate_mermaid_image")
async def test_mermaid_text_to_image(mock_mermaid_image, mock_mermaid_text_to_syntax):
    payload = {
        "query": "A simple mindmap",
        "chart_type": "mindmap",
        "style": "default",
        "direction": "TB",
    }

    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    mock_mermaid_image.return_value = "test_url.com"
    mock_mermaid_text_to_syntax.return_value = "graph TB\nA-->B"

    response = client.post(
        "/experience/mermaid/transformers/text_to_image/invoke",
        json=payload,
        headers=headers,
    )

    assert "success" in response.text
    assert "response" in response.text
    assert "invocationId" in response.text
    assert response.status_code == 200


@patch("app.routes.mermaid.mermaid_router.convert_mermaid_text_to_syntax")
def test_mermaid_text_to_syntax(mock_mermaid_text_to_syntax):
    payload = {
        "query": "A simple mindmap",
        "chart_type": "mindmap",
        "style": "default",
        "direction": "TB",
    }

    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    mock_mermaid_text_to_syntax.return_value = "graph TB\nA-->B"

    response = client.post(
        "/experience/mermaid_service/transformers/text_to_syntax/invoke",
        json=payload,
        headers=headers,
    )

    assert "success" in response.text
    assert "response" in response.text
    assert "invocationId" in response.text
    assert response.status_code == 200


@patch("app.routes.mermaid.mermaid_router.generate_mermaid_image")
def test_mermaid_syntax_to_image(mock_mermaid_generate_image):
    payload = {
        "query": "A simple mindmap",
        "chart_type": "mindmap",
        "style": "default",
        "direction": "TB",
    }

    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    mock_mermaid_generate_image.return_value = "test_url.com"

    response = client.post(
        "/system/mermaid_service/transformers/syntax_to_image/invoke",
        json=payload,
        headers=headers,
    )

    assert "success" in response.text
    assert "response" in response.text
    assert "invocationId" in response.text
    assert response.status_code == 200
