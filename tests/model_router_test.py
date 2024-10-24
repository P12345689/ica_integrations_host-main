# -*- coding: utf-8 -*-
"""
Pytest for Model Router route.

Description: Tests Model Router route.

Authors: Andrei Colhon
"""

from unittest import mock
from unittest.mock import AsyncMock, patch, mock_open
from wsgiref import headers
import json

from fastapi import HTTPException
import pytest
from fastapi.testclient import TestClient

from app.routes.model_router.model_router_router import (
    compute_cosine_similarity,
    load_configuration,
    rank_options,
    route_prompt,
)
from app.server import app

client = TestClient(app)


def test_load_configuration_success():
    sample_config = {"key": "value"}
    mocked_file_content = json.dumps(sample_config)

    with patch("builtins.open", mock_open(read_data=mocked_file_content)):
        with patch("json.load", return_value=sample_config) as mock_json_load:
            config = load_configuration()
            mock_json_load.assert_called_once()
            assert config == sample_config


def test_load_configuration_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            load_configuration()


def test_load_configuration_invalid_json():
    with patch("builtins.open", mock_open(read_data="{invalid_json: ")):
        with patch(
            "json.load",
            side_effect=json.JSONDecodeError("Expecting value", "line 1", 1),
        ):
            with pytest.raises(json.JSONDecodeError):
                load_configuration()


def test_compute_cosine_similarity():
    text1 = "Hello world"
    text2 = "Hello world"
    assert compute_cosine_similarity(text1, text2) == pytest.approx(
        1.0
    ), "Identical texts should have a cosine similarity of 1"

    text1 = "Hello world"
    text2 = "Goodbye sun"
    assert compute_cosine_similarity(text1, text2) == pytest.approx(
        0.0
    ), "Completely different texts should have a cosine similarity of 0"

    text1 = "Hello world"
    text2 = "Hello sun"
    similarity = compute_cosine_similarity(text1, text2)
    assert (
        0 < similarity < 1
    ), "Partially overlapping texts should have a cosine similarity between 0 and 1"


def test_rank_options():
    prompt = "weather forecast"
    context = {"preferred_type": "model"}
    options = [
        {
            "name": "Weather Predictor",
            "description": "Predicts weather",
            "type": "model",
        },
        {
            "name": "Stock Predictor",
            "description": "Predicts stock prices",
            "type": "model",
        },
        {
            "name": "Recipe Generator",
            "description": "Generates cooking recipes",
            "type": "assistant",
        },
    ]

    ranked_options = rank_options(prompt, context, options)

    scores = [option["score"] for option in ranked_options]
    assert all(
        x >= y for x, y in zip(scores, scores[1:])
    ), "Options should be ranked in descending order of their scores"

    assert (
        ranked_options[0]["name"] == "Weather Predictor"
    ), "The most relevant option should be ranked highest"

    for option in ranked_options:
        print(f"Option: {option['name']}, Score: {option['score']}")


@pytest.fixture
def config():
    """A fixture that returns a sample configuration."""
    return {
        "options": [
            {
                "name": "Model A",
                "description": "A model for testing",
                "type": "model",
                "id": "model_a",
            },
            {
                "name": "Assistant B",
                "description": "An assistant for testing",
                "type": "assistant",
            },
            {
                "name": "Collection C",
                "description": "A collection for testing",
                "type": "document_collection",
            },
        ]
    }


@pytest.mark.asyncio
@patch("libica.ICAClient")
async def test_route_prompt_no_valid_options(mock_ica_client, config):
    """Test routing when no valid options are available."""
    prompt = "Test prompt"
    context = {}
    config["options"] = []

    with pytest.raises(ValueError) as exc_info:
        await route_prompt(prompt, context, config)

    assert "No valid options available for routing" in str(exc_info.value)


@pytest.mark.asyncio
async def test_route_prompt_unknown_type(config):
    """Test routing when an unknown option type is provided."""
    prompt = "Test prompt"
    context = {}
    config["options"].append(
        {
            "name": "Unknown Type",
            "description": "A test for unknown type",
            "type": "unknown",
        }
    )

    with pytest.raises(ValueError) as exc_info:
        await route_prompt(prompt, context, config)

    assert "Unknown option type: unknown" in str(exc_info.value)


@pytest.fixture
def mock_load_config():
    with patch(
        "app.routes.model_router.model_router_router.load_configuration"
    ) as mock:
        mock.return_value = {"some": "config"}
        yield mock


@pytest.fixture
def mock_route_prompt():
    with patch("app.routes.model_router.model_router_router.route_prompt") as mock:
        mock.return_value = {
            "response": "Routed response",
            "selected_option": {"name": "Model A"},
        }
        yield mock


@pytest.mark.asyncio
async def test_get_configuration_error():
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    with patch(
        "app.routes.model_router.model_router_router.load_configuration",
        side_effect=Exception("Configuration load error"),
    ):
        response = client.post(
            "/system/prompt_router/get_configuration/invoke", headers=headers
        )
        assert response.status_code == 500


@pytest.mark.asyncio
async def test_get_configuration_success(mock_load_config):
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/system/prompt_router/get_configuration/invoke", headers=headers
    )
    assert response.status_code == 200
    assert json.loads(response.json()["response"][0]["message"]) == {"some": "config"}


@pytest.mark.asyncio
async def test_route_prompt_experience_invalid_input():
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/experience/prompt_router/route_prompt/invoke",
        json={"bad": "data"},
        headers=headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_route_prompt_experience_success(mock_load_config, mock_route_prompt):
    valid_input = {"prompt": "test prompt", "context": {}}
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/experience/prompt_router/route_prompt/invoke",
        json=valid_input,
        headers=headers,
    )
    assert response.status_code == 200
    assert "Routed response" in response.json()["response"][0]["message"]


@pytest.mark.asyncio
async def test_route_prompt_experience_routing_error(mock_load_config):
    valid_input = {"prompt": "test prompt", "context": {}}
    with patch(
        "app.routes.model_router.model_router_router.route_prompt",
        side_effect=Exception("Routing error"),
    ):
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = client.post(
            "/experience/prompt_router/route_prompt/invoke",
            json=valid_input,
            headers=headers,
        )

        assert response.status_code == 500
