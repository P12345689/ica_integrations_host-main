# -*- coding: utf-8 -*-
# """
# Pytest for docbuilder route.

# Description: Tests docbuilder route.

# Authors: Gytis Oziunas
# """

from fastapi.testclient import TestClient

from app.server import app

client = TestClient(app)


def test_summarize_text_endpoint():
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/experience/summarize/summarize_text/invoke",
        json={
            "text": "This is a long text to summarize...",
            "max_tokens": 1024,
            "summary_type": "bullets",
            "summary_length": "short",
            "output_format": "markdown",
            "style": "casual",
            "additional_instruction": "Translate to Spanish",
            "chain_type": "map_reduce",
            "context_length": 4096,
            "temperature": 0.7,
            "chunk_size": 1000,
            "chunk_overlap": 200,
        },
        headers=headers,
    )
    assert response.status_code == 200
    assert "Resumen" in response.json()["response"][0]["message"]
    assert "invocationId" in response.json()


def test_get_text_stats():
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/system/summarize/retrievers/get_text_stats/invoke",
        json={"text": "This is a sample text."},
        headers=headers,
    )
    assert response.status_code == 200
    assert "invocationId" in response.json()
