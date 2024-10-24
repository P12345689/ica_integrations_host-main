# -*- coding: utf-8 -*-
"""
Pytest for jokes route.

Description: Tests jokes route using mock LLM response.

Authors: Mihai Criveti
"""

from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from app.server import app

client = TestClient(app)


def test_joke_endpoint():
    test_data = {"input": "chicken"}
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    expected_response = {
        "status": "success",
        "invocationId": "",
        "response": [
            {
                "message": "Why did the chicken cross the road? To get to the other side!",
                "type": "text",
            }
        ],
    }

    with (
        patch("app.routes.jokes.jokes_router.ChatConsultingAssistants") as mock_model,
        patch("app.routes.jokes.jokes_router.ChatPromptTemplate") as mock_prompt,
        patch("app.routes.jokes.jokes_router.LLMChain") as mock_llm_chain,
    ):
        mock_model.return_value = AsyncMock()
        mock_prompt.from_template.return_value = AsyncMock()
        mock_llm_chain.return_value.run.return_value = "Why did the chicken cross the road? To get to the other side!"

        response = client.post(
            "/experience/joke/retrievers/get_joke/invoke",
            json=test_data,
            headers=headers,
        )
        assert response.status_code == 200
        # assert response.json() == expected_response
