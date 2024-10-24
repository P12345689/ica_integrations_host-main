# -*- coding: utf-8 -*-
"""
Authors: Mihai Criveti
Description: Tests xlsx builder route.
"""

import json
import os
import sys
from typing import Any, Dict, Generator
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the app and necessary functions
from app.routes.xlsx_builder.xlsx_builder_router import app

# Configuration
API_KEY = "dev-only-token"
MOCK_XLSX_URL = "http://localhost:8080/public/xlsx_builder/xlsx_mock-id.xlsx"

client = TestClient(app)

# Type aliases
JSONDict = Dict[str, Any]


def mock_generate_xlsx(*args: Any, **kwargs: Any) -> str:
    return MOCK_XLSX_URL


@pytest.fixture
def mock_asyncio_to_thread() -> Generator[MagicMock, None, None]:
    with patch("asyncio.to_thread", side_effect=mock_generate_xlsx) as mock:
        yield mock


@pytest.fixture
def mock_call_prompt_flow() -> Generator[MagicMock, None, None]:
    with patch("app.routes.xlsx_builder.xlsx_builder_router.call_prompt_flow") as mock:
        yield mock


def test_generate_xlsx_single_sheet(mock_asyncio_to_thread: MagicMock) -> None:
    response = client.post(
        "/system/xlsx_builder/generate_xlsx/invoke",
        json={"csv_data": {"Product Data": "Product,Price,Quantity\nLaptop,1000,50\nPhone,500,200"}},
        headers={"Integrations-API-Key": API_KEY},
    )
    assert response.status_code == 200
    data: JSONDict = response.json()
    assert data["status"] == "success"
    assert MOCK_XLSX_URL in data["response"][0]["message"]


def test_generate_xlsx_multi_sheet(mock_asyncio_to_thread: MagicMock) -> None:
    response = client.post(
        "/system/xlsx_builder/generate_xlsx/invoke",
        json={
            "csv_data": {
                "Products": "Product,Price,Stock\nLaptop,1000,50\nPhone,500,200",
                "Sales": "Product,Sales\nLaptop,20000\nPhone,100000",
            }
        },
        headers={"Integrations-API-Key": API_KEY},
    )
    assert response.status_code == 200
    data: JSONDict = response.json()
    assert data["status"] == "success"
    assert MOCK_XLSX_URL in data["response"][0]["message"]


def test_generate_xlsx_complex_multi_sheet(mock_asyncio_to_thread: MagicMock) -> None:
    response = client.post(
        "/system/xlsx_builder/generate_xlsx/invoke",
        json={
            "csv_data": {
                "Employee Details": "Name,Age,Position\nJohn Doe,30,Engineer\nJane Smith,25,Designer",
                "Department Overview": "Department,Head\nEngineering,John Doe\nDesign,Jane Smith",
            }
        },
        headers={"Integrations-API-Key": API_KEY},
    )
    assert response.status_code == 200
    data: JSONDict = response.json()
    assert data["status"] == "success"
    assert MOCK_XLSX_URL in data["response"][0]["message"]


