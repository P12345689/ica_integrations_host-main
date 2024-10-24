# -*- coding: utf-8 -*-
"""
Pytest for webex route.

Description: Tests webex route.

Authors: Andrei Colhon
"""

from unittest.mock import Mock, patch

import pytest
import requests

from app.routes.webex.webex_router import webex_operation

WEBEX_API_BASE_URL = "https://webexapis.com/v1"


@patch("requests.get")
def test_webex_operation_list_transcripts(mock_get):
    sample_transcripts = {
        "items": [
            {"id": "1", "meetingTopic": "Meeting 1"},
            {"id": "2", "meetingTopic": "Meeting 2"},
        ]
    }

    mock_response = Mock()
    mock_response.json.return_value = sample_transcripts
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    token = "test_token"

    params = {}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    url = f"{WEBEX_API_BASE_URL}/meetingTranscripts"
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    transcripts = response.json().get("items", [])
    result = "\n".join([f"Transcript ID: {t['id']}, Meeting Topic: {t['meetingTopic']}" for t in transcripts])

    assert result == "Transcript ID: 1, Meeting Topic: Meeting 1\nTranscript ID: 2, Meeting Topic: Meeting 2"
    mock_get.assert_called_once_with(url, headers=headers, params=params)
    assert response.status_code == 200


@patch("requests.get")
def test_webex_operation_get_transcript(mock_get):
    sample_transcript = "This is the transcript"

    mock_response = Mock()
    mock_response.text = sample_transcript
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    token = "test_token"

    params = {"transcript_id": "121", "format": "test_format"}

    format_param = params.get("format", "vtt")

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    transcript_id = params.get("transcript_id")

    url = f"{WEBEX_API_BASE_URL}/meetingTranscripts/{transcript_id}/download"
    response = requests.get(url, headers=headers, params=format_param)
    response.raise_for_status()
    result = response.text

    assert result == "This is the transcript"
    assert response.status_code == 200
    mock_get.assert_called_once_with(url, headers=headers, params=format_param)


@patch("requests.get")
def test_webex_operation_list_meetings(mock_get):
    sample_response = {
        "items": [
            {
                "id": "1",
                "title": "Meeting 1",
                "start": "2023-07-12T09:00:00Z",
                "end": "2023-07-12T10:00:00Z",
                "timezone": "UTC",
            },
            {
                "id": "2",
                "title": "Meeting 2",
                "start": "2023-07-13T11:00:00Z",
                "end": "2023-07-13T12:00:00Z",
                "timezone": "UTC",
            },
        ]
    }

    mock_response = Mock()
    mock_response.json.return_value = sample_response
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_get.return_value = mock_response

    token = "test_token"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    url = f"{WEBEX_API_BASE_URL}/meetings"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    meetings = response.json().get("items", [])
    result = "\n".join(
        f"Meeting ID: {m['id']}, Meeting title: {m['title']}, Meeting start time: {m['start']}, Meeting end time: {m['end']}, Timezone: {m['timezone']}"
        for m in meetings
    )

    expected_result = (
        "Meeting ID: 1, Meeting title: Meeting 1, Meeting start time: 2023-07-12T09:00:00Z, Meeting end time: 2023-07-12T10:00:00Z, Timezone: UTC\n"
        "Meeting ID: 2, Meeting title: Meeting 2, Meeting start time: 2023-07-13T11:00:00Z, Meeting end time: 2023-07-13T12:00:00Z, Timezone: UTC"
    )

    mock_get.assert_called_once_with(url, headers=headers)
    assert response.status_code == 200
    assert result == expected_result


@patch("requests.post")
def test_webex_operation_invite_people(mock_post):
    sample_response = {"response": "query executed correctly"}

    mock_response = Mock()
    mock_response.json.return_value = sample_response
    mock_response.status_code = 200
    mock_response.raise_for_status = Mock()
    mock_post.return_value = mock_response

    token = "test_token"

    params = {"transcript_id": "121", "format": "test_format"}

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    url = f"{WEBEX_API_BASE_URL}/meetingInvitees"
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status()

    assert response.status_code == 200
    mock_post.asser_called_once()


def test_webex_operation_no_transcript_id():
    params = {}
    token = "test_token"

    with pytest.raises(Exception) as e_info:
        result = webex_operation(token=token, action="get_transcript", params=params)

    assert "Transcript ID is required to get a transcript" in str(e_info.value)


def test_webex_operation_no_meeting_id():
    params = {}
    token = "test_token"

    with pytest.raises(Exception) as e_info:
        result = webex_operation(token=token, action="invite_people", params=params)

    assert "Meeting ID is required to invite other people" in str(e_info.value)
