# -*- coding: utf-8 -*-
"""
Pytest for chart route.

Description: Tests xlsx builder route.

Authors: Andrei Colhon
"""

import os
from io import StringIO
from unittest.mock import patch

import pandas as pd
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.routes.xlsx_builder.xlsx_builder_router import (generate_xlsx,
                                                         write_csv_to_xlsx)
from app.server import app

client = TestClient(app)


def test_write_csv_to_xlsx(tmp_path, mock_csv_str):
    file_path = tmp_path / "public/xlsx_builder/test.xlsx"
    os.makedirs(file_path.parent, exist_ok=True)
    test_df = pd.read_csv(StringIO(mock_csv_str))
    write_csv_to_xlsx(test_df, file_path, "Sheet1")

    loaded_df = pd.read_excel(file_path, sheet_name="Sheet1")
    pd.testing.assert_frame_equal(test_df, loaded_df)


@patch("app.routes.xlsx_builder.xlsx_builder_router.write_csv_to_xlsx")
def test_generate_xlsx_valid_csv(
    mock_write_csv_to_xlsx,
    mock_csv_str,
    mock_sheet_str,
    mocker,
):
    mock_makedirs = mocker.patch("os.makedirs")
    file_url = generate_xlsx(mock_csv_str, mock_sheet_str)

    mock_makedirs.assert_called_once()
    mock_write_csv_to_xlsx.assert_called_once()
    assert "public/xlsx_builder" in file_url


def test_generate_xlsx_invalid_csv(
    mock_non_csv_str,
    mock_sheet_str,
):
    with pytest.raises(Exception) as e_info:
        generate_xlsx(mock_non_csv_str, mock_sheet_str)

    assert "Failed to generate XLSX: initial_value must be str or None, not int" in str(e_info.value)


@pytest.mark.asyncio
@patch("app.routes.xlsx_builder.xlsx_builder_router.write_csv_to_xlsx")
async def test_generate_xlsx_route(mock_write_csv_to_xlsx, mock_correct_csv_data):
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        mock_write_csv_to_xlsx.return_value = None
        test_data = mock_correct_csv_data
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/xlsx_builder/generate_xlsx/invoke", json=test_data, headers=headers)
    assert response.status_code == 200
    mock_write_csv_to_xlsx.assert_called_once()


@pytest.mark.asyncio
async def test_generate_xlsx_route_bad_data(mock_wrong_csv_data):
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        test_data = mock_wrong_csv_data
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post("/system/xlsx_builder/generate_xlsx/invoke", json=test_data, headers=headers)
    assert response.status_code == 422


@pytest.mark.asyncio
@patch("app.routes.xlsx_builder.xlsx_builder_router.write_csv_to_xlsx")
async def test_generate_xlsx_experience_route(mock_write_csv_to_xlsx, mock_experience_xlsx_query):
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        mock_write_csv_to_xlsx.return_value = None
        test_data = mock_experience_xlsx_query
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/experience/xlsx_builder/generate_xlsx/invoke",
            json=test_data,
            headers=headers,
        )
    assert response.status_code == 200
    mock_write_csv_to_xlsx.assert_called_once()


@pytest.mark.asyncio
async def test_generate_xlsx_experience_route_bad_data(
    mock_experience_xlsx_query_bad_format,
):
    async with AsyncClient(app=app, base_url=client.base_url) as ac:
        test_data = mock_experience_xlsx_query_bad_format
        headers = {
            "Content-Type": "application/json",
            "Integrations-API-Key": "dev-only-token",
        }
        response = await ac.post(
            "/experience/xlsx_builder/generate_xlsx/invoke",
            json=test_data,
            headers=headers,
        )
    assert response.status_code == 422