def test_generate_xlsx_invalid_input() -> None:
    response = client.post(
        "/system/xlsx_builder/generate_xlsx/invoke",
        json={"invalid_key": "invalid_data"},
        headers={"Integrations-API-Key": API_KEY},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_xlsx_experience_simple(
    mock_call_prompt_flow: MagicMock, mock_asyncio_to_thread: MagicMock
) -> None:
    mock_llm_response: JSONDict = {
        "csv_data": {
            "Books": "Title,Author,Publication Year\nBook1,Author1,2020\nBook2,Author2,2021\nBook3,Author3,2022\nBook4,Author4,2023\nBook5,Author5,2024"
        }
    }
    mock_call_prompt_flow.return_value = json.dumps(mock_llm_response)

    response = client.post(
        "/experience/xlsx_builder/generate_xlsx/invoke",
        json={
            "query": "Create an XLSX file with a list of 5 popular books, including their titles, authors, and publication years."
        },
        headers={"Integrations-API-Key": API_KEY},
    )
    assert response.status_code == 200
    data: JSONDict = response.json()
    assert data["status"] == "success"
    assert MOCK_XLSX_URL in data["response"][0]["message"]


@pytest.mark.asyncio
async def test_generate_xlsx_experience_multi_sheet(
    mock_call_prompt_flow: MagicMock, mock_asyncio_to_thread: MagicMock
) -> None:
    mock_llm_response: JSONDict = {
        "csv_data": {
            "Movies": "Title,Director,Year\nMovie1,Director1,2020\nMovie2,Director2,2021",
            "Box Office": "Title,Earnings\nMovie1,1000000\nMovie2,2000000",
        }
    }
    mock_call_prompt_flow.return_value = json.dumps(mock_llm_response)

    response = client.post(
        "/experience/xlsx_builder/generate_xlsx/invoke",
        json={
            "query": "Generate an XLSX file with two sheets: one for a list of popular movies and another for their box office earnings."
        },
        headers={"Integrations-API-Key": API_KEY},
    )
    assert response.status_code == 200
    data: JSONDict = response.json()
    assert data["status"] == "success"
    assert MOCK_XLSX_URL in data["response"][0]["message"]


@pytest.mark.asyncio
async def test_generate_xlsx_experience_complex(
    mock_call_prompt_flow: MagicMock, mock_asyncio_to_thread: MagicMock
) -> None:
    mock_llm_response: JSONDict = {
        "csv_data": {
            "Financial Summary": "Year,Quarter,Income,Expenses,Net Profit\n2021,Q1,100000,80000,20000\n2021,Q2,120000,90000,30000",
            "Quarterly Breakdown": "Year,Quarter,Category,Amount\n2021,Q1,Sales,80000\n2021,Q1,Marketing,20000",
        }
    }
    mock_call_prompt_flow.return_value = json.dumps(mock_llm_response)

    response = client.post(
        "/experience/xlsx_builder/generate_xlsx/invoke",
        json={
            "query": "Create an XLSX file with a summary of quarterly financial reports for the past three years. Include income, expenses, and net profit for each quarter."
        },
        headers={"Integrations-API-Key": API_KEY},
    )
    assert response.status_code == 200
    data: JSONDict = response.json()
    assert data["status"] == "success"
    assert MOCK_XLSX_URL in data["response"][0]["message"]


def test_generate_xlsx_experience_invalid_input() -> None:
    response = client.post(
        "/experience/xlsx_builder/generate_xlsx/invoke",
        json={"invalid_key": "invalid_data"},
        headers={"Integrations-API-Key": API_KEY},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_generate_xlsx_experience_llm_error(
    mock_call_prompt_flow: MagicMock,
) -> None:
    mock_call_prompt_flow.side_effect = Exception("LLM error")

    response = client.post(
        "/experience/xlsx_builder/generate_xlsx/invoke",
        json={"query": "Create an XLSX file with some data."},
        headers={"Integrations-API-Key": API_KEY},
    )
    assert response.status_code == 500
    data: JSONDict = response.json()
    assert "Failed to generate XLSX after all attempts" in data["detail"]


def test_xlsx_content() -> None:
    with patch("pandas.ExcelWriter") as mock_excel_writer, patch(
        "app.routes.xlsx_builder.xlsx_builder_router.generate_xlsx",
        side_effect=mock_generate_xlsx,
    ):
        mock_workbook = MagicMock()
        mock_excel_writer.return_value.__enter__.return_value = mock_workbook

        response = client.post(
            "/system/xlsx_builder/generate_xlsx/invoke",
            json={"csv_data": {"Sheet1": "Column1,Column2\nValue1,Value2"}},
            headers={"Integrations-API-Key": API_KEY},
        )

        assert response.status_code == 200
        data: JSONDict = response.json()
        assert data["status"] == "success"
        assert MOCK_XLSX_URL in data["response"][0]["message"]


if __name__ == "__main__":
    pytest.main(["-v", __file__])
