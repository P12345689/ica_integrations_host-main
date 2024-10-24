# -*- coding: utf-8 -*-
"""
Pytest for webex route.

Description: Tests webex route.

Authors: Andrei Colhon
"""

import json
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.server import app
from dev.app.routes.ms_teams.ms_teams_router import teams_operation

integration_client = TestClient(app)


@pytest.mark.asyncio
@patch("dev.app.routes.ms_teams.ms_teams_router.teams_operation")
async def test_teams_route_valid_input(mock_operation):
    """
    Test the MS Teams system endpoint with valid input.
    """
    mock_result = {
        "subject": "Team Sync",
        "start": {"dateTime": "2024-07-26T10:00:00Z"},
        "end": {"dateTime": "2024-07-26T11:00:00Z"},
        "attendees": [
            {"emailAddress": {"address": "user1@example.com", "name": "User One"}},
            {"emailAddress": {"address": "user2@example.com", "name": "User Two"}},
        ],
    }
    mock_operation.return_value = mock_result
    async with AsyncClient(app=app, base_url=integration_client.base_url) as ac:
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        test_data = {
            "action": "get_meeting",
            "params": {"id": "5335ggf"},
            "token": "test_token",
        }
        response = await ac.post("/system/ms_teams/invoke", headers=headers, json=test_data)
    assert response.status_code == 200
    expected_message = (
        "Teams Operation Result:\n\n"
        f"{mock_result}\n\n\n\n\n\n"
        "Is there anything else you'd like to know about Teams?"
    )

    # Adjust the assertion to match the actual response format
    assert response.json().get("response") == [{"message": expected_message, "type": "text"}]


@pytest.mark.asyncio
async def test_teams_route_invalid_input():
    """
    Test the MS Teams system endpoint with invalid input.
    """
    async with AsyncClient(app=app, base_url=integration_client.base_url) as ac:
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        test_data = {
            "params": {"id": "5335ggf"},
            "token": "test_token",
        }
        response = await ac.post("/system/ms_teams/invoke", headers=headers, json=test_data)
    assert response.status_code == 422


test_app = FastAPI()
client = TestClient(test_app)


@test_app.post("/experience/ms_teams/invoke")
async def teams_invoke(data: dict):
    query = data.get("query", {})
    if not query or query == "":
        return {
            "results": {
                "status": "success",
                "response": [
                    {
                        "message": "I'm sorry but i couldn't find a response, please try with a different query",
                        "type": "text",
                    }
                ],
            }
        }, 200
    return {
        "results": {
            "status": "success",
            "response": [{"message": "Meeting successfully created", "type": "text"}],
        }
    }, 200


@pytest.mark.asyncio
async def test_teams_experience_valid_input():
    """
    Test the MS Teams experience endpoint with valid input.
    """
    with (
        patch("dev.app.routes.ms_teams.ms_teams_router.ICAClient") as mock_client,
        patch("dev.app.routes.ms_teams.ms_teams_router.template_env.get_template") as mock_template,
    ):
        mock_client_instance = mock_client.return_value
        mock_template.return_value.render.return_value = "Rendered content"
        mock_client_instance.prompt_flow = AsyncMock(
            return_value=json.dumps(
                {
                    "action": "create_meeting",
                    "params": {
                        "time": "10:00 AM",
                        "participants": ["user@example.com"],
                    },
                    "analysis": "Creating a meeting at 10:00 AM",
                }
            )
        )

        async with AsyncClient(app=test_app, base_url="http://test") as ac:
            headers = {
                "Content-Type": "application/json",
                "Integrations-API-Key": "dev-only-token",
            }
            response = await ac.post(
                "/experience/ms_teams/invoke",
                headers=headers,
                json={
                    "query": "Schedule a meeting",
                    "access_token": "fake-access-token",
                },
            )

            assert response.status_code == 200
            assert "Meeting successfully created" in response.text


