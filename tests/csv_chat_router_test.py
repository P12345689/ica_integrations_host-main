# -*- coding: utf-8 -*-
"""
Pytest for CSV_chat route.

Description: Tests CSV_chat route.

Authors: Andrei Colhon
"""

import json
from unittest import mock
from unittest.mock import AsyncMock, MagicMock, patch
from wsgiref import headers
import pandas as pd
from pandas.testing import assert_frame_equal

from fastapi import HTTPException, UploadFile
import pytest
from fastapi.testclient import TestClient
from io import StringIO, BytesIO

from app.server import app

client = TestClient(app)

from app.routes.csv_chat.csv_chat_router import (
    extract_column_unique_values,
    load_dataframe,
    sanitize_code,
    sanitize_user_input,
    MAX_FILE_SIZE,
    process_csv_chat,
    execute_code_with_timeout,
    safe_load_dataframe,
)

client = TestClient(app)

MAX_DATAFRAME_ROWS = 4
MAX_DATAFRAME_COLS = 4


@pytest.fixture
def csv_content():
    return "col1,col2\nval1,val2\nval3,val4\n"


@pytest.fixture
def dataframe(csv_content):
    return pd.read_csv(StringIO(csv_content))


def test_sanitize_user_input():
    assert sanitize_user_input("normal query") == "normal query"
    assert sanitize_user_input("drop table users;") is None


def test_sanitize_code():
    safe_code = "df.head()"
    dangerous_code = "import os; os.system('rm -rf /')"
    assert sanitize_code(safe_code) == safe_code
    with pytest.raises(ValueError):
        sanitize_code(dangerous_code)


@pytest.mark.asyncio
async def test_load_dataframe(csv_content, dataframe):
    df = await load_dataframe(csv_content=csv_content)
    assert_frame_equal(df, dataframe)


def test_extract_column_unique_values(dataframe):
    result = extract_column_unique_values(dataframe)
    expected = "col1: val1, val3\ncol2: val2, val4"
    assert result == expected


csv_data = "col1,col2\n1,2\n3,4"
large_csv_data = "col1,col2\n" + "\n".join(["1,2"] * (MAX_DATAFRAME_ROWS + 1))
csv_file_url = "http://example.com/data.csv"
xlsx_file_url = "http://example.com/data.xlsx"


@pytest.mark.asyncio
async def test_load_dataframe_from_csv_content():
    with patch("pandas.read_csv") as mock_read_csv:
        mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
        mock_read_csv.return_value = mock_df
        df = await load_dataframe(csv_content="col1,col2\n1,2\n3,4")
        assert df.equals(mock_df)
        assert df.shape == (2, 2)


mock_df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})


@pytest.mark.asyncio
@patch("requests.get")
async def test_load_dataframe_from_url(mock_get):
    mock_response = MagicMock()
    mock_response.__enter__.return_value.raise_for_status = MagicMock()
    mock_response.__enter__.return_value.iter_content = MagicMock(
        return_value=[b"col1,col2\n1,2\n3,4"]
    )
    mock_get.return_value = mock_response

    with patch("pandas.read_csv", return_value=mock_df) as mock_read_csv:
        df = await load_dataframe(file_url="http://example.com/data.csv")
        mock_read_csv.assert_called_once()
        assert df.equals(mock_df)
        assert df.shape == (
            2,
            2,
        )


@pytest.mark.asyncio
async def test_load_dataframe_from_upload_file():
    content = b"col1,col2\n5,6\n7,8"
    upload_file = UploadFile(filename="data.csv", file=BytesIO(content))
    with (
        patch.object(upload_file, "read", return_value=content),
        patch("pandas.read_csv", return_value=mock_df) as mock_read_csv,
    ):
        df = await load_dataframe(file=upload_file)
        mock_read_csv.assert_called_once()
        assert df.equals(mock_df)
        assert df.shape == (2, 2)


@pytest.mark.asyncio
async def test_file_size_exceeds_limit():
    large_content = b"a" * (MAX_FILE_SIZE + 1)
    upload_file = UploadFile(filename="data.csv", file=BytesIO(large_content))
    with patch.object(upload_file, "read", return_value=large_content):
        with pytest.raises(ValueError) as excinfo:
            await load_dataframe(file=upload_file)
        assert "File size exceeds the maximum allowed size" in str(excinfo.value)


@pytest.mark.asyncio
async def test_unsupported_file_format():
    upload_file = UploadFile(filename="data.unsupported", file=BytesIO(b"some content"))
    with patch.object(upload_file, "read", return_value=b"some content"):
        with pytest.raises(ValueError) as excinfo:
            await load_dataframe(file=upload_file)
        assert "Unsupported file format" in str(excinfo.value)


mock_df_2 = MagicMock()
mock_df_2.shape = (100, 2)
mock_df_2.head.return_value.to_dict.return_value = {"col1": [1, 2], "col2": [3, 4]}
mock_df_2.describe.return_value.to_dict.return_value = {
    "col1": {"count": 100, "mean": 2},
    "col2": {"count": 100, "mean": 4},
}


@pytest.mark.asyncio
@patch("app.routes.csv_chat.csv_chat_router.safe_load_dataframe")
@patch("app.routes.csv_chat.csv_chat_router.process_csv_chat")
@patch("app.routes.csv_chat.csv_chat_router.sanitize_user_input")
async def test_chat_with_csv(mock_sanitize, mock_process_chat, mock_load_df):
    mock_sanitize.return_value = "safe query"
    mock_load_df.return_value = mock_df_2
    mock_process_chat.return_value = json.dumps(
        {"code": "print('Hello World')", "message": "test message"}
    )

    headers = {
        "Integrations-API-Key": "dev-only-token",
    }

    response = client.post(
        "/experience/csv_chat/ask/invoke",
        data={"query": "data summary", "csv_content": "col1,col2\n1,2\n3,4"},
        headers=headers,
    )

    assert response.status_code == 200
    assert "success" in response.json()["status"]


@patch(
    "app.routes.csv_chat.csv_chat_router.safe_load_dataframe",
    side_effect=ValueError("Data loading failed"),
)
async def test_chat_with_csv_data_error(mock_load_df):
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/experience/csv_chat/ask/invoke",
        json={"query": "data summary", "csv_content": "invalid data"},
        headers=headers,
    )

    assert response.status_code == 200
    assert "error" in response.json()["status"]
    assert "Data loading failed" in response.json()["response"][0]["message"]


@pytest.mark.asyncio
@patch("app.routes.csv_chat.csv_chat_router.load_dataframe")
async def test_get_csv_info(mock_load_df):
    data = {
        "col1": range(100),
        "col2": range(100),
    }
    mock_df = pd.DataFrame(data)

    mock_load_df.return_value = mock_df

    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }

    response = client.post(
        "/system/csv_chat/info/invoke",
        json={"csv_content": "col1,col2\n1,2\n3,4"},
        headers=headers,
    )

    assert response.status_code == 200
    info = json.loads(response.json()["response"][0]["message"])
    expected_shape = [100, 2]
    assert info["shape"] == expected_shape
    assert "columns" in info


@patch(
    "app.routes.csv_chat.csv_chat_router.load_dataframe",
    side_effect=Exception("Loading error"),
)
async def test_get_csv_info_error(mock_load_df):
    headers = {
        "Content-Type": "application/json",
        "Integrations-API-Key": "dev-only-token",
    }
    response = client.post(
        "/system/csv_chat/info/invoke",
        json={"csv_content": "invalid content"},
        headers=headers,
    )

    assert response.status_code == 500
    assert "Loading error" in response.content.decode()