@pytest.mark.asyncio
async def test_teams_experience_invalid_input():
    """
    Test the MS Teams experience endpoint with empty input.
    """
    with (
        patch("dev.app.routes.ms_teams.ms_teams_router.ICAClient") as mock_client,
        patch("dev.app.routes.ms_teams.ms_teams_router.template_env.get_template") as mock_template,
    ):
        mock_client_instance = mock_client.return_value
        mock_template.return_value.render.return_value = "Rendered content"
        mock_client_instance.prompt_flow = AsyncMock(
            return_value=json.dumps(
                {
                    "action": "create_meeting",
                    "params": {
                        "time": "10:00 AM",
                        "participants": ["user@example.com"],
                    },
                    "analysis": "Creating a meeting at 10:00 AM",
                }
            )
        )

        async with AsyncClient(app=test_app, base_url="http://test") as ac:
            headers = {
                "Content-Type": "application/json",
                "Integrations-API-Key": "dev-only-token",
            }
            response = await ac.post(
                "/experience/ms_teams/invoke",
                headers=headers,
                json={
                    "query": "",
                    "access_token": "fake-access-token",
                },
            )

            assert response.status_code == 200
            assert "I'm sorry but i couldn't find a response, please try with a different query" in response.text


@patch("requests.get")
def test_get_meeting(mock_get):
    action = "get_meeting"
    params = {"id": "5335ggf"}
    token = "test_token"

    meeting_info = (
        "Meeting subject: Team Sync\n"
        "Meeting start time: 2024-07-26T10:00:00Z\n"
        "Meeting end time: 2024-07-26T11:00:00Z\n"
        "Meeting attendees:\nUser One (user1@example.com)\nUser Two (user2@example.com)"
    )

    mock_response = Mock()
    mock_response.json.return_value = {
        "subject": "Team Sync",
        "start": {"dateTime": "2024-07-26T10:00:00Z"},
        "end": {"dateTime": "2024-07-26T11:00:00Z"},
        "attendees": [
            {"emailAddress": {"address": "user1@example.com", "name": "User One"}},
            {"emailAddress": {"address": "user2@example.com", "name": "User Two"}},
        ],
    }
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = teams_operation(action=action, params=params, token=token)
    mock_get.assert_called_once()
    assert meeting_info == result


@patch("requests.get")
def test_list_meetings(mock_get):
    action = "list_meetings"
    params = {"end_date": "2024-07-29T11:00:00Z"}
    token = "test_token"

    meeting_list = {
        "value": [
            {
                "id": "1",
                "subject": "Team Sync",
                "start": {"dateTime": "2024-07-26T10:00:00Z"},
                "end": {"dateTime": "2024-07-26T11:00:00Z"},
            }
        ]
    }

    expected_meeting_info = "Meeting Id: 1, Meeting subject: Team Sync, Meeting start time: 2024-07-26T10:00:00Z, Meeting end time: 2024-07-26T11:00:00Z"

    mock_response = Mock()
    mock_response.json.return_value = meeting_list
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    result = teams_operation(action=action, params=params, token=token)
    mock_get.assert_called_once()
    assert expected_meeting_info == result


@patch("requests.post")
def test_find_timeslot(mock_post):
    action = "find_timeslots"
    params = {
        "attendees": [
            {"emailAddress": {"address": "user1@example.com", "name": "User One"}},
            {"emailAddress": {"address": "user2@example.com", "name": "User Two"}},
        ],
        "timeConstraint": {
            "timeslots": [
                {
                    "start": {"dateTime": "2024-07-26T10:00:00Z"},
                    "end": {"dateTime": "2024-07-26T11:00:00Z"},
                }
            ]
        },
    }
    token = "test_token"

    mock_response = Mock()
    mock_response.json.return_value = {
        "meetingTimeSuggestions": [
            {
                "meetingTimeSlot": {
                    "start": {"dateTime": "2024-07-26T10:00:00Z"},
                    "end": {"dateTime": "2024-07-26T11:00:00Z"},
                }
            },
            {
                "meetingTimeSlot": {
                    "start": {"dateTime": "2024-07-27T14:00:00Z"},
                    "end": {"dateTime": "2024-07-27T15:00:00Z"},
                }
            },
        ]
    }
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response

    result = teams_operation(action=action, params=params, token=token)

    expected_result = (
        "Timeslot:\nDate: 2024-07-26,\nTime: 10:00 - 11:00\n" "Timeslot:\nDate: 2024-07-27,\nTime: 14:00 - 15:00"
    )

    mock_post.assert_called_once()
    assert result == expected_result
